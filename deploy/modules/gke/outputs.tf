output "external_ip"{
    value = google_compute_global_address.external_ip.address
    description = "The IP address reserved for grafana"
}