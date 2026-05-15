import logging
from datetime import datetime
from database.manager import save_prediction

logger = logging.getLogger(__name__)

class SupplyChainPredictor:
    """
    Predicts supply chain disruptions using Vessel speeds, Train delays, and Infrastructure outages.
    """
    def __init__(self):
        self.type = "supply_chain"

    def analyze(self, vessel_data, train_data, outage_data):
        risk_score = 0
        evidence = []

        # 1. Maritime Congestion: Large clusters of ships with zero speed near ports
        if isinstance(vessel_data, list) and len(vessel_data) > 0:
            stationary_cargo = len([v for v in vessel_data if v.get('category') == 'cargo' and float(v.get('speed', 0)) < 0.5])
            if stationary_cargo > 20:
                risk_score += 30
                evidence.append(f"Major maritime congestion: {stationary_cargo} cargo ships stationary")

        # 2. Rail Delays
        if isinstance(train_data, list) and len(train_data) > 0:
            delayed_trains = len([t for t in train_data if t.get('delay', 0) > 60])
            if delayed_trains > 5:
                risk_score += 20
                evidence.append(f"Significant rail network delays detected ({delayed_trains} trains > 1h delay)")

        # 3. Power/Internet Outages at Hubs
        if isinstance(outage_data, list) and len(outage_data) > 0:
            critical_outages = len([o for o in outage_data if o.get('severity') == 'critical'])
            if critical_outages > 2:
                risk_score += 20
                evidence.append("Infrastructure outages at critical logistics hubs")

        risk_level = "HIGH" if risk_score > 50 else "MEDIUM" if risk_score > 25 else "LOW"
        confidence = min(0.95, 0.6 + (risk_score / 150))

        if risk_score > 15:
            save_prediction(self.type, risk_score, risk_level, confidence, evidence)

        return {
            "type": self.type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "evidence": evidence,
            "timestamp": datetime.utcnow().isoformat()
        }
