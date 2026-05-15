from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import os
import asyncio
import logging
from typing import List, Dict, Any
from database.manager import init_db, get_predictions
from ingestors.bridge_logic import ShadowBrokerBridge, FreeDataIngestor
from predictors.conflict import RealConflictPredictor
from predictors.environment import EnvironmentalCrimePredictor
from predictors.supply_chain import SupplyChainPredictor
from learning.accuracy import AccuracyTracker

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aegis-bridge")

app = FastAPI(title="AEGIS Unified API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ShadowBroker Backend URL
SB_BACKEND_URL = os.getenv("SB_BACKEND_URL", "http://localhost:8000")
bridge = ShadowBrokerBridge(SB_BACKEND_URL)
free_ingestor = FreeDataIngestor()

# Initialize Predictors
conflict_predictor = RealConflictPredictor()
env_predictor = EnvironmentalCrimePredictor()
supply_predictor = SupplyChainPredictor()
accuracy_tracker = AccuracyTracker()

@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("AEGIS Unified API Started")
    # Start background analysis loop
    asyncio.create_task(analysis_loop())

async def analysis_loop():
    """
    Periodic background task to run predictors on fresh data.
    """
    while True:
        try:
            logger.info("Starting intelligence analysis cycle...")
            # Fetch slow tier data for analysis
            sb_data = await bridge.fetch_shadowbroker_data(tier="slow")
            if "error" in sb_data:
                sb_data = await free_ingestor.get_all_free_data()

            # Run Predictors
            conflict_predictor.analyze(
                sb_data.get("gdelt", []),
                sb_data.get("firms_fires", []),
                sb_data.get("internet_outages", [])
            )

            env_predictor.analyze(
                sb_data.get("fishing_activity", []),
                sb_data.get("air_quality", []),
                sb_data.get("ships", [])
            )

            supply_predictor.analyze(
                sb_data.get("ships", []),
                sb_data.get("trains", []),
                sb_data.get("internet_outages", [])
            )

            logger.info("Analysis cycle complete.")
        except Exception as e:
            logger.error(f"Predictor cycle failed: {e}")

        # Run every 10 minutes
        await asyncio.sleep(600)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "aegis-unified-api"}

@app.get("/api/stream")
async def get_unified_stream():
    """
    Unified endpoint for WorldWideView shadow-bridge plugin.
    Combines ShadowBroker data with Unified Intelligence alerts.
    """
    # Fetch fast data from ShadowBroker
    sb_data = await bridge.fetch_shadowbroker_data(tier="fast")

    # Fallback to direct free APIs if ShadowBroker returns error
    if "error" in sb_data:
        sb_data = await free_ingestor.get_all_free_data()

    # Transform to WWV format
    entities = bridge.transform_to_geoentities(sb_data)

    # Fetch intelligence alerts
    predictions = get_predictions(limit=20)

    return {
        "entities": entities,
        "intelligence": predictions,
        "accuracy": accuracy_tracker.get_accuracy_report(),
        "metadata": {
            "source": "shadowbroker-unified",
            "timestamp": asyncio.get_event_loop().time()
        }
    }

@app.get("/api/predictions")
async def predictions():
    return get_predictions()

@app.get("/api/accuracy")
async def accuracy():
    return accuracy_tracker.get_accuracy_report()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
