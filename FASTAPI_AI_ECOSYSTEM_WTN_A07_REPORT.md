# รายงาน WTN-A07: Trainer Worker Implementation (ฉบับเชิงลึกสมบูรณ์)

**ระบบกำหนดเวลาเทรนโมเดลแบบอะซิงโครนัส (Async Scheduled Trainer Worker Architecture)**  
**ด้วย FastAPI, Redis Scheduled Queue, MinIO Object Storage และ PyTorch Container Execution**

**ข้อมูลผู้จัดทำ (Individual Author):**
* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: 6710110295)

**ลิงก์ GitHub Remote Repository:**  
👉 [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

## 1. แผนภาพสถาปัตยกรรมระบบและการอธิบายองค์ประกอบเชิงลึก (System Architecture & Component Mechanics)

ระบบถูกออกแบบตามหลักการ **Cloud-Native Microservices** บน Docker Container โดยแยกการทำงานระหว่างบริการรับคำขอ (API Gateway Layer), บริการจัดการคิวงาน (In-Memory Queue Layer), บริการจัดเก็บข้อมูล (Object Storage Layer) และบริการประมวลผลเทรนโมเดล (Compute Worker Layer) อย่างเด็ดขาด (Decoupled Architecture)

![แผนภาพสถาปัตยกรรมระบบ System Architecture Diagram](backend/sandbox/screenshots/system_architecture_wtn_a07.png)
*รูปที่ 1.1: แผนภาพสถาปัตยกรรมระบบ (FastAPI, Redis Queue, MinIO Storage และ Trainer Worker GPU)*

### อธิบายรายละเอียดของแต่ละคอมโพเนนต์ใน Diagram:

1. **FastAPI Server Container (`ai_fastapi` - Port 8000):**
   * **บทบาท:** ทำหน้าที่เป็น REST API Gateway สำหรับรับ HTTP Requests จากภายนอก
   * **หน้าที่หลัก:**
     - ให้บริการ Endpoint `POST /api/v1/datasets/import-huggingface` เพื่อเชื่อมต่อและดึงชุดข้อมูลจาก Hugging Face Hub เข้ามาบันทึกบน MinIO
     - ให้บริการ Endpoint `POST /api/v1/training/enqueue` เพื่อรับพารามิเตอร์การจองคิวเทรน เช่น `job_id`, `base_model`, `delay_seconds` แล้วเขียนข้อมูลบรรจุลงคิว Redis

2. **Redis Service (`redis` - Port 6379):**
   * **บทบาท:** ทำหน้าที่เป็น In-Memory Scheduled Queue สำหรับจัดลำดับงานที่ต้องประมวลผลล่วงหน้า
   * **กลไกเชิงลึก:** ใช้โครงสร้างข้อมูลชนิด **Redis Sorted Set (`ZADD`)** โดยกำหนดให้ค่า Unix Timestamp เป้าหมาย (`scheduled_at`) ทำหน้าที่เป็น **Score** เพื่อเรียงลำดับคิวจากเวลาที่ต้องเริ่มรันก่อนไปหลัง

3. **MinIO Object Storage (`minio` - Port 9000/9001):**
   * **บทบาท:** ทำหน้าที่เป็น Centralized Object Storage (S3 API Compatible) จัดเก็บข้อมูลที่จำเป็นทั้งหมดของระบบ
   * **โครงสร้างการเก็บบักเก็ต:**
     - **บักเก็ต `datasets`:** จัดเก็บไฟล์ชุดข้อมูลดิบที่ดาวน์โหลดมาจาก Hugging Face ในรูปแบบไฟล์ JSON เช่น `conll2003_train.json`
     - **บักเก็ต `models`:** จัดเก็บไฟล์ค่าน้ำหนักโมเดลไบนารีที่ฝึกสำเร็จแล้ว เช่น `model_job_001_bert_base_cased.tar.gz` พร้อมทั้งไฟล์ Log การเทรนในโฟลเดอร์ `logs/training_job_001.log`

4. **Trainer Worker Container (`ai_trainer_worker`):**
   * **บทบาท:** ทำหน้าที่เป็น Background Compute Worker ที่รันอย่างเป็นอิสระ (Background Daemon)
   * **กลไกเชิงลึก:** คอยคิวเร่งดึงงานจาก Redis แบบ Polling Loop เมื่อถึงเวลาเริ่มรัน ทำการดาวน์โหลด Dataset จาก MinIO มา Fine-tune โมเดล Token Classification (NER) ผ่าน PyTorch / Hugging Face Transformers บน GPU/CPU แล้วสตรีมไฟล์โมเดลไบนารีและ Log กลับไปบันทึกบน MinIO

---

## 2. การสร้าง Dockerfile และการรันระบบด้วย Docker Compose

### 2.1 การสร้าง Dockerfile สำหรับ FastAPI Server (`backend/Dockerfile`)
ใช้ Base Image `python:3.12-slim` และใช้ `uv` เป็น Package Manager เพื่อให้การสตรีม Build Container รวดเร็วและมีขนาดเบาที่สุด
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
ติดตั้งไลบรารีทางด้าน Machine Learning ได้แก่ `torch`, `transformers`, `datasets`, `seqeval` ร่วมกับ `redis` และ `minio` สำหรับการประมวลผลเทรนโมเดล
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

### 2.3 การส่งผ่าน GPU Acceleration (NVIDIA Container Toolkit)
หากต้องการประมวลผลบนฮาร์ดแวร์ GPU CUDA สามารถเพิ่มการตั้งค่าทรัพยากรใน `compose.yml` ภายใต้บริการ `trainer_worker`:
```yaml
trainer_worker:
  build:
    context: .
    dockerfile: Dockerfile.worker
  environment:
    - REDIS_HOST=redis
    - MINIO_ENDPOINT=minio:9000
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]
```

### 2.4 การรันด้วย Docker Compose
บริการทั้งหมดสั่งงานรวมกันผ่านคำสั่ง:
```bash
docker compose up --build -d
```
* **คำอธิบาย Flag:**
  * **`--build`**: บังคับให้ Docker สร้าง (Rebuild) Container Images ใหม่จาก Dockerfile ป้องกันการใช้ Cache เก่าที่มีโค้ดตกรุ่น
  * **`-d` (Detached Mode)**: สั่งให้คอนเทนเนอร์ทำงานแบบ Background ในเบื้องหลัง คืนหน้าจอ Terminal ให้ผู้ใช้งานพิมพ์คำสั่งอื่นต่อได้ทันที

---

## 3. การนำเข้า Dataset และกลไก Redis Scheduled Queue เชิงลึก

### 3.1 การโหลด Dataset จาก Hugging Face มาลง MinIO
* **Endpoint Path:** `POST /api/v1/datasets/import-huggingface`
* **พารามิเตอร์ Query:** `dataset_name=conll2003`, `split=train`
* **กลไกการทำงาน:**
  1. FastAPI ดึงชุดข้อมูล Token Classification / Named Entity Recognition (NER) จาก Hugging Face Datasets Hub
  2. แปลงโครงสร้างข้อมูลเป็น JSON Format ที่ประกอบด้วย `tokens` และ `ner_tags`
  3. สตรีมอัปโหลดไปจัดเก็บยัง MinIO บักเก็ต `datasets` ในชื่อไฟล์ `conll2003_train.json`

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

### 3.3 กลไกการ Enqueue และโครงสร้าง Redis Scheduled Queue
* **ชื่อ Queue ใน Redis:** `scheduled_training_queue`
* **กลไกเชิงลึก (Atomic Scheduling):**
  1. ระบบคำนวณเวลาเริ่มประมวลผลจริง: `scheduled_at = current_unix_timestamp + delay_seconds`
  2. เรียกคำสั่ง `redis_client.zadd("scheduled_training_queue", {payload_json: scheduled_at})`
  3. ค่า `scheduled_at` จะถูกนำไปใช้เป็น **Score** ใน Sorted Set ทำให้คิวงานถูกจัดเรียงตามลำดับเวลาอย่างแม่นยำ

---

## 4. การทำงานของ Trainer Worker (Worker Mechanics, Token Classification & Upload)

### 4.1 การดึงข้อมูลแบบ Atomic Lock ป้องกัน Worker แย่งงานกัน (Concurrency Control)
เพื่อรองรับกรณีที่มี Trainer Worker รันพร้อมกันหลายตัว (Horizontal Scaling) การดึงงานจากคิวจะทำผ่านกลไก Atomic Claim Lock:
```python
# 1. ค้นหางานที่ถึงเวลาเริ่มรันแล้ว (score <= current_timestamp)
ready_jobs = redis_client.zrangebyscore("scheduled_training_queue", 0, current_timestamp, start=0, num=1)

if ready_jobs:
    job_payload = ready_jobs[0]
    # 2. ปลดล็อคคิวแบบ Atomic ด้วย ZREM เพื่อรับประกันว่ามี Worker เพียงตัวเดียวที่ได้งานนี้ไปทำ
    if redis_client.zrem("scheduled_training_queue", job_payload):
        # ดำเนินการเทรนโมเดล...
```

### 4.2 รายละเอียดงาน Token Classification (Named Entity Recognition - NER) & BIO Tagging Scheme
โมเดลที่ Worker ทำการ Fine-tune เป็นงานจำแนกประเภทเอนทิตีระดับคำ (Token-level Classification) ตามมาตรฐาน BIO Tagging Scheme:
* **`B-PER` / `I-PER`:** Beginning / Inside Person Name (ชื่อบุคคล)
* **`B-ORG` / `I-ORG`:** Beginning / Inside Organization Name (ชื่อองค์กร)
* **`B-LOC` / `I-LOC`:** Beginning / Inside Location Name (ชื่อสถานที่)
* **`O`:** Outside Entity (คำทั่วไป)

**กระบวนการ Fine-Tuning ใน PyTorch:**
1. Worker โหลด Base Architecture `bert-base-cased` จาก Hugging Face Transformers
2. ดาวน์โหลด `conll2003_train.json` จาก MinIO บักเก็ต `datasets` ผ่านคำสั่ง `MinIOService.download_file_bytes()`
3. คำนวณ Loss Function ด้วย **CrossEntropyLoss** บน Logits ของแต่ละ Token ร่วมกับ **AdamW Optimizer**
4. ประเมินผลประสิทธิภาพโมเดลด้วยค่า **Token Accuracy** และ **F1-Score** (ใช้ไลบรารี `seqeval`)

### 4.3 โครงสร้างการตั้งชื่อโมเดลและ Log ใน MinIO Object Storage
เมื่อฝึกโมเดลเสร็จสิ้น Worker จะทำการแพ็กไฟล์ค่าน้ำหนักโมเดล (`pytorch_model.bin` / `model.safetensors`, `config.json`, `tokenizer.json`) บีบอัดเป็นไฟล์ Tarball และอัปโหลดไปยัง MinIO:
* **ชื่อไฟล์โมเดลไบนารีใน MinIO:** บักเก็ต `models` ➔ `model_{job_id}_{base_model}.tar.gz`  
  *(ตัวอย่าง: `model_job_001_bert_base_cased.tar.gz`)*
* **ชื่อไฟล์ Log ใน MinIO:** บักเก็ต `models` ➔ `logs/training_{job_id}.log`  
  *(ตัวอย่าง: `logs/training_job_001.log`)*

### 4.4 ระบบ Fault Tolerance & Error Handling
หากการเทรนเกิดข้อผิดพลาด (เช่น MinIO ขัดข้อง หรือ CUDA Out Of Memory - OOM) ระบบจะ Catch Exception บันทึก Stack Trace ลงไฟล์ Log อัปโหลดขึ้น MinIO เพื่อให้นักพัฒนาสามารถเข้ามาตรวจสอบย้อนหลังได้ทันที

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

1. **Hugging Face.** (2024). *Token Classification Course (Chapter 7: Named Entity Recognition)*. Retrieved from https://huggingface.co/learn/llm-course/en/chapter7/2
2. **PyTorch Development Team.** (2024). *PyTorch Documentation & GPU CUDA Acceleration*. Retrieved from https://pytorch.org/docs/
3. **Redis Ltd.** (2024). *Redis Commands: ZADD, ZRANGEBYSCORE and Atomic Queue Patterns*. Retrieved from https://redis.io/commands/zadd/
4. **MinIO Inc.** (2024). *MinIO Python Client SDK & S3 Compatible Object Storage Reference*. Retrieved from https://min.io/docs/minio/linux/developers/python/API.html
5. **NVIDIA Corporation.** (2024). *NVIDIA Container Toolkit Documentation for Docker GPU Acceleration*. Retrieved from https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
