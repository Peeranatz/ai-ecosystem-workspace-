# AI Ecosystem Web API Workspace (FastAPI)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)
![MinIO](https://img.shields.io/badge/MinIO-S3--Storage-C72C48?logo=minio)
![Redis](https://img.shields.io/badge/Redis-Task--Queue-DC382D?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Architecture](https://img.shields.io/badge/Architecture-Clean--Layered-orange)

> **Enterprise Clean Architecture Web API for AI Ecosystem Lifecycle (MLOps)**  
> พัฒนาด้วย **FastAPI, PostgreSQL 17, MinIO Object Storage, Redis Task Queue, Label Studio SDK** และ **Docker Compose**

---

## 👤 ผู้จัดทำโปรเจกต์ (Author)

* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: 6710110295)

---

## 📌 ภาพรวมและวัตถุประสงค์ของโปรเจกต์ (Project Overview)

โปรเจกต์นี้จัดทำขึ้นเพื่อออกแบบและพัฒนาระบบ **Web API ระดับองค์กรสำหรับรองรับระบบ AI Ecosystem (WTN-A06)** ที่ครอบคลุมวงจรชีวิตการบริหารจัดการปัญญาประดิษฐ์ (MLOps Lifecycle) ตั้งแต่การนำเข้าชุดข้อมูล, การฝึกฝนโมเดลแบบ Asynchronous ทั้งแบบ Time-Series และ Non-Time-Series Workers, การกำกับแท็กข้อมูลด้วย Label Studio SDK, การลงทะเบียนเวอร์ชันโมเดล, การให้บริการทำนายผล (Inference) ความเร็วสูง, ไปจนถึงการเฝ้าระวังสุขภาพระบบและการจัดทำ Log แบบ Structured JSON Format

---

## 📂 ดัชนีคู่มือประจำโฟลเดอร์ย่อย (Subfolder Documentation Index)

ตามข้อกำหนดของงาน **WTN-A06** ในทุกๆ Subfolder สำคัญของระบบ ได้รับการจัดทำไฟล์ `README.md` ประจำโฟลเดอร์สำหรับอธิบายรายละเอียดการทำงานและไกด์สำหรับนักพัฒนา:

* 📘 **[backend/README.md](backend/README.md)**: ภาพรวมบริการ Backend ทั้งหมด
* 📘 **[backend/app/README.md](backend/app/README.md)**: สถาปัตยกรรม Clean Architecture และทิศทางเรียกใช้โค้ด
* 📘 **[backend/app/core/README.md](backend/app/core/README.md)**: ระบบคอนฟิกูเรชัน `.env` และการออก JWT Tokens
* 📘 **[backend/app/routers/README.md](backend/app/routers/README.md)**: จุดเชื่อมต่อ API ทั้ง 7 โดเมนงาน
* 📘 **[backend/app/schemas/README.md](backend/app/schemas/README.md)**: Pydantic Validation Schemas
* 📘 **[backend/app/services/README.md](backend/app/services/README.md)**: ตรรกะธุรกิจ และ SDK Client Services (MinIO, Label Studio, Worker)
* 📘 **[backend/app/models/README.md](backend/app/models/README.md)**: ตารางฐานข้อมูล PostgreSQL (SQLAlchemy ORM)
* 📘 **[backend/app/utils/README.md](backend/app/utils/README.md)**: ระบบ Structured JSON Logger
* 📘 **[backend/sandbox/README.md](backend/sandbox/README.md)**: สภาพแวดล้อมทดลองและ PoC Scripts
* 📘 **[backend/scripts/README.md](backend/scripts/README.md)**: สคริปต์แปลง `openapi.json` ➔ Excel/CSV (`export_openapi_excel.py`)

---

## 🏛️ สถาปัตยกรรมระบบและหลักการออกแบบ (Architecture Blueprint)

```text
+-----------------------------------------------------------------------+
|                             USERS LAYER                               |
|        [ End Users (Inference) ]      [ Admins (Management) ]         |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                         GATEWAY LAYER (FastAPI)                       |
|   - Authentication & Authorization (JWT)                              |
|   - Rate Limiting & Security Inspection                               |
|   - Request Routing & Schema Validation (Pydantic)                    |
+-----------------------------------------------------------------------+
            |                                               |
            v (Sync HTTP)                                   v (Async Queue)
+------------------------------------+    +-----------------------------+
|    CENTRAL FASTAPI SERVER LAYER    |    |  BACKGROUND WORKERS LAYER   |
|  - Routers Layer (Endpoints)       |    |  - Time-Series Worker       |
|  - Services Layer (Business Logic) |    |  - Non-Time-Series Worker   |
|  - Models Layer (SQLAlchemy ORM)   |    +-----------------------------+
+------------------------------------+                  |
            |                                           |
            v                                           v
+-----------------------------------------------------------------------+
|                         STORAGE & DATA LAYER                          |
|  - PostgreSQL 17 (Metadata/Users)  - Redis (Task Queue/Cache)        |
|  - MinIO Object Storage (Datasets/Model Weights)                      |
|  - External Tools (Label Studio Data Annotation)                      |
+-----------------------------------------------------------------------+
```

---

## 📊 รายละเอียด API Snapshot (7 Domains Specification)

| โดเมนงาน (Domain) | HTTP Verb | API Endpoint | หน้าที่และการทำงาน (Functionality) |
| :--- | :---: | :--- | :--- |
| **1. Authentication** | `POST` | `/api/v1/auth/register` | สมัครสมาชิกใหม่ เข้ารหัส Password ด้วย Bcrypt |
| | `POST` | `/api/v1/auth/login` | ตรวจสอบรหัสผ่าน ออก Stateless JWT Access Token |
| | `GET` | `/api/v1/auth/me` | ดึงข้อมูลโปรไฟล์ผู้ใช้งานปัจจุบันที่ยืนยันตัวตนแล้ว |
| **2. Dataset Storage** | `POST` | `/api/v1/datasets/upload` | สตรีมไฟล์ดิบไป MinIO (`raw-datasets`) และบันทึก Metadata ลง PostgreSQL |
| | `GET` | `/api/v1/datasets` | ดูรายการชุดข้อมูลทั้งหมด รองรับ Pagination (`skip/limit`) |
| | `GET` | `/api/v1/datasets/{dataset_id}` | ดึงรายละเอียดชุดข้อมูลรายตัวตาม ID |
| **3. Model Registry** | `POST` | `/api/v1/models/upload` | อัปโหลดและลงทะเบียนโมเดลเวอร์ชันใหม่แบบ Append-Only Log |
| | `GET` | `/api/v1/models` | ดูประวัติประวัติเวอร์ชันโมเดลทั้งหมดในระบบ (Audit Trail) |
| | `GET` | `/api/v1/models/latest` | ดึงไฟล์โมเดลเวอร์ชันล่าสุดที่เสถียรสำหรับนำไปทำนายผล |
| | `GET` | `/api/v1/models/{model_id}` | ดึงรายละเอียดโมเดลตาม ID |
| **4. Async Training** | `POST` | `/api/v1/training/start` | สั่งเริ่มฝึกโมเดล คืนค่า **`202 Accepted`** + `job_id` โยนงานเข้า Redis Queue |
| | `GET` | `/api/v1/training/status/{job_id}` | ตรวจสอบสถานะและความคืบหน้าการฝึกโมเดล (Polling) |
| | `POST` | `/api/v1/training/cancel/{job_id}` | ยกเลิกงานฝึกโมเดลในคิว |
| **5. Inference** | `POST` | `/api/v1/predict` | ส่งข้อมูลเข้าประมวลผลทำนายผลความเร็วสูง (Low-latency Inference) |
| **6. Label Studio** | `GET` | `/api/v1/ls/projects` | ดึงรายการโครงการกำกับแท็กข้อมูลจาก Label Studio SDK |
| | `POST` | `/api/v1/ls/projects` | สร้างโครงการกำกับแท็กข้อมูลใหม่ใน Label Studio |
| | `POST` | `/api/v1/ls/tasks/import` | นำเข้าชุดข้อมูลเพื่อเตรียมกำกับแท็กคำบรรยาย |
| | `GET` | `/api/v1/ls/annotations/export` | ส่งออกผลการกำกับแท็กข้อมูลนำไปฝึกโมเดล AI |
| **7. Monitoring & Health** | `GET` | `/api/v1/system/health` | ตรวจเช็คสุขภาพการเชื่อมต่อ PING ไปยัง PostgreSQL, MinIO, Redis |
| | `GET` | `/api/v1/system/logs` | เรียกดูประวัติ Log การทำงานรูปแบบ Structured JSON |

---

## ⚡ วิธีการรันโปรเจกต์และสคริปต์ส่งออก Excel/CSV

### 1. ติดตั้ง Backing Services ด้วย Docker Compose
```bash
docker compose up -d
```

### 2. รันแอปพลิเคชันเซิร์ฟเวอร์หลัก (FastAPI Backend)
```bash
cd backend
uv run uvicorn app.main:app --reload
```
เปิดดูหน้าเอกสาร **Swagger UI** ได้ที่: 👉 **`http://127.0.0.1:8000/docs`**

### 3. รันสคริปต์สกัด API List เป็นไฟล์ Excel (`.xlsx`) และ CSV
```bash
cd backend
uv run python scripts/export_openapi_excel.py
```
ผลลัพธ์จะสร้างไฟล์ `api_list_snapshot.xlsx` และ `api_list_snapshot.csv` ในโฟลเดอร์ `backend/` ทันที!