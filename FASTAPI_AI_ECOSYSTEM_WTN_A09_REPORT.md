# รายงานการศึกษาและการประยุกต์ใช้งานเครื่องมือติดตามระบบ (Observability Tools for AI Ecosystem)
## รายงานประจำ Assignment 9 (WTN-A09)

**ข้อมูลผู้จัดทำ:**
* **ชื่อ-นามสกุล:** นายพีรณัฐ จุ้นฮก
* **รหัสนักศึกษา:** 6710110295
* **รายวิชา:** 241-353 AI Ecosystem Module (ASM09: Observability Tools)
* **GitHub Repository:** [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)

---

## 1. บทนำและวัตถุประสงค์ (Introduction & Objectives)

ระบบนิเวศของปัญญาประดิษฐ์ (AI Ecosystem) ยุคปัจจุบันประกอบด้วยบริการที่หลากหลายและทำงานแบบอะซิงโครนัส (Asynchronous Architecture) เช่น Web API Gateway, In-Memory Message Queues (Redis), Database Systems (PostgreSQL), Object Storage (MinIO), MLOps Tracking (MLflow), และ Background Inference Workers การซ่อมบำรุงและเฝ้าระบุปัญหาเมื่อระบบขัดข้องจึงจำเป็นต้องใช้ระบบ **Observability Stack** ที่ครอบคลุม Telemetry ทั้ง 3 เสาหลัก (Pillars of Observability): **Metrics**, **Logs**, และ **Traces**

**วัตถุประสงค์การทดลอง:**
1. เพื่อศึกษาเครื่องมือติดตามและคอยดูการทำงานของระบบ (Observability Tools) ใน AI Ecosystem
2. เพื่อติดตั้งและผสานรวมเครื่องมือ **OpenTelemetry (OTel)**, **Prometheus**, **Loki**, **Tempo**, และ **Grafana** เข้ากับโปรเจค AI Ecosystem
3. เพื่อวัดผลการทำงานจริงจากการเรียกใช้งาน NER Inference Worker ใน Assignment 8

---

## 2. Assignment Part 1: การศึกษาเครื่องมือ Observability ทั้ง 5 ตัว (Observability Tools Deep-Dive)

### 2.1 OpenTelemetry (OTel)
* **คืออะไร:** OpenTelemetry เป็น Open-source Vendor-neutral Framework ภายใต้ Cloud Native Computing Foundation (CNCF) ที่กำหนดมาตรฐาน API, SDK, และ Collector สำหรับการจัดเก็บข้อมูล Telemetry
* **ใช้สำหรับทำอะไร:** ทำหน้าที่เป็นตัวกลาง (Collector & Instrumentator) รวบรวมข้อมูล Traces, Metrics, และ Logs จากแอปพลิเคชัน จากนั้นแปลงรูปแบบให้อยู่ในมาตรฐาน OTLP (OpenTelemetry Protocol) แล้วส่งออก (Export) ไปยัง Backend ต่างๆ
* **ประโยชน์:** ป้องกันการยึดติดกับผู้ให้บริการรายใดรายหนึ่ง (No Vendor Lock-in), รวมศูนย์การจัดการข้อมูล Telemetry ไว้ที่จุดเดียว
* **ตัวอย่างการใช้งาน:** ใช้ OpenTelemetry Python SDK ดักจับระยะเวลาการทำงาน (Span Duration) ของฟังก์ชัน `execute_ner_inference()` ใน Inference Worker

### 2.2 Prometheus
* **คืออะไร:** Prometheus เป็นระบบติดตามและแจ้งเตือนข้อมูลเชิงอนุกรมเวลา (Time-Series Monitoring & Alerting Toolkit)
* **ใช้สำหรับทำอะไร:** คอยดึงข้อมูล (Scrape/Pull Model) ตัวเลขวัดผล (Metrics) จาก HTTP Endpoints เช่น `/metrics` หรือผ่าน OTel Collector
* **ประโยชน์:** รองรับภาษา PromQL สำหรับการคำนวณและสร้างกราฟประสิทธิภาพระบบ (เช่น CPU Usage, Request Count, Latency Percentiles)
* **ตัวอย่างการใช้งาน:** ติดตามจำนวนคำขอ `http_requests_total` และอัตราความสำเร็จของ FastAPI Web API

