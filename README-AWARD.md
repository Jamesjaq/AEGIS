# 🏆 AEGIS - The Award-Winning Unified Intelligence Platform

AEGIS is the ultimate fusion of **WorldWideView** and **ShadowBroker**, creating the most complete open-source intelligence (OSINT) platform available. Merging high-fidelity 3D visualization with real-time global telemetry and predictive intelligence.

## 🌟 Key Features

### 🌍 Unified 3D Globe
Every single one of the **35+ ShadowBroker data layers** is now rendered in stunning 3D using WorldWideView's Cesium-powered globe.
- **Google Photorealistic 3D Tiles**
- **Horizon Culling & Chunked Rendering** for 60 FPS performance with 5,000+ entities.
- **Visual Overlays**: FLIR (Thermal), NVG (Night Vision), and CRT (Retro) shaders for situational awareness.

### 🆓 "Free Like ShadowBroker" Philosophy
AEGIS is built for the world. It requires **zero credit card information** and uses 100% free or public API tiers.
- **Global Flights** via OpenSky Network
- **Maritime Traffic** via AIS Stream
- **Earthquakes, Fires, Satellites, and Conflict Zones** from public OSINT feeds.
- **Offline Demo Mode**: Proves reliability even in disconnected environments.

### 🧠 AEGIS Intelligence (Predictive Analytics)
We've added a predictive intelligence layer that analyzes real-time telemetry to forecast global events using lightweight heuristics (no heavy ML required):
1. **Conflict Prediction**: Analyzes GDELT events, NASA thermal anomalies, and internet outages to forecast regional instability (6h forecast).
2. **Environmental Crime**: Flags suspicious loitering in protected zones and critical air quality drops.
3. **Supply Chain Alerts**: Monitors vessel speeds, rail delays, and infrastructure status to warn of logistical bottlenecks.

### 📊 Accountability & Transparency
- **Rolling Accuracy Tracking**: The system validates its own predictions against real-world outcomes.
- **One-Click Export**: Empowering journalists and analysts with JSON evidence bundles and screenshots.
- **Audit Logs**: All intelligence alerts are stored in a local SQLite database for historical review.

## 🛠️ Components
- **ShadowBroker Backend**: High-frequency data fetchers for multi-domain OSINT.
- **Unified API (Bridge)**: Lightweight FastAPI service routing data and running intelligence heuristics.
- **AEGIS Predictors**: Rules-based intelligence engines with rolling accuracy tracking.
- **WorldWideView (HUD)**: The cinematic 3D frontend with a dedicated `shadow-bridge` plugin.

## 🚀 Quick Start
AEGIS is fully containerized and lightweight enough to run on a standard laptop (4GB RAM).

```bash
docker-compose up -d
```

Open `http://localhost:3000` to enter AEGIS COMMAND.

---
*AEGIS: Uniting the world's public signals into one intelligence surface.* 🏆
