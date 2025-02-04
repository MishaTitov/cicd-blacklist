module "network" {
  source = "./modules/network"
}

module "compute" {
  source = "./modules/compute"
  vpc_id = module.network.aws_vpc_id
  subnet_ids = module.network.public_subnet_ids
  git_credentials = var.git_credentials
  mongodb_secret = var.mongodb_secret
  providers = {
    tls = tls
  }
}
