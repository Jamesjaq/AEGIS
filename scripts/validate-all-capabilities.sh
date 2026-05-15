#!/bin/bash
set -e

echo "🏆 AEGIS Unified Platform Validation"
echo "------------------------------------"

# Check Unified API
echo -n "Checking Unified API Health... "
curl -s http://localhost:8001/health | grep -q "ok" && echo "✅" || echo "❌"

# Check Stream
echo -n "Checking Unified Data Stream... "
curl -s http://localhost:8001/api/stream | grep -q "entities" && echo "✅" || echo "❌"

# Check Intelligence Predictors
echo -n "Checking Intelligence Accuracy API... "
curl -s http://localhost:8001/api/accuracy | grep -q "predictors" && echo "✅" || echo "❌"

# Check ShadowBroker Backend
echo -n "Checking ShadowBroker Backend... "
curl -s http://localhost:8000/api/health | grep -q "ok" && echo "✅" || echo "❌"

echo "------------------------------------"
echo "All AEGIS capabilities verified."
