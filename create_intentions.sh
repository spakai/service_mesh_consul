#!/bin/bash
set -e

# Paths to certs
CA_CERT="certs/consul-agent-ca.pem"
CLIENT_CERT="certs/dc1-client-consul-0.pem"
CLIENT_KEY="certs/dc1-client-consul-0-key.pem"
CONSUL_ADDR="https://127.0.0.1:8501"

echo "🔧 Setting up Consul intentions..."

# Set default policy to deny (optional - uncomment if you want to deny all by default)
# curl -k --cert $CLIENT_CERT --key $CLIENT_KEY \
#   --request POST \
#   --data '{"DefaultPolicy":"deny"}' \
#   $CONSUL_ADDR/v1/connect/intentions/check

# Deny service_a to talk to service_b using HTTP API
echo "⛔ Creating deny intention: service_a → service_b"
curl -k --cert $CLIENT_CERT --key $CLIENT_KEY \
  --request POST \
  --data '{"SourceName":"service_a","DestinationName":"service_b","Action":"deny"}' \
  $CONSUL_ADDR/v1/connect/intentions

echo "✅ Deny intention created successfully."

# List all intentions
echo "📋 Current intentions:"
consul intention list -http-addr=$CONSUL_ADDR -ca-file=$CA_CERT -client-cert=$CLIENT_CERT -client-key=$CLIENT_KEY

echo ""
echo "🧪 Testing the deny intention..."
echo "Testing service_a calling service_b (should fail):"
curl -s http://localhost:5000/call-b || echo "❌ Call failed as expected (intention working)"

echo ""
echo "Testing service_a direct endpoint (should work):"
curl -s http://localhost:5000/ || echo "❌ Service A not responding"

echo ""
echo "🎉 Intention setup complete!" 