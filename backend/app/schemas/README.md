# Data Validation Layer Schemas (`app/schemas/`)

> **In-Memory Request/Response Validation Layer via Pydantic V2**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/schemas/`)

โฟลเดอร์ `schemas/` ทำหน้าที่เป็น **Validation Layer** โดยใช้ออบเจกต์ **Pydantic V2 BaseModels** ในการนิยามสเปกและตรวจสอบความถูกต้องของข้อมูล (Data Validation & Serialization) ทั้งฝั่งอินพุตที่ยิงเข้ามาใน Request Payload และฝั่งเอาต์พุตที่จะตอบกลับเป็น HTTP Response

หากผู้ใช้งานยิงข้อมูลผิดชนิด Pydantic จะ Rejected คำสั่งและตอบกลับ HTTP Status `422 Unprocessable Entity` ให้อัตโนมัติโดยไม่ต้องเขียนโค้ด `if/else` เช็คเอง

---

## 📁 รายละเอียดไฟล์ในโฟลเดอร์

| ชื่อไฟล์ Schema | หน้าที่และการทำงาน (Functionality) |
| :--- | :--- |
| **`auth_schema.py`** | `RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserProfileResponse` |
| **`dataset_schema.py`** | `DatasetMetadataResponse` (ชื่อไฟล์, ขนาดไฟล์, minio_path, วันที่) |
| **`model_schema.py`** | `ModelRecordResponse` (ชื่อโมเดล, เวอร์ชัน Append-Only, metrics) |
| **`training_schema.py`** | `TrainingStartRequest`, `JobAcceptedResponse` (202 Accepted), `JobStatusResponse` |
| **`system_schema.py`** | `HealthCheckResponse` (PING Status PostgreSQL/MinIO/Redis), `PredictionRequest/Response` |