### 2.3 Loki (Grafana Loki)
* **คืออะไร:** Loki เป็นระบบจัดเก็บและรวบรวม Log (Log Aggregation System) ที่ออกแบบโดย Grafana Labs
* **ใช้สำหรับทำอะไร:** จัดเก็บไฟล์ Log จากคอนเทนเนอร์และแอปพลิเคชันโดยทำ Index เฉพาะ Labels (Metadata) ทำให้ประหยัดพื้นที่จัดเก็บข้อมูลอย่างมหาศาล
* **ประโยชน์:** สามารถค้นหา Log ร่วมกับ Metrics บน Grafana ผ่านภาษา LogQL ได้โดยไม่ต้องจัดทำ Index ข้อความทั้งหมดแบบ Elasticsearch
* **ตัวอย่างการใช้งาน:** รวมศูนย์ Log จาก Docker Containers และค้นหา Log ข้อผิดพลาดของ Inference Worker ผ่านคำสั่ง `{job="fastapi"}`

### 2.4 Tempo (Grafana Tempo)
* **คืออะไร:** Tempo เป็นระบบจัดเก็บการแกะรอยการทำงานแบบแจกจ่าย (High-scale Distributed Traces Backend)
* **ใช้สำหรับทำอะไร:** จัดเก็บข้อมูล Spans และ Trace IDs ที่ส่งมาจาก OpenTelemetry เพื่อติดตามลำดับการทำงานและคอขวด (Bottlenecks) ข้ามบริการ
* **ประโยชน์:** ใช้งานทรัพยากรน้อย ไม่ต้องการ Search Index ขนาดใหญ่ และเชื่อมโยง (Cross-link) กับ Loki และ Prometheus ได้ทันที
* **ตัวอย่างการใช้งาน:** ติดตาม Trace ID เดียวกันตั้งแต่ผู้ใช้ยิง API `POST /predict` ผ่าน FastAPI ไปจนถึง Inference Worker ดึงคิว Redis มาประมวลผล

### 2.5 Grafana
* **คืออะไร:** Grafana เป็นแพลตฟอร์มแสดงผลและสร้างแดชบอร์ดส่วนกลาง (Visualization & Analytics Dashboard Platform)
* **ใช้สำหรับทำอะไร:** สรุปและแสดงผลข้อมูลจาก Datasources หลากหลายประเภท (Prometheus, Loki, Tempo) ไว้บนแดชบอร์ดเดียว
* **ประโยชน์:** มีระบบแจ้งเตือน (Unified Alerting), ปรับแต่งหน้าจอค้นหา (Explore View) และวิเคราะห์ปัญหาในระบบได้อย่างรวดเร็ว
* **ตัวอย่างการใช้งาน:** แสดงผลกราฟ Metrics ความเร็วในการทำนายผล NER พร้อมตาราง Log และการคลิกดู Trace Waterfall Diagram ในหน้าจอเดียว

---

## 3. Assignment Part 2: การติดตั้งและการประยุกต์ใช้งานในโปรเจค (Implementation & Integration)

### 3.1 สถาปัตยกรรมและการสร้างบริการใน Docker Compose

ระบบถูกออกแบบให้มีคอนเทนเนอร์เพิ่มขึ้น 5 บริการหลักใน `compose.yml`:
1. `otel-collector` (otel/opentelemetry-collector-contrib:0.98.0) — พอร์ต `4317` (gRPC), `4318` (HTTP), `8889` (Metrics)
2. `prometheus` (prom/prometheus:v2.51.0) — พอร์ต `9090`
3. `loki` (grafana/loki:3.0.0) — พอร์ต `3100`
4. `tempo` (grafana/tempo:2.4.1) — พอร์ต `3200`
5. `grafana` (grafana/grafana:10.4.1) — พอร์ต `3000`

```yaml
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.98.0
    container_name: otel-collector
    ports:
      - "4317:4317"
      - "4318:4318"
      - "8889:8889"
      - "13133:13133"

  prometheus:
    image: prom/prometheus:v2.51.0
    ports:
      - "9090:9090"

  loki:
    image: grafana/loki:3.0.0
    ports:
      - "3100:3100"

  tempo:
    image: grafana/tempo:2.4.1
    ports:
      - "3200:3200"

  grafana:
    image: grafana/grafana:10.4.1
    ports:
      - "3000:3000"
```

### 3.2 การทำให้ Component ในโปรเจคใช้งาน Observability Stack

1. **FastAPI Backend Instrumentation:**
   * ติดตั้ง `opentelemetry-instrumentation-fastapi` และ `prometheus-fastapi-instrumentator`
   * เปิดใช้งาน OpenTelemetry Middleware และเปิดเผย Metrics Endpoint ที่ `/metrics`
