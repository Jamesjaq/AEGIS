import sqlite3
import os
from datetime import datetime
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "alerts.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            type TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            evidence TEXT,
            was_correct BOOLEAN,
            actual_outcome TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prediction(prediction_type, risk_score, risk_level, confidence, evidence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (timestamp, type, risk_score, risk_level, confidence, evidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        prediction_type,
        risk_score,
        risk_level,
        confidence,
        json.dumps(evidence)
    ))
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def update_outcome(prediction_id, was_correct, actual_outcome):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE predictions
        SET was_correct = ?, actual_outcome = ?
        WHERE id = ?
    """, (was_correct, actual_outcome, prediction_id))
    conn.commit()
    conn.close()

def get_predictions(limit=100):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
