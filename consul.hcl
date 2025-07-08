datacenter = "dc1"
data_dir = "data"
bind_addr = "127.0.0.1"
client_addr = "0.0.0.0"
ca_file   = "/home/spakai/consul/certs/consul-agent-ca.pem"
cert_file = "/home/spakai/consul/certs/dc1-server-consul-0.pem"    # For server agent
key_file  = "/home/spakai/consul/certs/dc1-server-consul-0-key.pem"
verify_incoming = true
verify_outgoing = true
verify_server_hostname = true

connect {
  enabled = true
}

ports {
  http = 0         # disable HTTP (port 8500)
  https = 8501     # enable TLS listener
  grpc = 0
  grpc_tls = 8503
}

addresses {
  https = "0.0.0.0"
}



