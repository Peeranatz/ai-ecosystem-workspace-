# AI Ecosystem Web API Workspace (FastAPI)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)
![MinIO](https://img.shields.io/badge/MinIO-S3--Storage-C72C48?logo=minio)
![Redis](https://img.shields.io/badge/Redis-Task--Queue-DC382D?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Architecture](https://img.shields.io/badge/Architecture-Clean--Layered-orange)

> **Enterprise Clean Architecture Web API for AI Ecosystem Lifecycle (MLOps)**  
> พัฒนาด้วย **FastAPI, PostgreSQL 17, MinIO Object Storage, Redis Task Queue** และ **Docker Compose**

---

## 👤 ผู้จัดทำโปรเจกต์ (Author)

* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: 6710110295)

---

## 📌 ภาพรวมและวัตถุประสงค์ของโปรเจกต์ (Project Overview)

โปรเจกต์นี้จัดทำขึ้นเพื่อออกแบบและพัฒนาระบบ **Web API ระดับองค์กรสำหรับรองรับระบบ AI Ecosystem** ที่ครอบคลุมวงจรชีวิตการบริหารจัดการปัญญาประดิษฐ์ (MLOps Lifecycle) ตั้งแต่การนำเข้าชุดข้อมูล, การฝึกฝนโมเดลแบบ Asynchronous, การลงทะเบียนเวอร์ชันโมเดล, การให้บริการทำนายผล (Inference) ความเร็วสูง, ไปจนถึงการเฝ้าระวังสุขภาพระบบและการจัดทำ Log แบบ Structured JSON Format

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
|  - Routers Layer (Endpoints)       |    |  - Job Workers              |
|  - Services Layer (Business Logic) |    |  - Training Workers (GPU)   |
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

### 🌟 5 เสาหลักการออกแบบระบบ (5 Architectural Pillars)

1. **Separation of Concerns (การแบ่งแยกหน้าที่):** ออกแบบระบบเป็น Layered Design แยกชั้น `routers/` (Presentation), `schemas/` (Validation), `services/` (Business Logic), และ `models/` (Data Access) ออกจากกันอย่างเด็ดขาด
2. **Dependency Injection (`Depends`):** ประยุกต์ใช้กลไก `Depends()` ของ FastAPI สำหรับการฉีดการเชื่อมต่อ Database Connection Session และการดักตรวจสอบสิทธิ์ JWT โดยระบบจะทำการคืนทรัพยากรให้อัตโนมัติเมื่อประมวลผลเสร็จสิ้น
3. **Immutability Policy (ความไม่เปลี่ยนรูปของข้อมูล):** บังคับใช้นโยบาย **Append-Only Log** สำหรับตารางทะเบียนโมเดล (`model_record`) โดยใช้วิธี `INSERT` สร้างเวอร์ชันใหม่เสมอ (`v1.0.0` ➔ `v1.1.0`) เพื่อรักษาร่องรอยการตรวจสอบ (Audit Trail) และสามารถย้อนกลับ (Rollback) ได้ 100%
4. **Twelve-Factor App Methodology:** ปฏิบัติตาม Config Factor (Factor III) แยกค่าตั้งค่า ข้อมูลฐานข้อมูล และ Secret Keys ออกจากโค้ดไปใส่ในไฟล์ **`.env`**
5. **Structured JSON Logging:** บันทึก Log การทำงานทั้งหมดของแอปพลิเคชันเป็นรูปแบบ **JSON Format** ที่มี Key-Value มาตรฐาน รองรับการนำ Log ไปวิเคราะห์และทำแดชบอร์ดเฝ้าระวังระบบร่วมกับ Grafana Loki หรือ ELK Stack

---

## 🔀 กระบวนการทำงานของข้อมูล (Data Flow Scenarios)

### Scenario A: การยิงขอผลทำนาย AI (Low-Latency Inference Flow)
```text
[ Client ] ---> POST /api/v1/predict (Input Data)
                  |
                  v
         [ predict_router ]
                  |
                  v
       [ inference_service ] ---> Load Weights from RAM / MinIO
                  |
                  v
  [ Client ] <--- Return JSON Prediction ({ label: "cat", confidence: 0.984 })
```

### Scenario B: การสั่งฝึกฝนโมเดล AI เบื้องหลัง (Asynchronous Heavy Training Flow)
```text
[ Admin Client ] ---> POST /api/v1/training/start
                         |
                         +---> (1) Save DB Status "PENDING"
                         +---> (2) Push Job Payload to Redis Task Queue
                         |
[ Admin Client ] <--- (3) Return HTTP 202 Accepted + job_id (Immediate Non-blocking)
       |
       v (Polling)
[ GET /api/v1/training/status/{job_id} ] <--- Check Progress Status
                                                    ^
                                                    |
                                      [ Background Training Worker ]
                                        - Pulls task from Redis
                                        - Downloads dataset from MinIO
                                        - Saves new weights (.pt) to MinIO
                                        - Updates DB status to "COMPLETED"
```

---

## 🗄️ ตารางเปรียบเทียบการจัดเก็บข้อมูล (Storage Isolation Matrix)

| เทคโนโลยี Storage | ชนิดข้อมูลที่จัดเก็บ (Data Type) | เหตุผลทางสถาปัตยกรรม (Architectural Rationale) |
| :--- | :--- | :--- |
| **PostgreSQL 17** (Port 5433) | Relational Data: Users, Dataset Metadata, Model Registry Records | ต้องการ ACID Compliance, Relational Integrity และการค้นหา Metadata ที่รวดเร็ว |
| **MinIO Storage** (Port 9000/9001) | Unstructured Large Files: Raw CSV/ZIP Datasets, PyTorch `.pt` Model Weights | ป้องกันไม่ให้ไฟล์ไบนารีขนาดใหญ่ส่งผลให้ฐานข้อมูลอืดบวม |
| **Redis Server** (Port 6379) | In-Memory Key-Value: Task Queue Payloads, RAM Caching Layer | ต้องการความเร็วอ่าน-เขียนระดับ Microsecond และการส่งงานคิวประมวลผลเบื้องหลัง |

---

## 📁 โครงสร้างโปรเจกต์ (Clean Architecture Directory Layout)

```text
ai-ecosystem-workspace/
├── compose.yml                # Docker Compose (PostgreSQL, MinIO, Redis, Label Studio)
├── README.md                  # เอกสารอธิบายโปรเจกต์
└── backend/
    ├── main.py                # Top-level Entry point (uvicorn runner)
    ├── pyproject.toml         # จัดการ Dependencies ด้วย uv (FastAPI, Uvicorn, SQLAlchemy, etc.)
    └── app/
        ├── main.py            # แอปพลิเคชันหลัก FastAPI, CORS & Logging Middleware
        ├── core/
        │   ├── config.py      # Pydantic BaseSettings สำหรับโหลดไฟล์ .env
        │   └── security.py    # Bcrypt Hashing & JWT Access Token Generator
        ├── routers/           # Presentation Layer (API Endpoints 6 กลุ่ม)
        │   ├── auth_router.py
        │   ├── dataset_router.py
        │   ├── model_router.py
        │   ├── training_router.py
        │   ├── predict_router.py
        │   └── system_router.py
        ├── schemas/           # Validation Layer (Pydantic Models)
        │   ├── auth_schema.py
        │   ├── dataset_schema.py
        │   ├── model_schema.py
        │   ├── training_schema.py
        │   └── system_schema.py
        ├── services/          # Business Logic Layer
        │   ├── auth_service.py
        │   ├── dataset_service.py
        │   ├── model_service.py
        │   ├── training_service.py
        │   └── inference_service.py
        ├── models/            # Data Access Layer (SQLAlchemy ORM Entities)
        │   ├── user_model.py
        │   ├── dataset_model.py
        │   └── model_record_model.py
        └── utils/
            └── logger.py      # Custom Structured JSON Logger
```

---

## 📡 รายละเอียด API ที่พึงมีใน AI Ecosystem (5 Domains API Specification)

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
| **5. Inference & Monitoring** | `POST` | `/api/v1/predict` | ส่งข้อมูลเข้าประมวลผลทำนายผลความเร็วสูง (Low-latency Inference) |
| | `GET` | `/api/v1/system/health` | ตรวจเช็คสุขภาพการเชื่อมต่อ PING ไปยัง PostgreSQL, MinIO, Redis |
| | `GET` | `/api/v1/system/logs` | เรียกดูประวัติ Log การทำงานรูปแบบ Structured JSON |

---

## 🪵 ตัวอย่าง Structured JSON Logging (System Logging Spec)

แอปพลิเคชันได้รับการติดตั้ง Middleware บันทึก Log การทำงานในรูปแบบ **Machine-Readable Structured JSON Format** สำหรับรองรับระบบ Observability:

```json
{
  "timestamp": "2026-07-30T18:47:58.357524+00:00",
  "system_name": "ai-ecosystem-backend",
  "log_level": "INFO",
  "message": "GET /docs - Status: 200 - 2.57ms",
  "module": "main",
  "filename": "main.py",
  "lineno": 41,
  "http_method": "GET",
  "endpoint": "/docs",
  "status_code": 200,
  "execution_time_ms": 2.57,
  "client_ip": "127.0.0.1"
}
```

---

## ⚡ วิธีการรันโปรเจกต์บนเครื่องตนเอง (Getting Started)

### 1. ติดตั้ง Backing Services ด้วย Docker Compose
```bash
docker compose up -d
```
*บริการที่รันขึ้นมา:*
* **PostgreSQL 17:** `localhost:5433`
* **MinIO Console:** `http://localhost:9001` (User: `minioadmin`, Pass: `minioadmin`)
* **Redis Server:** `localhost:6379`
* **Label Studio:** `http://localhost:8080`

### 2. รันแอปพลิเคชันเซิร์ฟเวอร์หลัก (FastAPI Backend)
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### 3. เข้าทดสอบ API ผ่าน Swagger UI
เปิดเว็บเบราว์เซอร์ไปที่: 👉 **`http://127.0.0.1:8000/docs`**