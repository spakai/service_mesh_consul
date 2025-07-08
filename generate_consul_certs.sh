#!/bin/bash
set -e

CERT_DIR="./certs"
DC="dc1"
DOMAIN="consul"
SERVER_SAN="server.${DC}.${DOMAIN}"

echo "🔄 Cleaning certs folder..."
rm -rf "$CERT_DIR"
mkdir -p "$CERT_DIR"

echo "✅ Generating CA..."
consul tls ca create

echo "✅ Generating server cert with SAN: $SERVER_SAN..."
consul tls cert create -server -dc "$DC" -additional-dnsname="$SERVER_SAN"

echo "✅ Generating client cert with SANs..."
consul tls cert create -client -dc "$DC" \
  -additional-dnsname="client.${DC}.${DOMAIN}" \
  -additional-dnsname="server.${DC}.${DOMAIN}" \
  -additional-dnsname="localhost" \
  -additional-dnsname="127.0.0.1" \
  -additional-ipaddress="127.0.0.1"

# Move CA outputs manually
mv *.pem "$CERT_DIR/" 2>/dev/null || true

# Move server certs
SERVER_CERT=$(find . -maxdepth 1 -name "*-server-consul-*.pem" | grep -v key.pem | head -n1)
SERVER_KEY=$(find . -maxdepth 1 -name "*-server-consul-*-key.pem" | head -n1)

# Move client certs
CLIENT_CERT=$(find . -maxdepth 1 -name "*-client-consul-*.pem" | grep -v key.pem | head -n1)
CLIENT_KEY=$(find . -maxdepth 1 -name "*-client-consul-*-key.pem" | head -n1)

echo "🎉 Done. Contents of $CERT_DIR:"
ls -1 "$CERT_DIR"

