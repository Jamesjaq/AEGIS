import logging
from datetime import datetime
from database.manager import save_prediction

logger = logging.getLogger(__name__)

class EnvironmentalCrimePredictor:
    """
    Detects potential environmental crimes using Fishing, Air Quality, and Protected Zones data.
    """
    def __init__(self):
        self.type = "environment"

    def analyze(self, fishing_data, air_quality_data, vessel_data):
        risk_score = 0
        evidence = []

        # 1. Fishing Activity in suspicious patterns (e.g., loitering in EEZs)
        if isinstance(fishing_data, list) and len(fishing_data) > 0:
            loitering = len([f for f in fishing_data if f.get('event_type') == 'loitering'])
            if loitering > 5:
                risk_score += 25
                evidence.append(f"Multiple vessels loitering in protected fishing zones")

        # 2. Air Quality anomalies (illegal industrial activity)
        if isinstance(air_quality_data, list) and len(air_quality_data) > 0:
            high_pm25 = len([a for e in air_quality_data if (a := e.get('value', 0)) > 150])
            if high_pm25 > 0:
                risk_score += 20
                evidence.append(f"Critical Air Quality (PM2.5) detected near industrial clusters")

        # 3. AIS Spoofing/Dark Vessels (Vessels with disabled or inconsistent AIS)
        # This is a heuristic: vessels moving fast with no recent updates or unknown types
        if isinstance(vessel_data, list):
            dark_vessels = len([v for v in vessel_data if v.get('type') == 'unknown' and float(v.get('speed', 0)) > 5])
            if dark_vessels > 10:
                risk_score += 15
                evidence.append(f"Increased presence of unidentified fast-moving vessels")

        risk_level = "HIGH" if risk_score > 40 else "MEDIUM" if risk_score > 15 else "LOW"
        confidence = min(0.9, 0.4 + (risk_score / 120))

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
