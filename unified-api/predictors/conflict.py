import logging
from datetime import datetime
from database.manager import save_prediction

logger = logging.getLogger(__name__)

class RealConflictPredictor:
    """
    Predicts potential conflict based on GDELT, FIRMS Fires, and IODA Outages.
    Heuristics derived from open-source situational awareness research.
    """
    def __init__(self):
        self.type = "conflict"

    def analyze(self, gdelt_data, fire_data, outage_data):
        risk_score = 0
        evidence = []

        # 1. GDELT Analysis: Focus on negative Goldstein scale and conflict intensity
        # Assuming gdelt_data is a list of events
        if isinstance(gdelt_data, list) and len(gdelt_data) > 0:
            avg_goldstein = sum(float(e.get('goldstein', 0)) for e in gdelt_data) / len(gdelt_data)
            if avg_goldstein < -5:
                risk_score += 30
                evidence.append(f"High intensity negative events (Avg Goldstein: {avg_goldstein:.2f})")
            elif avg_goldstein < -2:
                risk_score += 15
                evidence.append(f"Moderate negative event trend (Avg Goldstein: {avg_goldstein:.2f})")

        # 2. NASA FIRMS Analysis: Thermal anomalies as proxy for kinetic activity
        # Assuming fire_data is a list of hotspots
        if isinstance(fire_data, list):
            hot_zones = len([f for f in fire_data if float(f.get('confidence', 0) or 0) > 80])
            if hot_zones > 10:
                risk_score += 25
                evidence.append(f"Critical thermal anomaly cluster ({hot_zones} high-conf fires)")
            elif hot_zones > 3:
                risk_score += 10
                evidence.append(f"Elevated thermal activity detected")

        # 3. IODA Analysis: Internet outages in sensitive regions
        # Assuming outage_data is a list of outages
        if isinstance(outage_data, list) and len(outage_data) > 0:
            risk_score += 20
            evidence.append(f"Internet infrastructure disruption in {len(outage_data)} regions")

        risk_level = "HIGH" if risk_score > 50 else "MEDIUM" if risk_score > 20 else "LOW"
        confidence = min(0.95, 0.5 + (risk_score / 150))

        if risk_score > 10:
            save_prediction(self.type, risk_score, risk_level, confidence, evidence)

        return {
            "type": self.type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "evidence": evidence,
            "timestamp": datetime.utcnow().isoformat()
        }
