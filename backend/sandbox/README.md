# Developer Sandbox & Proof-of-Concept Tests (`sandbox/`)

> **Experimental Environment for Component Prototyping & Testing**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`sandbox/`)

โฟลเดอร์ `sandbox/` เป็นสภาพแวดล้อมทดลองและพิสูจน์แนวคิด (Proof of Concept: PoC) สำหรับให้นักพัฒนาทดลองติดตั้งและยิงคำสั่งทดสอบไลบรารีต่าง ๆ (MinIO SDK, Label Studio SDK, PostgreSQL SQLAlchemy, ARQ Workers, Custom Logger) ก่อนที่จะถูก Refactor ย้ายโค้ดเข้าสู่ Production-Ready Application ภายใต้โฟลเดอร์ `app/services/`

---

## 📁 สรุปไฟล์ทดสอบและโฟลเดอร์ย่อย

| ชื่อไฟล์ / โฟลเดอร์ | หน้าที่และการทดสอบ (Testing Purpose) |
| :--- | :--- |
| **`minio/upload_download.py`** | สคริปต์ทดสอบการเชื่อมต่อ MinIO S3 SDK, การสร้าง Bucket และอัปโหลด/ดาวน์โหลดไฟล์ |
| **`minio/versioning_test.py`** | สคริปต์ทดสอบระบบ Object Versioning บน MinIO สำหรับระบบทะเบียนโมเดล |
| **`test_logger.py`** | สคริปต์ทดสอบระบบ Structured JSON Logging |
| **`test_settings.py`** | สคริปต์ทดสอบการอ่านค่า `.env` ผ่าน Pydantic Settings |
| **`screenshots/`** | โฟลเดอร์เก็บภาพหลักฐานแคปเจอร์หน้าจอการรันระบบจริง |
| **`slide_images/`** | โฟลเดอร์เก็บรูปภาพไดอะแกรมจากสไลด์นำเสนอ |
