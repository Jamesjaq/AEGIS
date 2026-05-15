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

## 🛠️ How to Set It Up

AEGIS is fully containerized and easy to deploy.

### 1. Prerequisites
- **Docker** and **Docker Compose** installed.
- (Optional) Free API keys to unlock full global coverage (see [FREE_API_SETUP.md](./FREE_API_SETUP.md)).

### 2. Quick Start (1-Click)
Clone the repository and start all four services (ShadowBroker Backend, ShadowBroker Frontend, WorldWideView HUD, and Unified API):

```bash
git clone https://github.com/your-repo/aegis.git
cd aegis
docker-compose up -d
```

### 3. Accessing the HUD
- **AEGIS COMMAND (3D Globe)**: `http://localhost:3000`
- **ShadowBroker Dashboard (2D/Control)**: `http://localhost:3001`
- **Unified API Health**: `http://localhost:8001/health`

### 4. Configuration (API Keys)
To see real-time data for all layers, you need to provide free keys in the `.env` files.
- Copy `shadowbroker/backend/.env.example` to `shadowbroker/backend/.env` and fill in your keys.
- Refer to [**FREE_API_SETUP.md**](./FREE_API_SETUP.md) for direct links to get your free tokens for OpenSky, AIS Stream, NASA, etc.

---

## 🧠 Intelligence Engines
AEGIS goes beyond visualization by correlating data across domains:
- **Conflict Predictor**: Monitors GDELT news trends, NASA thermal anomalies, and internet outages to flag regional instability.
- **Environmental Crime**: Detects suspicious vessel loitering in protected zones and critical drops in air quality.
- **Supply Chain Alerts**: Analyzes maritime congestion, rail delays, and infrastructure status to warn of logistical bottlenecks.

---

## 🚀 Deployment Modes
- **Online**: Connects to live APIs for real-time situational awareness.
- **Offline/Demo**: Includes a built-in generator to simulate data flow for training or testing in disconnected environments.

---

## 🏆 Award-Ready
AEGIS is designed for the world's most prestigious open-source and humanitarian tech awards. It proves that sophisticated global intelligence can be built using only public goods, zero cost, and standard hardware.

---
*Created with ☕ and the belief that information should be free.* 🌍
