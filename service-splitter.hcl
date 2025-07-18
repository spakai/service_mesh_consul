Kind = "service-splitter"
Name = "service_b"
Splits = [
  { Weight = 80, ServiceSubset = "v1" },
  { Weight = 20, ServiceSubset = "v2" }
] 