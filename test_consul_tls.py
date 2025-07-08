import requests

CONSUL_HOST = "https://localhost:8501"
CERT = ("certs/dc1-client-consul-0.pem", "certs/dc1-client-consul-0-key.pem")
CA = "certs/consul-agent-ca.pem"

try:
    response = requests.get(f"{CONSUL_HOST}/v1/agent/self", cert=CERT, verify=CA)
    print("✅ TLS connection successful!")
    print("Agent info:")
    print(response.json())
except requests.exceptions.SSLError as e:
    print("❌ TLS verification failed!")
    print(e)
except Exception as ex:
    print("❌ Request failed!")
    print(ex)

