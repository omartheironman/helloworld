resource "google_compute_global_address" "external_ip" {
  project      = var.project 
  name         = "${substr(var.region, 0, 2)}-ip-address"
  address_type = "EXTERNAL"
  ip_version   = "IPV4"
}