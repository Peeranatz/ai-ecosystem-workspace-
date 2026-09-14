# คู่มือสรุปเนื้อหาสำหรับเขียนรายงานด้วยมือ (Master Handwriting Guide)
## รายงาน WTN-A08: MLflow Tracking and Inference Worker Implementation

**ข้อมูลผู้จัดทำ:**
* **ชื่อ-นามสกุล:** นายพีรณัฐ จุ้นฮก
* **รหัสนักศึกษา:** 6710110295
* **GitHub Repository:** [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

> [!NOTE]
> **คำแนะนำสำหรับคุณสกาย:** คุณสกายสามารถคัดลอกข้อความในหัวข้อที่ 1 ถึง 5 ด้านล่างนี้ เขียนด้วยลายมือลงในกระดาษรายงานได้เลยครับ โดยในส่วนที่มีกรอบรูปภาพ ให้เว้นช่องสำหรับแปะรูป Screenshot ที่รันได้จริงตามที่ระบุไว้ครับ!

---

## 1. ทฤษฎีและการทำงานของ MLflow (MLflow Architecture & Features)

### 1.1 MLflow คืออะไร?
MLflow เป็น Open-source MLOps Platform ที่ออกแบบมาเพื่อบริหารจัดการวงจรชีวิตของ Machine Learning (ML Lifecycle) แบบครบวงจร ช่วยให้นักพัฒนาสามารถบันทึกผลการทดลอง (Experiment Tracking), จัดเก็บและเวอร์ชันโมเดล (Model Registry), บรรจุโมเดลเป็นแพ็กเกจมาตรฐาน (MLflow Models) และส่งมอบโมเดลไปใช้งานบน Production (Deployment) ได้อย่างมีประสิทธิภาพ

### 1.2 ฟีเจอร์หลักของ MLflow (Core Features)
1. **MLflow Tracking:** บันทึกและเปรียบเทียบ Parameters, Code Versions, Metrics (Loss, Accuracy, F1-Score) และ Artifacts จากการเทรนโมเดล
2. **MLflow Model Registry:** ระบบคลังเก็บโมเดลส่วนกลาง ช่วยในการจัดการเวอร์ชัน (Model Versioning), สถานะพายไลน์ (Staging, Production, Archived) และประวัติการเปลี่ยนแปลง
3. **MLflow Projects:** รูปแบบมาตรฐานในการแพ็กเกจโค้ด Machine Learning เพื่อให้สามารถรันซ้ำ (Reproducible Execution) ได้บนทุกสภาพแวดล้อม
4. **MLflow Models:** รูปแบบไฟล์และ API มาตรฐานสำหรับส่งออกโมเดลไปรัน Inference ผ่าน REST API หรือ Batch Processing

### 1.3 การทำงานร่วมกันระหว่าง MLflow, PostgreSQL และ MinIO Object Storage
สถาปัตยกรรม MLflow Tracking Server ถูกออกแบบแยกส่วนจัดเก็บข้อมูลเป็น 2 ส่วนสำคัญ (Decoupled Storage Architecture):
* **PostgreSQL (Backend Metadata Store):** ทำหน้าที่เป็น Database สำหรับเก็บบันทึกข้อมูลประเภท Metadata เช่น ชื่อ Experiment, Run ID, Parameters, Metrics, Tags และสถานะการเปลี่ยนเวอร์ชันใน Model Registry
* **MinIO Object Storage (Default Artifact Root - S3 Compatible):** ทำหน้าที่เป็น S3 Object Storage สำหรับเก็บไฟล์ไบนารีขนาดใหญ่ (Artifacts) ได้แก่ ค่าน้ำหนักโมเดล PyTorch (`.bin` / `.safetensors`), ไฟล์คอนฟิก (`config.json`), ไฟล์ Tokenizer (`tokenizer.json`) และไฟล์ Log การเทรน

---

## 2. การจัดเก็บผลการเทรนและการเรียกใช้งานโมเดล (Training Log & Model Retrieval)

### 2.1 MLflow เก็บผลการเทรนอย่างไร?
เมื่อ Trainer Worker เริ่มต้นกระบวนการ Fine-tuning โมเดล Token Classification (NER) ระบบจะสื่อสารกับ MLflow ผ่านคำสั่ง:
1. `mlflow.set_tracking_uri("http://mlflow:5000")` — กำหนด URL ของ MLflow Server
2. `mlflow.set_experiment("conll2003_ner")` — สร้างหรืออ้างอิงถึงชื่อ Experiment
3. `mlflow.start_run()` — บันทึกพารามิเตอร์ผ่าน `log_params()`, ค่า Loss/Accuracy ผ่าน `log_metric()` และไฟล์โมเดลผ่าน `log_model()`

### 2.2 การเรียกใช้โมเดล (Model Retrieval & Versioning)
MLflow ช่วยให้ Inference Worker สามารถดึงโมเดลมาทำนายผลได้อย่างยืดหยุ่น 2 รูปแบบ:
* **การเรียกใช้เวอร์ชันล่าสุด (Latest Version):** อ้างอิงผ่าน URI `models:/conll2003_ner/latest` หรือ Stage Tag `models:/conll2003_ner/Production` เพื่อให้ระบบนำโมเดลล่าสุดไปใช้โดยอัตโนมัติ
* **การเรียกใช้เวอร์ชันเฉพาะเจาะจง (Specific Version):** อ้างอิงผ่าน URI ระบุเลขเวอร์ชันตรงๆ เช่น `models:/conll2003_ner/1` หรือ `models:/conll2003_ner/2` ช่วยรองรับการย้อนกลับ (Rollback) หากโมเดลเวอร์ชันใหม่มีปัญหา

---

## 3. งานสร้าง Inference Workerและการเรียกใช้งานโมเดล (Inference Worker Architecture)

### 3.1 การสร้างและสถาปัตยกรรม Inference Worker
Inference Worker ถูกสร้างเป็น Container บริการแยก (`ai_inference_worker`) ทำหน้าที่เป็น Background Daemon:
1. **การโหลดโมเดล:** โหลดค่าน้ำหนักโมเดล Token Classification (NER) จาก MLflow Model Registry เข้าสู่ RAM/GPU Memory เมื่อเริ่มต้น Container
2. **การเฝ้ารับคิวงาน:** คอยฟังคิวคำขอทำนายผลจาก Redis List Queue (`inference_job_queue`) ผ่านคำสั่ง `BLPOP`
3. **การประมวลผล:** ดึงข้อความมาสกัดจำแนกเอนทิตี (Named Entity Recognition: PER, ORG, LOC) แล้วบันทึกผลลัพธ์ลง Redis Key `inference_result:{job_id}`

---

## 4. API สำหรับการเรียกใช้งานผ่าน FastAPI (Inference APIs)

FastAPI Server ให้บริการ 3 API Endpoints หลักสำหรับการทำนายผล:
1. `POST /api/v1/inference/predict` — รับ Payload ข้อความ ทำการ Enqueue ลงคิว Redis และคืนค่า `job_id` ทันที (Non-blocking Queue Pattern)
2. `GET /api/v1/inference/job/{job_id}` — ขอดูสถานะและผลลัพธ์การสกัดเอนทิตีจาก `job_id`
3. `GET /api/v1/inference/models` — ตรวจสอบรายชื่อโมเดลและเวอร์ชันทั้งหมดที่มีใน MLflow

---

## 5. ผลการทำงานและการทดสอบระบบ (System Screenshots & Visual Proof)

### 5.1 แผนภาพสถาปัตยกรรมระบบ (System Architecture Diagram)
![แผนภาพสถาปัตยกรรมระบบ WTN-A08 (FastAPI, Redis Queue, MLflow Server, PostgreSQL, MinIO และ Inference Worker)](backend/sandbox/screenshots/system_architecture_wtn_a08.png)
*รูปที่ 5.1: แผนภาพสถาปัตยกรรมระบบ WTN-A08*

---

### 5.2 ภาพแสดงหน้าต่าง MLflow Tracking UI (Experiments & Metrics)
![ภาพหน้าจอ MLflow Tracking UI (http://localhost:5000) แสดง Experiment conll2003_ner พารามิเตอร์ และกราฟ Metrics](backend/sandbox/screenshots/screenshot_mlflow_tracking_wtn_a08.png)
*รูปที่ 5.2: หน้าต่าง MLflow Tracking UI บันทึกผลการทดลองการเทรนโมเดล conll2003_ner พร้อมค่า Loss, Accuracy และ F1-Score*

---

### 5.3 ภาพแสดงหน้าต่าง MLflow Model Registry
![ภาพหน้าจอ MLflow Model Registry แสดงโมเดล conll2003_ner และ Version 1](backend/sandbox/screenshots/screenshot_mlflow_registry_wtn_a08.png)
*รูปที่ 5.3: คลังโมเดลส่วนกลาง (Model Registry) ใน MLflow จัดเก็บโมเดลเวอร์ชันล่าสุดที่พร้อมนำไปใช้งานบน Inference Worker*

---

### 5.4 ภาพแสดงไฟล์ Artifacts ใน MinIO Console (`s3://mlflow/`)
![ภาพหน้าจอ MinIO Console (http://localhost:9001) บักเก็ต mlflow](backend/sandbox/screenshots/screenshot_minio_mlflow_wtn_a08.png)
*รูปที่ 5.4: ไฟล์ค่าน้ำหนักโมเดลไบนารีและ Artifacts ที่ถูก MLflow นำมาบันทึกใน MinIO Object Storage บักเก็ต mlflow*

---

### 5.5 ภาพผลลัพธ์การยิง API `/predict` ผ่าน Swagger UI
![ผลลัพธ์การยิง API POST /api/v1/inference/predict ได้รับ job_id](backend/sandbox/screenshots/screenshot_predict_api_wtn_a08.png)
*รูปที่ 5.5: การยิง API สั่งทำนายผลข้อความ ได้รับ job_id กลับมาสำหรับการติดตามผล*

---

### 5.6 ภาพผลลัพธ์การขอดูผลการทำงานจาก `job_id` ผ่าน Swagger UI
![ผลลัพธ์การยิง API GET /api/v1/inference/job/{job_id} แสดงเอนทิตี PER, ORG, LOC](backend/sandbox/screenshots/screenshot_job_result_api_wtn_a08.png)
*รูปที่ 5.6: ผลลัพธ์การสกัด Named Entities (องค์กร บุคคล สถานที่) ที่ได้จากการประมวลผลของ Inference Worker*

---

### 5.7 ภาพ Log การทำงานของ Inference Worker สด
![Log การทำงานสดของ Inference Worker ผ่าน Terminal](backend/sandbox/screenshots/screenshot_inference_worker_logs_wtn_a08.png)
*รูปที่ 5.7: Log การดึงคิวจาก Redis และการประมวลผลทำนายผลโมเดลสดของ Inference Worker*

---

## 6. คำสั่งสำหรับการ Commit งานขึ้น GitHub Project

```bash
git add .
git commit -m "WTN-A08: Complete MLflow Tracking Server, Inference Worker, and Prediction APIs implementation"
git push origin main
```
