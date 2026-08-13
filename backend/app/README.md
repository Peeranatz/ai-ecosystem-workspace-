# Application Package Directory (`app/`)

> **Core Production Application Source Code (Clean Architecture Baseline)**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/`)

โฟลเดอร์ `app/` เป็นศูนย์กลางซอร์สโค้ดหลักของเซิร์ฟเวอร์ **FastAPI Backend Application** ที่ถูกจัดโครงสร้างตามหลัก **Clean Architecture (Layered Design)** โดยแบ่งแยกความรับผิดชอบซอฟต์แวร์ออกเป็น 6 ชั้นโมดูล (Sub-modules) อย่างเป็นระเบียบ เพื่อให้โค้ดมีระดับ Low Coupling, High Cohesion และง่ายต่อการทดสอบและบำรุงรักษาระดับองค์กร

---

## 📁 โครงสร้างโมดูลภายในโฟลเดอร์ (`app/`)

```text
backend/app/
├── main.py            # Entry point หลักของ FastAPI App, CORS, Logging Middleware & Tag Metadata
├── core/              # โมดูลระบบความปลอดภัย (.env Loading, Bcrypt Hashing, JWT Tokens)
├── routers/           # Presentation Layer (API Endpoints ครบทั้ง 7 โดเมน)
├── schemas/           # Validation Layer (Pydantic Models สำหรับ In-Memory Request/Response)
├── services/          # Business Logic Layer (ตรรกะคำนวณทางธุรกิจ & Client SDK Wrappers)
├── models/            # Data Access Layer (SQLAlchemy ORM Entities นิยามตาราง DB)
└── utils/             # Helper Utilities (Custom Machine-Readable Structured JSON Logger)
```

---

## 🔄 สายธารการทำงานและทิศทางเรียกใช้งาน (Dependency Call Direction)

```text
[ HTTP Request ] ➔ routers/ ➔ schemas/ (Validate) ➔ services/ (Logic/SDK) ➔ models/ (ORM/DB)
```

1. **`routers/`** คอยรับ HTTP Request แล้วส่งข้อมูลผ่าน **`schemas/`** เพื่อตรวจสอบชนิดข้อมูล (Data Validation)
2. **`routers/`** เรียกใช้งาน **`services/`** เพื่อคำนวณตรรกะทางธุรกิจ ห้ามเขียน SQL ใน Router
3. **`services/`** เรียกใช้งาน **`models/`** (SQLAlchemy ORM) เพื่อส่งคำสั่ง SQL ไปยัง PostgreSQL หรือสตรีมไฟล์ไป MinIO / Redis Queue
4. **กฎเหล็ก:** ชั้นในสุด (`services/`, `models/`) จะไม่ย้อนกลับไปเรียกชั้นนอก (`routers/`) เด็ดขาด

---

## 💻 ตัวอย่างการรันเซิร์ฟเวอร์เบื้องต้น

```bash
cd backend
uv run uvicorn app.main:app --reload
```
เปิดดูหน้าเอกสาร **Swagger UI** ได้ที่: `http://127.0.0.1:8000/docs`
