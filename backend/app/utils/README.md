# Utilities Module (`app/utils/`)

> **Application Utility Helpers & Observability Logging Layer**

---

## 📌 บทบาทและหน้าที่ของโฟลเดอร์ (`app/utils/`)

โฟลเดอร์ `utils/` เก็บไฟล์เครื่องมือช่วยเหลือ (Helper Utilities) ส่วนกลางของแอปพลิเคชัน โดยไฟล์หลักคือ **`logger.py`** ซึ่งทำหน้าที่สร้างระบบบันทึกประวัติการทำงานแบบ **Machine-Readable Structured JSON Logging** ตามมาตรฐานความพร้อมของระบบระดับองค์กร (Observability Requirement)

---

## 📁 รายละเอียดระบบ Logging (`logger.py`)

* **รูปแบบ Log:** แปลงข้อความ Plaintext ทั่วไปให้เป็น **JSON Format** แบบ Key-Value
* **ฟิลด์มาตรฐาน:** `timestamp`, `system_name`, `log_level`, `message`, `module`, `filename`, `lineno`, `http_method`, `endpoint`, `status_code`, `execution_time_ms`, `client_ip`
* **ประโยชน์:** ระบบ Log Aggregator ระดับ Enterprise เช่น **Grafana Loki** หรือ **ElasticSearch** สามารถ Parse และ Index ฟิลด์ไปวิเคราะห์และสร้างแดชบอร์ดแจ้งเตือนภัยล่วงหน้าได้ทันที

```json
{
  "timestamp": "2026-08-14T01:00:00.123Z",
  "system_name": "ai-ecosystem-backend",
  "log_level": "INFO",
  "message": "GET /docs - Status: 200 - 2.57ms",
  "endpoint": "/docs",
  "status_code": 200,
  "execution_time_ms": 2.57
}
```
