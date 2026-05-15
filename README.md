# 🏆 AEGIS - Unified Intelligence Platform
**(All-source Earth Geospatial Intelligence System)**

AEGIS is a high-fidelity, open-source intelligence (OSINT) platform that unifies **WorldWideView**'s cinematic 3D globe with **ShadowBroker**'s massive 35+ real-time data layers. It adds a layer of **Predictive Intelligence** to forecast global events using rule-based heuristics derived from open data.

Built for analysts, researchers, and humanitarian responders, AEGIS provides a single intelligence surface where every public signal on Earth is visible in 3D.

---

## 🌟 Key Capabilities
- **🌍 Cinematic 3D Globe**: Powered by CesiumJS and Google Photorealistic 3D Tiles.
- **📡 35+ Data Layers**: Live tracking of aircraft (commercial/military), ships, satellites, earthquakes, wildfires, GDELT conflict events, and more.
- **🧠 Predictive Analytics**: Real-time forecasting for Conflict zones, Environmental crimes, and Supply Chain disruptions.
- **🆓 Free-Tier Only**: 100% free APIs. Zero credit card information required.
- **💻 Lightweight**: Optimized to run on a standard laptop (4GB RAM) with 60 FPS performance.
- **🛡️ Audit & Accountability**: Heuristic outcomes are tracked, scored for accuracy, and stored in a local SQLite database.

---

## 🛠️ Installation & Setup

Follow these steps to get AEGIS running on your machine.

### 1. Prerequisites
- **Docker** (Desktop or Engine)
- **Docker Compose** (V2 recommended, usually included with Docker Desktop)
- **Git**

### 2. Clone the Repository
```bash
git clone https://github.com/Jamesjaq/AEGIS.git
cd AEGIS
```

### 3. Configure Environment Variables (Optional but Recommended)
To unlock full global coverage for aircraft and ships, you should add your free API keys.
1. Copy the example environment file:
   ```bash
   cp shadowbroker/backend/.env.example shadowbroker/backend/.env
   ```
2. Edit `shadowbroker/backend/.env` and add your keys (e.g., `AIS_API_KEY`, `OPENSKY_CLIENT_ID`).
3. Refer to [**FREE_API_SETUP.md**](./FREE_API_SETUP.md) for direct links to get these keys for free.

### 4. Start AEGIS
Run the following command to build and start all services:
```bash
docker-compose up -d --build
```
*Note: If you have Docker Compose V2, you can also use `docker compose up -d --build`.*

### 5. Access the Platform
Once the containers are running, you can access the following:
- **AEGIS COMMAND (3D Globe)**: [http://localhost:3000](http://localhost:3000)
- **ShadowBroker Dashboard (2D Control)**: [http://localhost:3001](http://localhost:3001)
- **Unified API Health**: [http://localhost:8001/health](http://localhost:8001/health)

---

## 🧠 Intelligence Engines
AEGIS correlates data across multiple domains to provide early warnings:
- **Conflict Predictor**: Analyzes GDELT news trends, NASA thermal anomalies, and internet outages to flag regional instability.
- **Environmental Crime**: Detects suspicious vessel loitering in protected zones and critical drops in air quality.
- **Supply Chain Alerts**: Monitors maritime congestion, rail delays, and infrastructure status to warn of logistical bottlenecks.

## 🎬 Offline Demo Mode
No internet? No problem.
1. Open the 3D Globe at `http://localhost:3000`.
2. Open the **AEGIS COMMAND** sidebar on the left.
3. Click **"RUN OFFLINE DEMO"** to generate simulated OSINT telemetry for training and testing.

---

## 🏆 Award-Winning Technology
AEGIS is designed to be the most complete, accessible OSINT platform in the world. By using only free-tier APIs and standard hardware, it empowers users globally to monitor, analyze, and respond to critical world events.

---
*Created with ☕ and the belief that information should be free.* 🌍
