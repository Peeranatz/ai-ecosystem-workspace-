# Backend Service Architecture (`backend/`)

> **FastAPI Enterprise Backend Server & Subfolder Developer Guide**

---

## 📌 บทบาทและหน้าที่ของไดเรกทอรี (`backend/`)

ไดเรกทอรี `backend/` เป็นศูนย์กลางการพัฒนาและรันเซิร์ฟเวอร์หลักของระบบ **AI Ecosystem Enterprise Web API Platform** ที่มัดรวมแอปพลิเคชัน Clean Architecture, สภาพแวดล้อมทดลอง (Sandbox), สคริปต์อัตโนมัติ (Scripts), และระบบคอนฟิกูเรชันเข้าด้วยกัน

---

## 📁 สารบัญคู่มือพัฒนาประจำโฟลเดอร์ย่อย (Subfolder Developer Guides)

เพื่อให้การพัฒนาระบบมีความเป็นระเบียบและตรงตามสเปกงาน **WTN-A06** ในแต่ละ Subfolder สำคัญจะมีไฟล์ `README.md` ประจำโฟลเดอร์สำหรับอธิบายรายละเอียดการใช้งาน ดังนี้:

* 📘 **[app/README.md](app/README.md)**: คู่มือแอปพลิเคชันหลักและทิศทางการเรียกใช้งาน Clean Architecture
* 📘 **[app/core/README.md](app/core/README.md)**: คู่มือระบบความปลอดภัย, การโหลด `.env` และการออก JWT Tokens
* 📘 **[app/routers/README.md](app/routers/README.md)**: รายละเอียด API Endpoints ทั้ง 7 โดเมนงาน
* 📘 **[app/schemas/README.md](app/schemas/README.md)**: สเปก Pydantic Request/Response Validation Schemas
* 📘 **[app/services/README.md](app/services/README.md)**: ตรรกะคำนวณทางธุรกิจ และ Client SDK Services (MinIO, Label Studio, Worker)
* 📘 **[app/models/README.md](app/models/README.md)**: รายละเอียดตารางฐานข้อมูล PostgreSQL (SQLAlchemy ORM Entities)
* 📘 **[app/utils/README.md](app/utils/README.md)**: คู่มือการใช้งาน Structured JSON Logger
* 📘 **[sandbox/README.md](sandbox/README.md)**: โฟลเดอร์ทดลองและทดสอบไลบรารีเบื้องหลัง (Proof of Concept)
* 📘 **[scripts/README.md](scripts/README.md)**: สคริปต์แปลง `openapi.json` เป็นไฟล์ Excel (`.xlsx`) และ CSV

---

## ⚡ วิธีการรันเซิร์ฟเวอร์หลักและสคริปต์ Snapshot

### 1. รัน FastAPI Backend Server
```bash
cd backend
uv run uvicorn app.main:app --reload
```
เปิดดูหน้าเอกสาร **Swagger UI** ที่: `http://127.0.0.1:8000/docs`

### 2. รันสคริปต์ Snapshot API List ➔ Excel / CSV
```bash
uv run python scripts/export_openapi_excel.py
```
ผลลัพธ์จะถูกส่งออกเป็นไฟล์ `api_list_snapshot.xlsx` และ `api_list_snapshot.csv`
