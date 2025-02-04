variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
}

variable "git_credentials" {
  type = object({
    username = string
    token = string
  })
  sensitive = true
}

variable "mongodb_secret" {
  type = object({
    username = string
    password = string
    name = string
    rootpassword = string
  })
  sensitive = true
}
