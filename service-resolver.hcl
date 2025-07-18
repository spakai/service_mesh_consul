Kind = "service-resolver"
Name = "service_b"
Subsets = {
  "v1" = { Filter = "Service.Tags contains \"v1\"" }
  "v2" = { Filter = "Service.Tags contains \"v2\"" }
} 