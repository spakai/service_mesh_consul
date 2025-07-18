import os
import requests
from flask import Flask

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
CONSUL_PORT = os.environ.get("CONSUL_PORT", "8501")  # HTTPS port
SERVICE_NAME = "service_b"
SERVICE_PORT = 5002  # Different port for v2

CERT_DIR = "./certs"
CLIENT_CERT = os.path.join(CERT_DIR, "dc1-client-consul-0.pem")
CLIENT_KEY = os.path.join(CERT_DIR, "dc1-client-consul-0-key.pem")
CA_CERT = os.path.join(CERT_DIR, "consul-agent-ca.pem")

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello from service_b v2!"

def register_service():
    url = f"https://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    payload = {
        "Name": SERVICE_NAME,
        "ID": "service_b-v2",  # Unique service ID for v2
        "Port": SERVICE_PORT,
        "Tags": ["v2"],  # Tag as v2
        "Connect": {
            "SidecarService": {}
        },
        "Check": {
            "HTTP": f"http://localhost:{SERVICE_PORT}/hello",
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
            print(f"✅ Registered {SERVICE_NAME} v2 with Consul!")
        else:
            print(f"❌ Failed to register service v2: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Exception during registration: {e}")

def main():
    register_service()
    app.run(host="0.0.0.0", port=SERVICE_PORT)

if __name__ == "__main__":
    main() 