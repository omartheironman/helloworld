terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.43.0"
    }
    google-beta = {
        source = "hashicorp/google-beta"
    }
  }
}

data "google_client_config" "default" {}

provider "google" {
  # Configuration options
  project = var.project
  region  = var.region
}

