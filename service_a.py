import os
import requests
from flask import Flask, jsonify

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
CONSUL_PORT = os.environ.get("CONSUL_PORT", "8501")  # HTTPS port
SERVICE_NAME = "service_a"
SERVICE_PORT = 5000
UPSTREAM_PORT = 6000

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
    """Call Service B through the local Connect proxy."""
    url = f"http://localhost:{UPSTREAM_PORT}/hello"
    try:
        b_resp = requests.get(url)
        return jsonify({"service_b_response": b_resp.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def register_service():
    url = f"https://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    payload = {
        "Name": SERVICE_NAME,
        "Port": SERVICE_PORT,
        "Connect": {
            "SidecarService": {
                "Proxy": {
                    "Upstreams": [
                        {
                            "DestinationName": "service_b",
                            "LocalBindPort": UPSTREAM_PORT
                        }
                    ]
                }
            }
        },
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
