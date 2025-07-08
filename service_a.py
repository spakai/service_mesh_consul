import os
import requests
from flask import Flask, jsonify

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
CONSUL_PORT = os.environ.get("CONSUL_PORT", "8501")  # HTTPS port
SERVICE_NAME = "service_a"
SERVICE_PORT = 5000

CERT_DIR = "./certs"
CLIENT_CERT = os.path.join(CERT_DIR, "dc1-client-consul-0.pem")
CLIENT_KEY = os.path.join(CERT_DIR, "dc1-client-consul-0-key.pem")
CA_CERT = os.path.join(CERT_DIR, "consul-agent-ca.pem")

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from service_a!"

@app.route("/call-b")
def call_b():
    # Query Consul for service_b
    consul_url = f"https://{CONSUL_HOST}:{CONSUL_PORT}/v1/catalog/service/service_b"
    try:
        resp = requests.get(
            consul_url,
            cert=(CLIENT_CERT, CLIENT_KEY),
            verify=CA_CERT
        )
        if resp.status_code != 200:
            return jsonify({"error": f"Failed to query Consul: {resp.status_code} {resp.text}"}), 500
        services = resp.json()
        if not services:
            return jsonify({"error": "service_b not found in Consul"}), 404
        # Use the first available service_b instance
        service_b_info = services[0]
        address = service_b_info.get("ServiceAddress") or service_b_info.get("Address")
        port = service_b_info.get("ServicePort")
        if not address or not port:
            return jsonify({"error": "service_b address/port not found"}), 500
        # Call service_b's /hello endpoint
        url = f"http://{address}:{port}/hello"
        b_resp = requests.get(url)
        return jsonify({"service_b_response": b_resp.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def register_service():
    url = f"https://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    payload = {
        "Name": SERVICE_NAME,
        "Port": SERVICE_PORT,
        "Check": {
            "HTTP": f"http://localhost:{SERVICE_PORT}/",
            "Interval": "10s"
        }
    }
    try:
        response = requests.put(
            url,
            json=payload,
            cert=(CLIENT_CERT, CLIENT_KEY),
            verify=CA_CERT
        )
        if response.status_code == 200:
            print(f"✅ Registered {SERVICE_NAME} with Consul!")
        else:
            print(f"❌ Failed to register service: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Exception during registration: {e}")

def main():
    register_service()
    app.run(host="0.0.0.0", port=SERVICE_PORT)

if __name__ == "__main__":
    main() 
