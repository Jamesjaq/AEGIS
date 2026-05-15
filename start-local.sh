#!/bin/bash
# AEGIS Local Startup Script - Runs everything on one laptop

echo "🛡️ Starting AEGIS Locally..."

# Handle process cleanup on exit
cleanup() {
    echo "🛑 Stopping AEGIS services..."
    kill $BRIDGE_PID $SHADOW_PID $WWV_PID 2>/dev/null
}
trap cleanup SIGINT SIGTERM

# Start Unified Bridge (Port 5000)
cd unified-api
python3 bridge.py &
BRIDGE_PID=$!
echo "✅ Bridge running on port 5000 (PID: $BRIDGE_PID)"
cd ..

# Wait for bridge to start
sleep 3

# Start ShadowBroker (Port 8000) - Optional
if [ -d "shadowbroker/backend" ]; then
    echo "🔍 Starting ShadowBroker backend..."
    cd shadowbroker/backend
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
    python3 main.py &
    SHADOW_PID=$!
    echo "✅ ShadowBroker running on port 8000 (PID: $SHADOW_PID)"
    cd ../..
fi

# Start WorldWideView (Port 3000)
cd worldwideview
SKIP_DB=true DEMO_MODE=true pnpm dev &
WWV_PID=$!
echo "✅ WorldWideView running on port 3000 (PID: $WWV_PID)"
cd ..

echo ""
echo "🌍 AEGIS is running locally:"
echo "   Dashboard: http://localhost:5000/dashboard"
echo "   3D Globe:  http://localhost:3000"
echo "   API:       http://localhost:5000/api/predictions"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait
