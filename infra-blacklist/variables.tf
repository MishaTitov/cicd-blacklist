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
