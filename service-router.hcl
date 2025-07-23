Kind = "service-router"
Name = "service_b"
Routes = [
  {
    Match {
      HTTP {
        PathPrefix = "/"
      }
    }
    Destination {
      Service = "service_b"
      RequestTimeout = "2s"   # Timeout for requests
      NumRetries = 3           # Number of retries
    }
  }
] 