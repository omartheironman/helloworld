resource "google_compute_global_address" "external_ip" {
  project      = var.project 
  name         = "helloworld-ip-address"
  address_type = "EXTERNAL"
  ip_version   = "IPV4"
}