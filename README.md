# Consul Service Discovery Example

This project demonstrates service discovery using [Consul](https://www.consul.io/) with two Python Flask microservices: **Service A** and **Service B**. Both services register themselves with Consul and Service A discovers and calls Service B.

---

## Project Structure

```
consul/           # Consul configuration (consul.hcl)
service-a/        # Service A Flask app
service-b/        # Service B Flask app
certs/            # TLS certificates (if using TLS)
generate_consul_certs.sh  # Script to generate TLS certs
test_consul_tls.py        # Script to test Consul TLS endpoint
```

---

## Prerequisites
- Python 3.11+
- [Consul](https://www.consul.io/downloads)
- (Optional) Docker

---

## Running with TLS (Default)

1. **Generate certificates:**
   ```bash
   bash generate_consul_certs.sh
   ```

2. **Start Consul agent:**
   ```bash
   consul agent -dev -config-file=consul/consul.hcl
   ```

3. **Start Service B:**
   ```bash
   cd service-b
   python3 app.py
   ```

4. **Start Service A:**
   ```bash
   cd service-a
   python3 app.py
   ```

5. **Test Service A calling Service B:**
   ```bash
   curl http://localhost:5000/
   ```

---

## Running with HTTP Only (No TLS)

1. **Edit `consul/consul.hcl`:**
   - Set `ports { http = 8500 https = 0 }`
   - Remove or comment out all `ca_file`, `cert_file`, `key_file`, and TLS options.

2. **Update both `service-a/app.py` and `service-b/app.py`:**
   - Change all `https://localhost:8501` to `http://localhost:8500`
   - Remove all `cert=...` and `verify=...` arguments from `requests` calls.

3. **Restart Consul and both services as above.**

---

## How Service Discovery Works
- Each service registers itself with Consul on startup.
- Service A queries Consul's catalog to find Service B's address and port.
- Service A then makes an HTTP request to Service B using the discovered info.

---

## Testing
- **Service A main endpoint:** `curl http://localhost:5000/`
- **Service B data endpoint:** `curl http://localhost:5002/data`
- **Consul UI:** Visit [http://localhost:8500/ui/](http://localhost:8500/ui/) (if running in HTTP mode)

---

## Notes
- This setup is for local development and demonstration only.
- For production, use Consul Connect with sidecar proxies for secure mTLS communication.
- The Flask development server is not suitable for production workloads.

---

## License
MIT 