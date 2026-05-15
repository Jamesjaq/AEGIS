import os
import httpx
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class FreeDataIngestor:
    """
    Ingestor that strictly uses free/public endpoints.
    Can be used directly or as a fallback for ShadowBroker.
    """

    SOURCES = {
        "earthquakes": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "flights": "https://opensky-network.org/api/states/all",
        "conflicts": "https://api.gdeltproject.org/api/v2/events/events?format=json&query=conflict",
        "satellites": "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    }

    async def fetch_layer(self, layer_name: str) -> Dict[str, Any]:
        url = self.SOURCES.get(layer_name)
        if not url:
            return {"error": f"Layer {layer_name} not supported"}

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=15.0)
                if resp.status_code == 200:
                    return resp.json() if "json" in resp.headers.get("content-type", "") else {"raw": resp.text}
                return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    async def get_all_free_data(self) -> Dict[str, Any]:
        tasks = [self.fetch_layer(name) for name in self.SOURCES.keys()]
        results = await asyncio.gather(*tasks)
        return dict(zip(self.SOURCES.keys(), results))

class ShadowBrokerBridge:
    """
    Routes data from ShadowBroker backend to Unified API.
    Ensures zero data loss by preserving original telemetry.
    """
    def __init__(self, sb_backend_url: str):
        self.sb_url = sb_backend_url

    async def fetch_shadowbroker_data(self, tier: str = "fast") -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                if tier == "all":
                    resp = await client.get(f"{self.sb_url}/api/data", timeout=20.0)
                else:
                    resp = await client.get(f"{self.sb_url}/api/data/{tier}", timeout=10.0)

                if resp.status_code == 200:
                    return resp.json()
                return {"error": f"ShadowBroker API returned {resp.status_code}"}
        except Exception as e:
            logger.error(f"Failed to bridge ShadowBroker data: {e}")
            return {"error": str(e)}

    def transform_to_geoentities(self, sb_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        entities = []

        # 1. Flights
        for flight in sb_data.get("commercial_flights", []):
            entities.append({
                "id": f"flight-{flight.get('icao24')}",
                "pluginId": "shadow-bridge",
                "latitude": flight.get("lat"),
                "longitude": flight.get("lon"),
                "altitude": flight.get("alt"),
                "heading": flight.get("track"),
                "speed": flight.get("velocity"),
                "timestamp": flight.get("last_contact"),
                "label": flight.get("callsign", "N/A"),
                "properties": { **flight, "layer": "aviation", "sub_layer": "commercial" }
            })
        for flight in sb_data.get("military_flights", []):
            entities.append({
                "id": f"mil-{flight.get('icao24')}",
                "pluginId": "shadow-bridge",
                "latitude": flight.get("lat"),
                "longitude": flight.get("lon"),
                "altitude": flight.get("alt"),
                "heading": flight.get("track"),
                "label": flight.get("callsign", "MIL"),
                "properties": { **flight, "layer": "aviation", "sub_layer": "military" }
            })

        # 2. Ships
        for ship in sb_data.get("ships", []):
            entities.append({
                "id": f"ship-{ship.get('mmsi')}",
                "pluginId": "shadow-bridge",
                "latitude": ship.get("lat"),
                "longitude": ship.get("lon"),
                "heading": ship.get("heading"),
                "speed": ship.get("speed"),
                "label": ship.get("name", "N/A"),
                "properties": { **ship, "layer": "maritime" }
            })

        # 3. Conflicts (GDELT)
        for event in sb_data.get("gdelt", []):
            entities.append({
                "id": f"conflict-{event.get('id')}",
                "pluginId": "shadow-bridge",
                "latitude": event.get("lat"),
                "longitude": event.get("lon"),
                "label": event.get("title", "Conflict"),
                "properties": { **event, "layer": "conflict" }
            })

        # 4. Fires (NASA FIRMS)
        for fire in sb_data.get("firms_fires", []):
            entities.append({
                "id": f"fire-{fire.get('lat')}-{fire.get('lon')}",
                "pluginId": "shadow-bridge",
                "latitude": fire.get("lat"),
                "longitude": fire.get("lon"),
                "label": "Thermal Anomaly",
                "properties": { **fire, "layer": "natural-disaster", "sub_layer": "fire" }
            })

        # 5. Earthquakes
        for quake in sb_data.get("earthquakes", []):
            entities.append({
                "id": f"quake-{quake.get('id')}",
                "pluginId": "shadow-bridge",
                "latitude": quake.get("lat"),
                "longitude": quake.get("lng"),
                "label": f"M{quake.get('mag')} Quake",
                "properties": { **quake, "layer": "natural-disaster", "sub_layer": "earthquake" }
            })

        # 6. Satellites
        for sat in sb_data.get("satellites", []):
            entities.append({
                "id": f"sat-{sat.get('satid')}",
                "pluginId": "shadow-bridge",
                "latitude": sat.get("lat"),
                "longitude": sat.get("lng"),
                "altitude": sat.get("alt"),
                "label": sat.get("name"),
                "properties": { **sat, "layer": "space" }
            })

        # 7. Air Quality
        for aq in sb_data.get("air_quality", []):
            entities.append({
                "id": f"aq-{aq.get('id')}",
                "pluginId": "shadow-bridge",
                "latitude": aq.get("lat"),
                "longitude": aq.get("lon"),
                "label": f"AQ: {aq.get('value')}",
                "properties": { **aq, "layer": "natural-disaster", "sub_layer": "air_quality" }
            })

        # 8. Fishing
        for fish in sb_data.get("fishing_activity", []):
            entities.append({
                "id": f"fish-{fish.get('id')}",
                "pluginId": "shadow-bridge",
                "latitude": fish.get("lat"),
                "longitude": fish.get("lon"),
                "label": "Fishing Activity",
                "properties": { **fish, "layer": "maritime", "sub_layer": "fishing" }
            })

        # 9. Internet Outages
        for outage in sb_data.get("internet_outages", []):
            entities.append({
                "id": f"outage-{outage.get('region')}",
                "pluginId": "shadow-bridge",
                "latitude": outage.get("lat"),
                "longitude": outage.get("lon"),
                "label": f"Outage: {outage.get('region')}",
                "properties": { **outage, "layer": "infrastructure", "sub_layer": "outage" }
            })

        # 10. Trains
        for train in sb_data.get("trains", []):
            entities.append({
                "id": f"train-{train.get('id')}",
                "pluginId": "shadow-bridge",
                "latitude": train.get("lat"),
                "longitude": train.get("lon"),
                "heading": train.get("heading"),
                "label": f"Train {train.get('callsign')}",
                "properties": { **train, "layer": "infrastructure", "sub_layer": "train" }
            })

        return entities
