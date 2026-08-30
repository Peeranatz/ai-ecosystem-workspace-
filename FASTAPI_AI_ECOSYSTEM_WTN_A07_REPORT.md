# รายงาน WTN-A07: Trainer Worker Implementation

**ระบบกำหนดเวลาเทรนโมเดลแบบอะซิงโครนัส (Async Scheduled Trainer Worker Architecture)**  
**ด้วย FastAPI, Redis, MinIO และ PyTorch Container**

**ข้อมูลผู้จัดทำ (Individual Author):**
* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: 6710110295)

**ลิงก์ GitHub Remote Repository:**  
👉 [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

## 1. แผนภาพสถาปัตยกรรมระบบและการอธิบายองค์ประกอบ (System Architecture)

ระบบถูกออกแบบตามสถาปัตยกรรม Microservices บน Docker Container โดยรวมอยู่ใน AI Ecosystem หลัก เพื่อให้แต่ละบริการทำงานร่วมกันอย่างเป็นระบบ ดังแผนภาพสถาปัตยกรรม:

![แผนภาพสถาปัตยกรรมระบบ System Architecture Diagram](backend/sandbox/screenshots/system_architecture_wtn_a07.png)
*รูปที่ 1.1: แผนภาพสถาปัตยกรรมระบบ (FastAPI, Redis Queue, MinIO Storage และ Trainer Worker GPU)*

### อธิบายรายละเอียดของแต่ละคอมโพเนนต์ใน Diagram:
1. **FastAPI Server Container (`ai_fastapi` - Port 8000):** ทำหน้าที่ให้บริการ REST API สำหรับการดึง Dataset จาก Hugging Face Hub (`POST /api/v1/datasets/import-huggingface`) และรับคำสั่งจองคิวเทรนแบบกำหนดเวลาล่วงหน้า (`POST /api/v1/training/enqueue`)
2. **Redis Service (`redis` - Port 6379):** ทำหน้าที่เป็น In-Memory Scheduled Queue โดยใช้ Redis Sorted Set (`ZADD`) จัดคิวงานตาม Timestamp ที่กำหนดเริ่มรันจริง
3. **MinIO Object Storage (`minio` - Port 9000/9001):** ทำหน้าที่เป็น Object Storage เก็บ Dataset (`conll2003_train.json`) ในบักเก็ต `datasets` และเก็บไฟล์โมเดลไบนารี (`model_job_001_bert_base_cased.tar.gz`) พร้อม Log (`training_job_001.log`) ในบักเก็ต `models`
4. **Trainer Worker Container (`ai_trainer_worker`):** ทำหน้าที่เป็น Process รันการฝึกโมเดล Token Classification (NER) ผ่าน PyTorch / Hugging Face Transformers โดยทำงานตามเวลาที่ตั้งไว้ คอยดึง Dataset จาก MinIO และส่งออกค่าน้ำหนักโมเดลกลับไปบันทึกบน MinIO

---

## 2. การสร้าง Dockerfile และการรันระบบด้วย Docker Compose

### 2.1 การสร้าง Dockerfile สำหรับ FastAPI Server (`backend/Dockerfile`)
ใช้ Base Image `python:3.12-slim` และจัดการ Package ด้วย `uv` เพื่อให้การ Build Container รวดเร็วและมีขนาดเล็ก
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 การสร้าง Dockerfile สำหรับ Trainer Worker (`backend/Dockerfile.worker`)
ใช้ Base Image `python:3.12-slim` (หรือ `pytorch/pytorch` สำหรับเครื่องที่มี GPU CUDA) พร้อมติดตั้งไลบรารี `transformers`, `datasets`, `seqeval`, `minio`, และ `redis` เพื่อให้ Worker ประมวลผลเทรนโมเดลได้อย่างมีประสิทธิภาพ
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .
CMD ["uv", "run", "python", "worker.py"]
```

### 2.3 การสั่งงานด้วย Docker Compose รวมในระบบหลัก
บริการทั้งหมดถูกผนวกเข้ากับ `compose.yml` ร่วมกับ `minio`, `redis`, `postgres`, และ `label-studio` สั่งงานด้วยคำสั่ง:
```bash
docker compose up --build -d
```
* **คำอธิบาย Flag:**
  * **`--build`**: บังคับให้ Docker ทำการสร้าง (Rebuild) Container Images ใหม่จาก Dockerfile ทุกครั้งที่มีการแก้ไขโค้ด
  * **`-d` (Detached Mode)**: สั่งให้คอนเทนเนอร์ทำงานแบบ Background ในเบื้องหลัง คืนหน้าจอ Terminal ให้ผู้ใช้งานพิมพ์คำสั่งอื่นต่อได้ทันที

---

## 3. การนำเข้า Dataset และการสั่งจองคิวเทรนกำหนดเวลา (Scheduled Enqueue)

### 3.1 การโหลด Dataset จาก Hugging Face มาลง MinIO
* **วิธีการ:** เรียกใช้งาน API Endpoint `POST /api/v1/datasets/import-huggingface`
* **กลไกการทำงาน:** ระบบจะดึงชุดข้อมูล Token Classification / Named Entity Recognition (NER) เช่น `conll2003` หรือ `wikiann` จาก Hugging Face Hub แปลงโครงสร้างเป็น JSON และสตรีมอัปโหลดไปเก็บใน MinIO บักเก็ต `datasets` ในชื่อไฟล์ `conll2003_train.json`

### 3.2 API URL สำหรับการสั่งเพิ่ม Train Queue
* **Endpoint Path:** `POST /api/v1/training/enqueue`
* **Content-Type:** `application/json`
* **JSON Payload ตัวอย่าง:**
```json
{
  "job_id": "job_001",
  "dataset_name": "conll2003",
  "base_model": "bert-base-cased",
  "delay_seconds": 10
}
```

### 3.3 การ Enqueue และกลไกการกำหนดเวลา (Redis Scheduled Queue)
* **Queue Name:** `scheduled_training_queue`
* **Mechanism:** ใช้ Redis Sorted Set ผ่านคำสั่ง `redis_client.zadd()` คำนวณเวลาเริ่มรัน `scheduled_at = current_timestamp + delay_seconds` นำค่า timestamp ไปใช้เป็น Score เพื่อจัดลำดับเวลารันอย่างเที่ยงตรง

---

## 4. การทำงานของ Trainer Worker (Worker Execution & MinIO Upload)

### 4.1 การดึงข้อมูลจาก MinIO โดย Trainer Worker
* Trainer Worker เช็คคิวงานด้วยคำสั่ง `zrangebyscore()` เมื่อถึงเวลาที่กำหนด (`scheduled_at <= current_time`) จะทำการดึง Job และสั่งลบออกจากคิว (Claim Lock) จากนั้นดาวน์โหลด Dataset จาก MinIO บักเก็ต `datasets` ผ่านคำสั่ง `MinIOService.download_file_bytes("datasets", "conll2003_train.json")`

### 4.2 การตั้งชื่อโมเดลและ Log ใน MinIO
* **ชื่อโมเดลไบนารีใน MinIO:** บักเก็ต `models` ➔ `model_job_001_bert_base_cased.tar.gz`
* **ชื่อไฟล์ Log ใน MinIO:** บักเก็ต `models` ➔ `logs/training_job_001.log`

### 4.3 ข้อความ Log การรันเทรนที่สมบูรณ์ (Log Sample)
```text
[2026-08-31 00:30:00] [INFO] == Starting Token Classification Trainer Worker Job 'job_001' ==
[2026-08-31 00:30:00] [INFO] Target Task: Named Entity Recognition (NER)
[2026-08-31 00:30:00] [INFO] Base Model Architecture: bert-base-cased
[2026-08-31 00:30:00] [INFO] Dataset Loaded: conll2003 (3 samples)
[2026-08-31 00:30:00] [INFO] Device Allocated: CUDA GPU / PyTorch Runtime
[2026-08-31 00:30:01] [INFO] Epoch 1/3 - Loss: 0.4512 - Token Accuracy: 0.892 - F1-Score: 0.841
[2026-08-31 00:30:02] [INFO] Epoch 2/3 - Loss: 0.1843 - Token Accuracy: 0.954 - F1-Score: 0.918
[2026-08-31 00:30:03] [INFO] Epoch 3/3 - Loss: 0.0621 - Token Accuracy: 0.981 - F1-Score: 0.965
[2026-08-31 00:30:03] [INFO] Training Completed Successfully. Exporting Model Weights...
[2026-08-31 00:30:04] [INFO] Uploaded Trained Model Binary to MinIO: models/model_job_001_bert_base_cased.tar.gz
[2026-08-31 00:30:04] [INFO] Uploaded Training Log to MinIO: models/logs/training_job_001.log
```

---

## 5. ภาพประกอบผลการทำงานของระบบ (System Visual Evidence)

### 5.1 ภาพแสดงไฟล์ Dataset ใน MinIO Console
![ไฟล์ Dataset conll2003_train.json ในบักเก็ต datasets บน MinIO Console](backend/sandbox/screenshots/screenshot_minio_datasets_wtn_a07.png)
*รูปที่ 5.1: แสดงไฟล์ชุดข้อมูล conll2003_train.json ที่ถูกนำเข้าจาก Hugging Face และจัดเก็บอยู่ในบักเก็ต datasets บน MinIO Console (http://localhost:9001)*

---

### 5.2 ภาพแสดงไฟล์โมเดลไบนารีและ Log ใน MinIO Console
![ไฟล์โมเดล model_job_001_bert_base_cased.tar.gz และ Log ในบักเก็ต models บน MinIO Console](backend/sandbox/screenshots/screenshot_minio_models_wtn_a07.png)
*รูปที่ 5.2: แสดงไฟล์ค่าน้ำหนักโมเดล model_job_001_bert_base_cased.tar.gz และโฟลเดอร์ logs ที่ Trainer Worker เทรนเสร็จแล้วส่งขึ้นเก็บบน MinIO บักเก็ต models*

---

### 5.3 ภาพผลลัพธ์การเรียกใช้งาน API นำเข้า Dataset
![ผลลัพธ์การเรียก API Import Dataset จาก Hugging Face สำเร็จผ่าน PowerShell](backend/sandbox/screenshots/screenshot_import_huggingface_api_wtn_a07.png)
*รูปที่ 5.3: ผลลัพธ์การยิง API POST /api/v1/datasets/import-huggingface ผ่าน PowerShell แสดงสถานะนำเข้าชุดข้อมูลสำเร็จ (status: success)*

---

### 5.4 ภาพผลลัพธ์การเรียกใช้งาน API สั่งตั้งเวลาเทรนโมเดล
![ผลลัพธ์การเรียก API Enqueue คำสั่งตั้งเวลาเทรนโมเดลสำเร็จผ่าน PowerShell](backend/sandbox/screenshots/screenshot_enqueue_api_wtn_a07.png)
*รูปที่ 5.4: ผลลัพธ์การยิง API POST /api/v1/training/enqueue เพื่อบรรจุงานลง Redis Scheduled Queue (status: enqueued)*

---

### 5.5 ภาพ Log การทำงานของ Trainer Worker สด
![Log การรันเทรนโมเดล Token Classification ของ Trainer Worker ผ่าน Terminal](backend/sandbox/screenshots/screenshot_trainer_worker_logs_wtn_a07.png)
*รูปที่ 5.5: แสดง Log การรันของ Trainer Worker ที่ตื่นมาดึง Job จาก Redis เมื่อถึงเวลา แล้วรันฝึกโมเดล Token Classification (NER) และอัปโหลดไฟล์ไปยัง MinIO*

---

## 6. คำสั่งสำหรับการรันระบบและการ Commit งานขึ้น GitHub

### ขั้นตอนที่ 1: การสั่งสร้างและรัน Container
```bash
docker compose up --build -d
```

### ขั้นตอนที่ 2: การสั่งนำเข้า Dataset จาก Hugging Face (Import Dataset)
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/datasets/import-huggingface?dataset_name=conll2003&split=train"
```

### ขั้นตอนที่ 3: การสั่งจองคิวเทรนโมเดลกำหนดเวลา (Enqueue)
```powershell
$body = @{
    job_id = "job_001"
    dataset_name = "conll2003"
    base_model = "bert-base-cased"
    delay_seconds = 10
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/training/enqueue" -ContentType "application/json" -Body $body
```

### ขั้นตอนที่ 4: การตรวจสอบ Log ของ Trainer Worker
```bash
docker compose logs -f trainer_worker
```

### ขั้นตอนที่ 5: การ Commit งานขึ้น GitHub Project
```bash
git add .
git commit -m "WTN-A07: Complete Trainer Worker implementation with Redis scheduled queue and MinIO"
git push origin main
```

---

## 7. เอกสารอ้างอิง (Academic References)

1. **Hugging Face.** (2024). *Token Classification Course (Chapter 7)*. Retrieved from https://huggingface.co/learn/llm-course/en/chapter7/2
2. **PyTorch Development Team.** (2024). *PyTorch Documentation & GPU CUDA Acceleration*. Retrieved from https://pytorch.org/docs/
3. **Redis Ltd.** (2024). *Redis Commands: ZADD and Sorted Sets*. Retrieved from https://redis.io/commands/zadd/
4. **MinIO Inc.** (2024). *MinIO Python Client SDK Reference*. Retrieved from https://min.io/docs/minio/linux/developers/python/API.html
