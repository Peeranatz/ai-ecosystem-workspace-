# Presentation Layer Routers (`app/routers/`)

> **HTTP Request Handling & API Endpoints Gateway Layer**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/routers/`)

โฟลเดอร์ `routers/` ทำหน้าที่เป็น **Presentation Layer** หรือด่านหน้ารับ-ส่งข้อมูลผ่านโปรโตคอล **HTTP RESTful API** โดยแยกจุดเชื่อมต่อ API ออกเป็น 6 โมดูลหลักผ่าน `APIRouter()` ของ FastAPI คอยรับ HTTP Request, ตรวจสอบ Schema, เรียกใช้ Service คำนวณตรรกะ และคาย HTTP Status Code คืนกลับไปหาผู้ใช้งาน

---

## 📁 รายละเอียดโมดูลจุดเชื่อมต่อ API (Domain Endpoints Breakdown)

| ชื่อไฟล์ Router | Domain Tag | รายการ Endpoints ที่ให้บริการ |
| :--- | :--- | :--- |
| **`auth_router.py`** | `1. Authentication Domain` | `POST /api/v1/auth/register`<br>`POST /api/v1/auth/login`<br>`GET /api/v1/auth/me` |
| **`dataset_router.py`** | `2. Dataset Management Domain` | `POST /api/v1/datasets/upload`<br>`GET /api/v1/datasets`<br>`GET /api/v1/datasets/{dataset_id}` |
| **`model_router.py`** | `3. Model Registry Domain` | `POST /api/v1/models/upload`<br>`GET /api/v1/models`<br>`GET /api/v1/models/latest`<br>`GET /api/v1/models/{model_id}` |
| **`training_router.py`** | `4. Async Training Domain` | `POST /api/v1/training/start` (`202 Accepted`)<br>`GET /api/v1/training/status/{job_id}`<br>`POST /api/v1/training/cancel/{job_id}` |
| **`predict_router.py`** | `5. Inference Domain` | `POST /api/v1/predict` (Low-latency Inference) |
| **`label_studio_router.py`** | `6. Label Studio Domain` | `GET /api/v1/ls/projects`<br>`POST /api/v1/ls/projects`<br>`POST /api/v1/ls/tasks/import`<br>`GET /api/v1/ls/annotations/export` |
| **`system_router.py`** | `7. System Monitoring Domain` | `GET /api/v1/system/health`<br>`GET /api/v1/system/logs` |

---

## ⚠️ กฎเหล็กการเขียนโค้ดในชั้น Router
* **ห้ามเขียนคำสั่ง SQL** หรือเรียกต่อฐานข้อมูลตรงๆ ในไฟล์ Router
* **ห้ามคำนวณตรรกะทางธุรกิจซับซ้อน** ใน Router ให้ส่งผ่านไปให้ `services/` เป็นผู้คำนวณ
