# Core System Module (`app/core/`)

> **Application Configuration & Security Infrastructure Layer**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/core/`)

โฟลเดอร์ `core/` ทำหน้าที่เป็นศูนย์กลางของ **ระบบการตั้งค่าสภาพแวดล้อม (Configuration Engine)** และ **ระบบรักษาความปลอดภัย (Security Infrastructure)** ของทั้งแอปพลิเคชัน โดยปฏิบัติตามหลักการ **12-Factor App Methodology (Factor III: Config)** แยกค่าความลับ พอร์ตการเชื่อมต่อฐานข้อมูล และ Secret Keys ทั้งหมดออกจากซอร์สโค้ดไปใส่ไว้ในไฟล์ `.env`

---

## 📁 รายละเอียดไฟล์ในโฟลเดอร์

| ชื่อไฟล์ | บทบาทและหน้าที่การทำงาน (Responsibility) |
| :--- | :--- |
| **`config.py`** | โหลดค่าคอนฟิกูเรชันจากไฟล์ `.env` ด้วย **Pydantic BaseSettings** เช่น พอร์ต PostgreSQL (5433), MinIO (9000/9001), Redis (6379), และ Secret Keys |
| **`security.py`** | ระบบความปลอดภัย: การเข้ารหัสและตรวจสอบ Password ด้วย **Bcrypt Hashing Algorithm** และการสร้าง **Stateless JWT Access Token** |

---

## 💻 ตัวอย่างการนำไปใช้งานในโปรเจกต์ (Developer Guide)

```python
# การดึงค่า Config ไปใช้งาน
from app.core.config import settings
print(settings.POSTGRES_HOST, settings.SECRET_KEY)

# การ Hash และตรวจสอบ Password
from app.core.security import get_password_hash, verify_password, create_access_token

hashed = get_password_hash("my_secret_password")
is_valid = verify_password("my_secret_password", hashed)
token = create_access_token(subject="sky_admin")
```
