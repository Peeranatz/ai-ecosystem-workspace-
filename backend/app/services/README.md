# Business Logic Layer & Component Services (`app/services/`)

> **Business Calculation Logic & Client SDK Wrapper Layer**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/services/`)

โฟลเดอร์ `services/` เป็น **สมองคำนวณหลักของแอปพลิเคชัน (Business Logic Layer)** คอยประมวลผลตรรกะทางธุรกิจอย่างแท้จริง รวมถึงการมัดรวม Client SDK Wrappers สำหรับเชื่อมต่อกับบริการเบื้องหลัง (MinIO, Label Studio, Redis Task Queue, Worker Tasks)

ชั้นนี้ถูกออกแบบให้เป็น **Framework-Agnostic** (ไม่ยึดติดกับ Web Framework) ทำให้สามารถถูกเรียกใช้โดย FastAPI Router, Background Worker, หรือ CLI Script ได้โดยไม่พัง

---

## 📁 รายละเอียดไฟล์โมเดลบริการ (Service Wrappers Breakdown)

| ชื่อไฟล์ Service | หน้าที่และการทำงาน (Functionality) |
| :--- | :--- |
| **`minio_service.py`** | **MinIO S3 SDK Client Wrapper:** จัดการสร้าง Bucket, สตรีมไฟล์ดิบอัปโหลด/ดาวน์โหลด, จัดการ Object Versioning Metadata และ Presigned URLs |
| **`label_studio_service.py`** | **Label Studio SDK Client Wrapper:** เชื่อมต่อ Label Studio API เพื่อสร้าง Annotation Projects, นำเข้า Dataset Tasks และส่งออก Labeled Annotations |
| **`worker_service.py`** | **ARQ Worker Service:** ประมวลผลงานเบื้องหลังแยกเป็น **Time-Series Worker** (ตรวจจับอนาโมลี/พาดหัว) และ **Non-Time-Series Worker** (ฝึกโมเดล AI บน GPU) |
| **`auth_service.py`** | ตรรกะการตรวจสอบสิทธิ์สมัครสมาชิก/เข้าสู่ระบบ และการออก JWT Token |
| **`dataset_service.py`** | ตรรกะการแยกจัดเก็บข้อมูล (Separation of Storage) สตรีมลง MinIO และเก็บบันทึก Metadata บน PostgreSQL |
| **`model_service.py`** | ตรรกะทะเบียนโมเดลตามหลัก **Append-Only Immutability Policy** (สร้างแถวใหม่เสมอเพื่อ Audit Trail & Rollback) |
| **`inference_service.py`** | ตรรกะการโหลดค่าน้ำหนักโมเดลจาก RAM Cache/MinIO เพื่อทำนายผลความเร็วสูง (Low-latency Inference) |