2. **Inference Worker Instrumentation:**
   * สร้าง OpenTelemetry Tracer `inference_worker_service`
   * ใส่ Span Tracing ให้กับฟังก์ชัน `process_inference_job` และ `execute_ner_inference` พร้อมบันทึกพารามิเตอร์ `job.id`, `model.name`, `entities.count` และ `latency_ms`

---

## 4. ผลการทำงานและการทดสอบระบบ (System Screenshots & Visual Proof)

### 4.1 แผนภาพสถาปัตยกรรมระบบ Observability (System Architecture Diagram)
![แผนภาพสถาปัตยกรรมระบบ WTN-A09](backend/sandbox/screenshots/system_architecture_wtn_a09.png)
*รูปที่ 4.1: แผนภาพสถาปัตยกรรมระบบ Observability Stack (FastAPI, Inference Worker, OTel Collector, Prometheus, Loki, Tempo และ Grafana)*

---

### 4.2 หน้าต่าง Grafana Datasources Provisioning
![หน้าต่าง Grafana Data Sources](backend/sandbox/screenshots/screenshot_grafana_datasources_wtn_a09.png)
*รูปที่ 4.2: หน้าต่างตั้งค่า Connections ใน Grafana UI แสดงการตั้งค่า Datasources สำหรับ Prometheus, Loki และ Tempo อัตโนมัติ*

---

### 4.3 หน้าต่าง Prometheus Targets UI (`http://localhost:9090/targets`)
![หน้าต่าง Prometheus Targets](backend/sandbox/screenshots/screenshot_prometheus_ui_wtn_a09.png)
*รูปที่ 4.3: หน้าต่าง Prometheus Targets UI แสดงสถานะ UP สำหรับเป้าหมายดึง Metrics (fastapi host, otel-collector, prometheus)*

---

### 4.4 หน้าต่าง Grafana Metrics Explorer (Prometheus Metrics Query)
![หน้าต่าง Grafana Metrics Explorer](backend/sandbox/screenshots/screenshot_grafana_metrics_dashboard_wtn_a09.png)
*รูปที่ 4.4: หน้าต่าง Grafana Explore แสดงกราฟวัดผล Time-series Metrics จาก Prometheus*

---

### 4.5 หน้าต่าง Grafana Loki Log Explorer
![หน้าต่าง Grafana Loki Logs](backend/sandbox/screenshots/screenshot_grafana_loki_logs_wtn_a09.png)
*รูปที่ 4.5: หน้าต่าง Grafana Explore แสดงการค้นหา Log รวมศูนย์จาก Loki Engine*

---

### 4.6 หน้าต่าง Grafana Tempo Distributed Tracing
![หน้าต่าง Grafana Tempo Traces](backend/sandbox/screenshots/screenshot_grafana_tempo_traces_wtn_a09.png)
*รูปที่ 4.6: หน้าต่าง Grafana Explore แสดง Distributed Traces การทำงานของระบบผ่าน Tempo Engine*

---

### 4.7 ผลการทดสอบยิง API ทำนายผลและสร้าง Telemetry Data
![ผลการยิง API ใน Swagger UI](backend/sandbox/screenshots/screenshot_predict_api_telemetry_wtn_a09.png)
*รูปที่ 4.7: ผลการทดสอบยิง API สั่งทำนายผลข้อความ NER ผ่าน Swagger UI เพื่อส่งข้อมูล Telemetry ไปยังระบบ*

---

## 5. สรุปผลและลิงก์ตรวจสอบงาน (Conclusion & Source Code)

กระบวนการติดตั้งและทดสอบระบบ **Observability Stack (WTN-A09)** สำเร็จลุล่วงตามวัตถุประสงค์ ระบบสามารถดักจับ Metrics, Logs, และ Traces จากการทำงานของ FastAPI Web API และ Inference Worker ส่งผ่าน OpenTelemetry Collector ไปยัง Prometheus, Loki, และ Tempo และแสดงผลรวมกันบน Grafana UI ได้อย่างสมบูรณ์

* **GitHub Repository:** [https://github.com/Peeranatz/ai-ecosystem-workspace-.git](https://github.com/Peeranatz/ai-ecosystem-workspace-.git)
* **คำสั่งสำหรับการ Commit และ Push งานขึ้น GitHub:**
  ```bash
  git add .
  git commit -m "WTN-A09: Complete Observability Stack implementation (OpenTelemetry, Prometheus, Loki, Tempo, Grafana)"
  git push origin main
  ```
