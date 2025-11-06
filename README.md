#  IoT Dashboard (Python + Django + PostgreSQL + MQTT)

A beginner-friendly IoT backend project that receives data from devices through **MQTT**, stores it in a **PostgreSQL** database, and provides clean **REST APIs** using **Django REST Framework**.

---

##  Features
- Real-time data collection via MQTT
- REST APIs for devices and telemetry
- PostgreSQL database integration
- Swagger API documentation
- Django Admin panel for data management
- Simple fake device publisher (Python script)

---

##  Tech Stack
**Backend:** Python, Django, Django REST Framework  
**Database:** PostgreSQL  
**Messaging:** MQTT (Broker: test.mosquitto.org)  
**Documentation:** Swagger (drf-spectacular)  
**Tools:** Postman, VS Code  

---

## ⚙️ Setup Guide (Windows)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Tanishapamecha/iot-dashboard.git
cd iot-dashboard
2️⃣ Create virtual environment & install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
3️⃣ Create .env file in project root
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=iotdb
DB_USER=iotuser
DB_PASS=iotpass
MQTT_BROKER=test.mosquitto.org
MQTT_PORT=1883

4️⃣ Run migrations & create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

5️⃣ Start Django server
python manage.py runserver

6️⃣ Start MQTT worker (in new terminal)
python mqtt_worker.py

7️⃣ Start fake publisher (to simulate IoT data)
python tools\publisher.py


** API Endpoints**
 http://127.0.0.1:8000/api/docs/
Method	Endpoint	Description
GET	/api/devices/	List all devices
GET	/api/telemetry/	All telemetry data
GET	/api/devices/{device_id}/telemetry	Device-specific data
POST	/api/alerts/	Create an alert


** Django Admin**
Login to manage data manually:
 http://127.0.0.1:8000/admin/
Admin lets you view:
Devices
Telemetry (temperature, humidity, battery)
Alerts


📸 Screenshots

1. Swagger API Docs
2.Admin Dashboard

 Future Enhancements
Real-time WebSocket dashboard
Docker + Redis integration
Frontend using React or HTMX
Device-based alerts

👩‍💻 Author

Tanisha Pamecha
Python Backend Developer
https://github.com/Tanishapamecha/iot-dashboard/new/main?filename=README.md
https://www.linkedin.com/in/tanisha-pamecha-421a6626b/
