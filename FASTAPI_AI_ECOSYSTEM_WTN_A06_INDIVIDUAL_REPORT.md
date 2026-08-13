# รายงานสถาปัตยกรรมและการออกแบบ API List (WTN-A06)

**ข้อมูลผู้จัดทำ (Individual Author):**
* **นายพีรณัฐ จุ้นฮก** (รหัสนักศึกษา: 6710110295)

**ลิงก์ GitHub Remote Repository:**  
👉 [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

## 1. วัตถุประสงค์และการดำเนินงานโครงการ (WTN-A06 Objectives)

การดำเนินงานในโครงการ **WTN-A06: Project - Lib Installations - API List** มีวัตถุประสงค์หลักในการเปลี่ยนผ่านสภาพแวดล้อมทดลองทางความคิด (Sandbox Environment) มาสู่ **Production-Ready AI Ecosystem Backend Server** ที่จัดวางโครงสร้างอย่างเป็นระเบียบตามหลัก **Clean Architecture (Layered Design)** 

การพัฒนาระบบครั้งนี้ครอบคลุมการเชื่อมต่อโครงสร้างพื้นฐานระดับองค์กร ได้แก่ **PostgreSQL 17** (Relational Metadata Storage), **MinIO** (S3-Compatible Object Storage), **Redis 6379** (In-Memory Message Broker & Task Queue), และ **Label Studio** (Data Annotation Platform) พร้อมทั้งการย้ายตรรกะประมวลผลมาเป็น Production Services ใน `app/services/` การรองรับงานประมวลผลทั้งแบบ Time-Series และ Non-Time-Series Workers การปรับแต่ง Metadata ของเอกสาร API และการสร้างสคริปต์ส่งออก API List Snapshot เป็นไฟล์ **Excel (`.xlsx`)** และ **CSV**

---

## 2. โครงสร้างระบบและไฟล์ในไดเรกทอรี (Directory Structure & Subfolder READMEs)

เพื่อให้การบำรุงรักษาระบบซอฟต์แวร์เป็นไปตามสเปกงาน WTN-A06 ทุกๆ โฟลเดอร์หลักและโฟลเดอร์ย่อย (Subfolders) ในระบบ จะมีไฟล์ **`README.md` ประจำโฟลเดอร์** เพื่อกำกับหน้าที่การทำงาน (Developer Responsibilities) ไร้ปัญหาการเดาโครงสร้างโค้ด:

```text
ai-ecosystem-workspace/
├── compose.yml                # Docker Compose (PostgreSQL, MinIO, Redis, Label Studio)
├── README.md                  # เอกสารอธิบายโปรเจกต์และดัชนี Subfolder Documentation
└── backend/
    ├── README.md              # [Subfolder Docs 1] สรุปบริการ Backend และดัชนีคู่มือย่อย
    ├── pyproject.toml         # จัดการ Dependencies ด้วย uv (FastAPI, SQLAlchemy, MinIO, openpyxl, etc.)
    ├── api_list_snapshot.xlsx # ไฟล์ Snapshot API List รูปแบบ Excel
    ├── api_list_snapshot.csv  # ไฟล์ Snapshot API List รูปแบบ CSV
    ├── scripts/
    │   ├── README.md          # [Subfolder Docs 2] คู่มือสคริปต์แปลง openapi.json -> Excel/CSV
    │   ├── export_openapi_excel.py # สคริปต์แปลง OpenAPI เป็น Excel (.xlsx) และ CSV
    │   └── capture_report_screenshots.py # สคริปต์จับภาพหน้าจอระบบอัตโนมัติ
    ├── sandbox/
    │   ├── README.md          # [Subfolder Docs 3] คู่มือสภาพแวดล้อมทดลอง PoC Scripts
    │   ├── screenshots/       # รูปภาพหลักฐานการรันระบบจริง
    │   └── slide_images/      # รูปภาพแผนผังสถาปัตยกรรมระบบ
    └── app/
        ├── README.md          # [Subfolder Docs 4] สถาปัตยกรรม Clean Architecture & Call Flow
        ├── main.py            # แอปหลัก FastAPI, CORS, Logging Middleware & Tag Metadata
        ├── core/
        │   ├── README.md      # [Subfolder Docs 5] คู่มือระบบความปลอดภัย (.env Loading & JWT)
        │   ├── config.py      # Pydantic BaseSettings สำหรับโหลดไฟล์ .env
        │   └── security.py    # Bcrypt Hashing & JWT Access Token Generator
        ├── routers/           # Presentation Layer (API Endpoints ครบทั้ง 7 โดเมน)
        │   ├── README.md      # [Subfolder Docs 6] รายละเอียด API Endpoints 7 โดเมน
        │   ├── auth_router.py
        │   ├── dataset_router.py
        │   ├── model_router.py
        │   ├── training_router.py
        │   ├── predict_router.py
        │   ├── label_studio_router.py
        │   └── system_router.py
        ├── schemas/           # Validation Layer (Pydantic Models)
        │   ├── README.md      # [Subfolder Docs 7] Pydantic Request/Response Schemas
        │   ├── auth_schema.py
        │   ├── dataset_schema.py
        │   ├── model_schema.py
        │   ├── training_schema.py
        │   └── system_schema.py
        ├── services/          # Business Logic Layer & Component SDK Wrappers
        │   ├── README.md      # [Subfolder Docs 8] ตรรกะธุรกิจ & Client SDK Services
        │   ├── auth_service.py
        │   ├── dataset_service.py
        │   ├── model_service.py
        │   ├── training_service.py
        │   ├── inference_service.py
        │   ├── minio_service.py # Production MinIO S3 SDK Client Wrapper
        │   ├── label_studio_service.py # Production Label Studio SDK Client Wrapper
        │   └── worker_service.py # Time-Series & Non-Time-Series Background Workers
        ├── models/            # Data Access Layer (SQLAlchemy ORM Entities)
        │   ├── README.md      # [Subfolder Docs 9] ตารางฐานข้อมูล PostgreSQL ORM
        │   ├── user_model.py
        │   ├── dataset_model.py
        │   └── model_record_model.py
        └── utils/
            ├── README.md      # [Subfolder Docs 10] คู่มือ Structured JSON Logger
            └── logger.py      # Custom Machine-Readable Structured JSON Logger
```

---

## 3. เทคโนโลยีและ Infrastructure Stack (Docker Compose Setup)

ระบบได้รับการตั้งค่าการรันบริการส่วนหลังผ่านไฟล์ **`compose.yml`** เพื่อแยกการทำงานของที่จัดเก็บข้อมูลออกเป็นส่วนๆ (Storage Isolation Pattern):

| Service Name | Container Image | Port Mapping | Role & Functionality |
| :--- | :--- | :---: | :--- |
| **`postgres`** | `postgres:17-alpine` | `5433:5432` | Relational DB สำหรับจัดเก็บ Users, Metadata และ Model Registry |
| **`minio`** | `minio/minio:latest` | `9000:9000`<br>`9001:9001` | S3-Compatible Object Storage สำหรับไฟล์ดิบ (.zip, Datasets) และไฟล์โมเดล (.pt) |
| **`redis`** | `redis:alpine` | `6379:6379` | In-Memory Message Broker และ Task Queue สำหรับ ARQ Background Workers |
| **`label-studio`** | `heartexlabs/label-studio:latest` | `8080:8080` | Data Annotation & Labeling Platform สำหรับเตรียมข้อมูลฝึกโมเดล AI |

---

## 4. การออกแบบและเชื่อมต่อ Component ต่างๆ (Services & Workers Integration)

![แผนผังสถาปัตยกรรมระบบแบบรายละเอียด](backend/sandbox/slide_images/slide_12.png)

1. **`minio_service.py` (MinIO S3 SDK Client):**
   * บูรณาการการเชื่อมต่อ MinIO S3 API เพื่อบริหารจัดการ Bucket, สตรีมไฟล์ดิบอัปโหลด/ดาวน์โหลด, การตรวจสอบ Object Versioning และการออก Presigned Temporary URLs
2. **`label_studio_service.py` (Label Studio SDK Client):**
   * บูรณาการการเชื่อมต่อ Label Studio SDK สำหรับสร้าง Annotation Projects, นำเข้าชุดข้อมูล (`import_tasks`) และส่งออกผลการกำกับแท็กข้อมูล (`export_annotations`) เพื่อนำไปฝึกโมเดล
3. **`worker_service.py` (Background Worker Component):**
   * **Time-Series Worker:** รองรับการประมวลผลข้อมูลสตรีมเซ็นเซอร์ การตรวจจับอนาโมลี (Anomaly Detection) และการพาดหัวแนวโน้มอนาคต (Forecasting)
   * **Non-Time-Series Worker:** รองรับการฝึกโมเดล AI ภาพ/ข้อความ การประมวลผลข้อมูลภาพถ่าย และการบันทึกค่าน้ำหนักโมเดล (.pt) ไปยัง MinIO

---

## 5. รายการ Backend APIs ที่เปิดใช้งานจริง (Live API List Snapshot Table)

รายการจุดเชื่อมต่อ API ที่ลงทะเบียนและเปิดใช้งานจริงทั้ง 21 Endpoints แบ่งตาม 7 โดเมนงาน:

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
| **7. System Monitoring** | `GET` | `/api/v1/system/health` | ตรวจเช็คสุขภาพการเชื่อมต่อ PING ไปยัง PostgreSQL, MinIO, Redis | None | `200 OK` / `503` |
| | `GET` | `/api/v1/system/logs` | เรียกดูประวัติ Log การทำงานรูปแบบ Structured JSON | None | `200 OK` |

---

## 6. ระบบสกัด OpenAPI Spec เป็น CSV / Excel (Snapshot Export Utility)

สคริปต์ **`backend/scripts/export_openapi_excel.py`** ทำหน้าที่ดึงโครงสร้าง OpenAPI Schema (`/api/v1/openapi.json`) จากแอปพลิเคชัน FastAPI นำมาสกัดรายละเอียด และสร้างไฟล์ Snapshot ตาราง API ออกมา 2 รูปแบบไว้บริเวณ Root Directory ของ Backend:

1. **`api_list_snapshot.csv`**: ไฟล์ CSV เข้ารหัส UTF-8-SIG รองรับการอ่านภาษาไทยได้อย่างถูกต้อง
2. **`api_list_snapshot.xlsx`**: ไฟล์ Excel ปรับแต่งด้วยไลบรารี `openpyxl` ใส่สีส่วนหัว ปรับฟอนต์ Segoe UI ไฮไลต์สีราย HTTP Verb (GET=สีเขียว, POST=สีส้ม, DELETE=สีแดง) และจัดความกว้างคอลัมน์ให้อ่านง่ายโดยอัตโนมัติ

---

## 7. ภาพประกอบผลการทำงานของระบบ (System Visual Evidence)

### 7.1 ภาพหน้าจอ Interactive Swagger UI (`http://localhost:8000/docs`)
![หน้าต่าง Interactive Swagger UI](backend/sandbox/screenshots/screenshot_swagger_ui.png)
* **คำอธิบาย:** แสดงหน้าต่างอินเทอร์เฟซ Swagger UI ผ่าน URL `http://localhost:8000/docs` แสดงหมวดหมู่ Endpoints ทั้ง 7 โดเมนงาน พร้อมคำอธิบาย Tag Metadata ชัดเจน
* **ประโยชน์:** ใช้เป็นอินเทอร์เฟซสำหรับนักพัฒนาในการทดลองยิงขอ API (Interactive Testing) แบบ Real-time

### 7.2 ภาพหน้าจอ ReDoc Documentation (`http://localhost:8000/redoc`)
![หน้าต่าง ReDoc Documentation](backend/sandbox/screenshots/screenshot_redoc_ui.png)
* **คำอธิบาย:** แสดงหน้าเอกสาร ReDoc ผ่าน URL `http://localhost:8000/redoc` ในรูปแบบ Clean & Read-only Documentation พร้อมเมนูนอนทางฝั่งซ้าย
* **ประโยชน์:** ใช้เป็นคู่มืออ้างอิงสเปก API มาตรฐานสำหรับนักพัฒนาระบบภายนอกและทีมร่วมพัฒนา

### 7.3 ภาพหน้าจอ OpenAPI Specification JSON (`http://localhost:8000/api/v1/openapi.json`)
![หน้าต่าง OpenAPI Specification JSON](backend/sandbox/screenshots/screenshot_openapi_json.png)
* **คำอธิบาย:** แสดงผลลัพธ์โครงสร้าง JSON สเปกมาตรฐาน OpenAPI v3.1.0 ที่เซิร์ฟเวอร์สร้างขึ้นจาก Type Hints
* **ประโยชน์:** ใช้สำหรับการ Import เข้าสู่ซอฟต์แวร์ทดสอบ เช่น Postman, Insomnia หรือเครื่องมือสร้าง Client Code แบบอัตโนมัติ

### 7.4 ภาพหน้าจอ Health Check Response (`http://localhost:8000/api/v1/system/health`)
![หน้าต่าง Health Check Response](backend/sandbox/screenshots/screenshot_health_check.png)
* **คำอธิบาย:** ผลลัพธ์การตรวจสอบสุขภาพระบบผ่าน Endpoint `/api/v1/system/health`
* **ประโยชน์:** ใช้ทดสอบสถานะ PING การเชื่อมต่อระหว่าง FastAPI กับ PostgreSQL, MinIO, และ Redis

### 7.5 ภาพหน้าจอไฟล์ Snapshot `api_list_snapshot.xlsx` ที่ถูกสร้างขึ้นจริง
![ภาพหน้าจอไฟล์ Snapshot api_list_snapshot.xlsx](backend/sandbox/screenshots/screenshot_excel_snapshot.png)
* **คำอธิบาย:** ผลลัพธ์การสกัดรายการ API จากระบบสด ออกมาเป็นไฟล์สเปรดชีต Excel ตกแต่งสีจัดตารางสวยงาม
* **ประโยชน์:** สำหรับใช้อ้างอิงการ Audit แบบ Offline หรือส่งสรุปรายการ API ให้ผู้บริหาร/อาจารย์ตรวจประเมิน

---

## 8. เอกสารอ้างอิง (Academic References)

1. **Ramírez, S. (Tiangolo).** (2023). *FastAPI Documentation: Metadata and Docs URLs*. Retrieved from https://fastapi.tiangolo.com/tutorial/metadata/
2. **Martin, R. C.** (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
3. **Fowler, M.** (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
4. **Wiggins, A.** (2017). *The Twelve-Factor App Methodology*. Retrieved from https://12factor.net/
5. **Kreps, J.** (2014). *I Heart Logs: Event-Data, Stream Processing, and Big Data*. O'Reilly Media.
