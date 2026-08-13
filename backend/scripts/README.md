# Developer Automation Scripts (`scripts/`)

> **API List Snapshot & OpenAPI Export Utilities**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`scripts/`)

โฟลเดอร์ `scripts/` เก็บสคริปต์อัตโนมัติสำหรับการบริหารจัดการและสร้างเอกสารระบบ โดยไฟล์หลักคือ **`export_openapi_excel.py`** ซึ่งทำหน้าที่สกัดโครงสร้างจุดเชื่อมต่อ API ทั้งหมดจาก FastAPI (`openapi.json`) แปลงออกมาเป็นไฟล์ **Excel (`.xlsx`)** และ **CSV** สำหรับการทำ Snapshot API List ของระบบ

---

## 📁 สคริปต์แปลง `openapi.json` ➔ Excel/CSV (`export_openapi_excel.py`)

### การทำงานของสคริปต์:
1. นำเข้าแอปพลิเคชัน FastAPI จาก `app.main:app` แล้วสกัด **OpenAPI Schema Dictionary (`app.openapi()`)**
2. วนลูปอ่านรายการ API Endpoints ทั้งหมด ดึงข้อมูล: Tag/Domain, Path, HTTP Verb, Summary, Description, Parameters (Name, Location, Type, Required), และ Response Status Codes
3. ใช้ไลบรารี **`openpyxl`** สร้างไฟล์ Excel **`api_list_snapshot.xlsx`** พร้อมตกแต่งส่วนหัวสีน้ำเงินเข้ม ไฮไลต์สีตาม HTTP Verb (GET=เขียว, POST=ส้ม, DELETE=แดง) และจัดความกว้างคอลัมน์อัตโนมัติ
4. ส่งออกไฟล์ **`api_list_snapshot.csv`** ควบคู่กันไป

### วิธีการรันสคริปต์:
```bash
cd backend
uv run python scripts/export_openapi_excel.py
```

### ผลลัพธ์ที่ได้:
* `backend/api_list_snapshot.xlsx`
* `backend/api_list_snapshot.csv`
