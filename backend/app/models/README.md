# Data Access Layer Models (`app/models/`)

> **Relational Database Entities & SQLAlchemy ORM Schema Layer**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/models/`)

โฟลเดอร์ `models/` ทำหน้าที่เป็น **Data Access Layer** โดยใช้ออบเจกต์ **SQLAlchemy ORM** ในการนิยามตาราง คอลัมน์ และความสัมพันธ์ (Entities & Relationships) ของฐานข้อมูล **PostgreSQL 17** (Port 5433)

ชั้นนี้เป็นชั้นล่างสุดของสถาปัตยกรรม (Data Structure Level) ไม่มีการเรียกใช้ชั้นอื่นๆ และถูกเรียกใช้งานโดย `services/` เพียงฝั่งเดียวเท่านั้น

---

## 📁 รายละเอียดไฟล์ตารางฐานข้อมูล (SQLAlchemy ORM Entities)

| ชื่อไฟล์ Entity | ชื่อตารางใน PostgreSQL | คอลัมน์และข้อกำหนดทางสถาปัตยกรรม (Schema & Rationale) |
| :--- | :--- | :--- |
| **`user_model.py`** | `users` | `id`, `username`, `email`, `hashed_password`, `is_active`, `created_at` (เก็บข้อมูลสมาชิก) |
| **`dataset_model.py`** | `dataset_metadata` | `id`, `filename`, `file_size_bytes`, `minio_path`, `created_at` (เก็บเฉพาะ Metadata ของชุดข้อมูล) |
| **`model_record_model.py`** | `model_record` | `id`, `model_name`, `version`, `minio_path`, `metrics`, `created_at` (**Append-Only Log** ห้าม UPDATE เพื่อรักษาร่องรอยการตรวจสอบ Audit Trail) |
