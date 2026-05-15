# AEGIS Free API Setup Guide 🆓

To fully unlock the real-time tracking capabilities of AEGIS without spending a dime, follow these steps to obtain your free API keys.

## ✈️ Aviation Tracking (OpenSky Network)
- **Status**: Required for global flight state vectors.
- **Action**: Register for a free account at [OpenSky Network](https://opensky-network.org/index.php?option=com_users&view=registration).
- **Env Vars**: `OPENSKY_CLIENT_ID`, `OPENSKY_CLIENT_SECRET`.
- **Note**: Without these, the system falls back to ADS-B Exchange (limited coverage).

## 🚢 Maritime Tracking (AIS Stream)
- **Status**: Required for real-time vessel positions.
- **Action**: Get a free API key at [aisstream.io](https://aisstream.io).
- **Env Var**: `AIS_API_KEY`.

## 🔥 Wildfire Monitoring (NASA FIRMS)
- **Status**: Required for active fire hotspots.
- **Action**: Request a free MAP key at [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/api/map_key/).
- **Env Var**: `NASA_FIRMS_KEY`.

## 💨 Air Quality (OpenAQ)
- **Status**: Required for PM2.5 station data.
- **Action**: Get a free API key at [OpenAQ](https://openaq.org/).
- **Env Var**: `OPENAQ_API_KEY`.

## 🎣 Fishing Activity (Global Fishing Watch)
- **Status**: Required for vessel events.
- **Action**: Register for a free API token at [Global Fishing Watch](https://globalfishingwatch.org/our-apis/).
- **Env Var**: `GFW_API_TOKEN`.

---

## 🚫 Restricted / Paid APIs (Optional)
The following APIs are **NOT** required for core functionality and often require payment or credit cards. AEGIS will gracefully skip these or use static fallbacks if keys are missing.

- **Shodan**: Requires a paid API key for full device search. (Optional `SHODAN_API_KEY`)
- **Sentinel Hub**: Free tier exists but requires credit card for signup. AEGIS uses static Sentinel-2 imagery if missing. (Optional `SH_CLIENT_ID`, `SH_CLIENT_SECRET`)

## 🏠 Self-Hosted / No-Key Sources
The following work out-of-the-box with no keys required:
- 🌋 **Earthquakes**: USGS (Public)
- ⚔️ **Conflicts**: GDELT Project (Public)
- 🛰️ **Satellites**: CelesTrak (Public)
- 🚂 **Trains**: Amtrak / DigiTraffic (Public/Free Tier)
- 🌐 **Internet Outages**: Georgia Tech IODA (Public)
- 📡 **Radio**: OpenMHz / KiwiSDR (Public)
- 📺 **CCTV**: 11,000+ public feeds
