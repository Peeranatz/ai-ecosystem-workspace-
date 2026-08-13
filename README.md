# 🚀 AI Ecosystem Web API Workspace (FastAPI)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)
![MinIO](https://img.shields.io/badge/MinIO-S3--Storage-C72C48?logo=minio)
![Redis](https://img.shields.io/badge/Redis-Task--Queue-DC382D?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Architecture](https://img.shields.io/badge/Architecture-Clean--Layered-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **Enterprise Clean Architecture Web API for AI Ecosystem Lifecycle (MLOps Platform)**  
> พัฒนาด้วย **FastAPI Framework, PostgreSQL 17, MinIO Object Storage, Redis Task Queue, Label Studio SDK** และ **Docker Compose**

---

## 👤 ข้อมูลผู้จัดทำ (Author)

* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: **6710110295**)
* **GitHub Repository:** [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

## 📋 สารบัญนำทางด่วน (Table of Contents)

- [📌 ภาพรวมและวัตถุประสงค์ของโปรเจกต์ (Project Overview)](#-ภาพรวมและวัตถุประสงค์ของโปรเจกต์-project-overview)
- [🏛️ สถาปัตยกรรมระบบ 4 ชั้น (4-Layer Clean Architecture Blueprint)](#-สถาปัตยกรรมระบบ-4-ชั้น-4-layer-clean-architecture-blueprint)
- [🔀 สายธารการไหลของข้อมูล (System Data Flow Scenarios)](#-สายธารการไหลของข้อมูล-system-data-flow-scenarios)
- [🗄️ ตารางการจัดสรรที่เก็บข้อมูล (Storage Isolation Matrix)](#-ตารางการจัดสรรที่เก็บข้อมูล-storage-isolation-matrix)
- [📂 ดัชนีคู่มือประจำโฟลเดอร์ย่อย (Subfolder Documentation Index)](#-ดัชนีคู่มือประจำโฟลเดอร์ย่อย-subfolder-documentation-index)
- [📊 ตารางรายการจุดเชื่อมต่อ API 7 โดเมนงาน (21 Endpoints API Snapshot)](#-ตารางรายการจุดเชื่อมต่อ-api-7-โดเมนงาน-21-endpoints-api-snapshot)
- [🪵 ระบบเฝ้าระวังและบันทึกประวัติ (Structured JSON Logging & Observability)](#-ระบบเฝ้าระวังและบันทึกประวัติ-structured-json-logging--observability)
- [⚙️ สคริปต์สกัด OpenAPI เป็น Excel และ CSV (Snapshot Converter Script)](#-สคริปต์สกัด-openapi-เป็น-excel-และ-csv-snapshot-converter-script)
- [⚡ ขั้นตอนการรันระบบเบื้องต้น (Quick Start & Installation Guide)](#-ขั้นตอนการรันระบบเบื้องต้น-quick-start--installation-guide)
- [🛡️ 5 เสาหลักการออกแบบระบบ (5 Architectural Pillars)](#️-5-เสาหลักการออกแบบระบบ-5-architectural-pillars)

---

## 📌 ภาพรวมและวัตถุประสงค์ของโปรเจกต์ (Project Overview)

โปรเจกต์นี้จัดทำขึ้นเพื่อออกแบบและพัฒนาระบบ **Enterprise Web API Server สำหรับรองรับวงจรชีวิต AI Ecosystem (WTN-A06)** โดยมุ่งเน้นการเปลี่ยนผ่านสภาพแวดล้อมทดลอง (Sandbox) มาสู่ **Production-Ready Clean Architecture Backend** 

ระบบครอบคลุมวงจรชีวิตการบริหารจัดการปัญญาประดิษฐ์ (MLOps Lifecycle) ตั้งแต่:
1. **Authentication & Authorization:** ระบบยืนยันตัวตนด้วย Stateless JWT Access Tokens และการ Hash รหัสผ่านด้วย Bcrypt
2. **Dataset Management:** สตรีมไฟล์ดิบขนาดใหญ่เก็บที่ MinIO S3 Object Storage และดรรชนี Metadata บน PostgreSQL 17
3. **Model Registry:** ระบบทะเบียนเวอร์ชันโมเดลตามหลัก **Append-Only Immutability Policy** (ป้องกันการ UPDATE เขียนทับเพื่อ Audit Trail)
4. **Asynchronous Training Queue:** ระบบคิวสั่งเทรนโมเดลแบบไม่บล็อกเซิร์ฟเวอร์ คืนค่า **`HTTP 202 Accepted`** ทันที แยกประมวลผลผ่าน **Time-Series Worker** (ตรวจจับอนาโมลี) และ **Non-Time-Series Worker** (ฝึก AI บน GPU)
5. **Data Annotation Integration:** เชื่อมต่อ **Label Studio SDK** สำหรับสร้างโครงการกำกับแท็กข้อมูล นำเข้า Dataset Tasks และส่งออก Labeled Annotations
6. **Low-Latency Inference:** ช่องทางทำนายผลความเร็วสูงระดับมิลลิวินาทีสำหรับแอปพลิเคชันภายนอก
7. **Observability & Monitoring:** บันทึก Log แบบ **Structured JSON Format** และระบบ Health Check PING ตรวจสุขภาพคอนเทนเนอร์

---

## 🏛️ สถาปัตยกรรมระบบ 4 ชั้น (4-Layer Clean Architecture Blueprint)

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

## 🔀 สายธารการไหลของข้อมูล (System Data Flow Scenarios)

### Scenario A: Low-Latency Inference Channel (`POST /api/v1/predict`)
```text
[ Client ] ──(1) POST /predict ──> [ FastAPI Router ] ──(2) Validate ──> [ Inference Service ]
                                                                                │
[ Client ] <──(4) Return JSON Prediction <──(3) Execute In-Memory Weights <─────┘
```

### Scenario B: Asynchronous Heavy Training Flow (`POST /api/v1/training/start`)
```text
[ Admin Client ] ──(1) POST /training/start ──> [ FastAPI Server ]
                                                      │
[ Admin Client ] <──(3) Return 202 Accepted + job_id ─┼──(2) Push Job ──> [ Redis Task Queue ]
       │                                              │                           │
       ▼ (Polling GET /training/status/{job_id})       │                           ▼
[ Status: RUNNING / COMPLETED ] <─────────────────────┴──────────── [ Background Worker (GPU) ]
```

---

## 🗄️ ตารางการจัดสรรที่เก็บข้อมูล (Storage Isolation Matrix)

เพื่อรับประกันประสิทธิภาพและระเบียบของระบบ เราแยกประเภทการจัดเก็บข้อมูลออกเป็น 3 เทคโนโลยีตามหน้าที่:

| เทคโนโลยีที่เก็บข้อมูล | พอร์ต (Port) | ประเภทข้อมูลที่จัดเก็บ (Data Type) | เหตุผลทางวิศวกรรม (Engineering Rationale) |
| :--- | :---: | :--- | :--- |
| **PostgreSQL 17** | `5433` | Structured Relational Data (Users, Metadata, Model Registry) | ต้องการ ACID Transactions, Data Integrity และการเชื่อมโยงความสัมพันธ์ (Foreign Keys) |
| **MinIO Storage** | `9000/9001` | Unstructured Binary Objects (Raw Datasets, `.pt` Model Weights) | เหมาะสำหรับเก็บไฟล์ไบนารีขนาดใหญ่ รองรับ S3 API และ Object Versioning |
| **Redis Server** | `6379` | In-Memory Key-Value & Task Queues (ARQ Broker) | อ่าน-เขียนรวดเร็วระดับ Microseconds เหมาะสำหรับเป็น Message Broker และ Cache |

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

## 📊 ตารางรายการจุดเชื่อมต่อ API 7 โดเมนงาน (21 Endpoints API Snapshot)

| โดเมนงาน (Domain Tag) | HTTP Verb | API Endpoint Path | Summary & Description | Parameters | Status Codes |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **1. Authentication** | `POST` | `/api/v1/auth/register` | สมัครสมาชิกใหม่ เข้ารหัส Password ด้วย Bcrypt | Request Body (username, email, password) | `201 Created` |
| | `POST` | `/api/v1/auth/login` | ตรวจสอบรหัสผ่าน ออก Stateless JWT Access Token | Request Body (username, password) | `200 OK` |
| | `GET` | `/api/v1/auth/me` | ดึงข้อมูลโปรไฟล์ผู้ใช้งานปัจจุบันที่ยืนยันตัวตนแล้ว | Header Authorization Bearer Token | `200 OK` |
| **2. Dataset Storage** | `POST` | `/api/v1/datasets/upload` | สตรีมไฟล์ดิบไป MinIO (`raw-datasets`) และบันทึก Metadata ลง PostgreSQL | Multipart Form File Upload | `201 Created` |
| | `GET` | `/api/v1/datasets` | ดูรายการชุดข้อมูลทั้งหมด รองรับ Pagination | Query (`skip`, `limit`) | `200 OK` |
| | `GET` | `/api/v1/datasets/{dataset_id}` | ดึงรายละเอียดชุดข้อมูลรายตัวตาม ID | Path (`dataset_id`) | `200 OK` |
| **3. Model Registry** | `POST` | `/api/v1/models/upload` | อัปโหลดและลงทะเบียนโมเดลเวอร์ชันใหม่แบบ Append-Only Log | Form Data (model_name, version, file) | `201 Created` |
| | `GET` | `/api/v1/models` | ดูประวัติประวัติเวอร์ชันโมเดลทั้งหมดในระบบ (Audit Trail) | Query (`model_name`) | `200 OK` |
| | `GET` | `/api/v1/models/latest` | ดึงไฟล์โมเดลเวอร์ชันล่าสุดที่เสถียรสำหรับนำไปทำนายผล | Query (`model_name`) | `200 OK` |
| | `GET` | `/api/v1/models/{model_id}` | ดึงรายละเอียดโมเดลตาม ID | Path (`model_id`) | `200 OK` |
| **4. Async Training** | `POST` | `/api/v1/training/start` | สั่งเริ่มฝึกโมเดล คืนค่า **`202 Accepted`** + `job_id` โยนงานเข้า Redis Queue | Request Body (model_name, dataset_id, epochs) | `202 Accepted` |
| | `GET` | `/api/v1/training/status/{job_id}` | ตรวจสอบสถานะและความคืบหน้าการฝึกโมเดล (Polling) | Path (`job_id`) | `200 OK` |
| | `POST` | `/api/v1/training/cancel/{job_id}` | ยกเลิกงานฝึกโมเดลในคิว | Path (`job_id`) | `200 OK` |
| **5. Inference** | `POST` | `/api/v1/predict` | ส่งข้อมูลเข้าประมวลผลทำนายผลความเร็วสูง (Low-latency Inference) | Request Body (input_data) | `200 OK` |
| **6. Label Studio** | `GET` | `/api/v1/ls/projects` | ดึงรายการโครงการกำกับแท็กข้อมูลจาก Label Studio SDK | None | `200 OK` |
| | `POST` | `/api/v1/ls/projects` | สร้างโครงการกำกับแท็กข้อมูลใหม่ใน Label Studio | Request Body (title, description) | `201 Created` |
| | `POST` | `/api/v1/ls/tasks/import` | นำเข้าชุดข้อมูลเพื่อเตรียมกำกับแท็กคำบรรยาย | Query (`project_id`), Body (tasks) | `200 OK` |
| | `GET` | `/api/v1/ls/annotations/export` | ส่งออกผลการกำกับแท็กข้อมูลนำไปฝึกโมเดล AI | Query (`project_id`, `export_format`) | `200 OK` |
| **7. Monitoring & Health** | `GET` | `/api/v1/system/health` | ตรวจเช็คสุขภาพการเชื่อมต่อ PING ไปยัง PostgreSQL, MinIO, Redis | None | `200 OK` / `503` |
| | `GET` | `/api/v1/system/logs` | เรียกดูประวัติ Log การทำงานรูปแบบ Structured JSON | None | `200 OK` |

---

## 🪵 ระบบเฝ้าระวังและบันทึกประวัติ (Structured JSON Logging & Observability)

ระบบได้รับการติดตั้ง Custom Interceptor Middleware เพื่อแปลง Log ทุกๆ HTTP Request ให้อยู่ในรูปแบบ **Machine-Readable Structured JSON Format**:

```json
{
  "timestamp": "2026-08-14T01:30:00.123456+00:00",
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

## ⚙️ สคริปต์สกัด OpenAPI เป็น Excel และ CSV (Snapshot Converter Script)

เพื่อให้สามารถทำ **Snapshot API List** สำหรับตรวจสอบ Audit และส่งสรุปเอกสาร ระบบพัฒนาสคริปต์ในไฟล์ `backend/scripts/export_openapi_excel.py`:

```bash
cd backend
uv run python scripts/export_openapi_excel.py
```

### ผลลัพธ์ที่ได้:
* 📄 **`backend/api_list_snapshot.xlsx`**: ไฟล์ Excel ปรับแต่งด้วย `openpyxl` มีส่วนหัวสีน้ำเงินเข้ม ไฮไลต์สีราย HTTP Verb (GET=เขียว, POST=ส้ม)
* 📄 **`backend/api_list_snapshot.csv`**: ไฟล์ CSV เข้ารหัส UTF-8-SIG รองรับภาษาไทย

---

## ⚡ ขั้นตอนการรันระบบเบื้องต้น (Quick Start & Installation Guide)

### Step 1: Clone Repository & Setup Environment
```bash
git clone https.github.com/Peeranatz/ai-ecosystem-workspace-.git
cd ai-ecosystem-workspace
```

### Step 2: Launch Backing Services with Docker Compose
```bash
docker compose up -d
```
*(คำสั่งนี้จะเริ่มต้นรัน PostgreSQL 17 [Port 5433], MinIO [Port 9000/9001], Redis [Port 6379], และ Label Studio [Port 8080])*

### Step 3: Run FastAPI Application Server
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Step 4: Access Interactive Documentation
* **Swagger UI:** 👉 **`http://127.0.0.1:8000/docs`**
* **ReDoc Manual:** 👉 **`http://127.0.0.1:8000/redoc`**
* **OpenAPI Spec JSON:** 👉 **`http://127.0.0.1:8000/api/v1/openapi.json`**
* **Health Check PING:** 👉 **`http://127.0.0.1:8000/api/v1/system/health`**

---

## 🛡️ 5 เสาหลักการออกแบบระบบ (5 Architectural Pillars)

1. **Separation of Concerns (การแบ่งแยกหน้าที่):** แยกชั้น Router, Service, Schema, และ Model ออกจากกันอย่างเด็ดขาด
2. **Dependency Injection (`Depends`):** ใช้ `Depends()` บริหารจัดการเปิด-ปิด DB Session และดักตรวจ JWT Token ป้องกัน Connection Leak
3. **Immutability Policy (ความไม่เปลี่ยนรูป):** บังคับใช้นโยบาย Append-Only สำหรับ Model Registry ห้ามใช้ SQL `UPDATE` แก้ทับ เพื่อรักษา Audit Trail
4. **Twelve-Factor App Methodology:** แยกค่าตั้งค่าความลับทั้งหมดออกไปเก็บในไฟล์ `.env`
5. **Structured JSON Logging:** บันทึก Log รูปแบบ JSON รองรับการทำ Observability ร่วมกับ Grafana Loki / ElasticSearch