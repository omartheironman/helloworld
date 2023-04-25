variable "project" {
    type = string
    description = "Name of project"

}

variable "cluster_name" {
    type = string
    description = "Name of cluster"
}

variable "node_locations" {
  type        = list(string)
  description = "The list of zones where the GKE nodes are available in region"
}

variable "region" {
    type = string
    description = "Regional location of project"
}