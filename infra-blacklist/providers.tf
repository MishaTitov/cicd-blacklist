terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
    tls = {
      source = "hashicorp/tls"
      version = "~> 4.0" 
    }
  }

  backend "s3" {
		bucket = "michael-bucket-bc22"
		key = "terraform/blacklist/terraform.state"
		region = "ap-south-1"
	}

  required_version = ">= 1.0.0"
}

provider "aws" {
  region = "ap-south-1"

  default_tags {
    tags = {
      expiration_date = "03-03-2025"
      owner       = "michael.titov"
      bootcamp   = "BC22"
    }
  }
}

provider "helm" {
  kubernetes {
    host                   = module.compute.eks_cluster_endpoint
    cluster_ca_certificate = base64decode(module.compute.eks_cluster_ca_certificate)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", "michael-cluster"]
      command     = "aws"
    }
  }
}

provider "kubernetes" {
  host                   = module.compute.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(module.compute.eks_cluster_ca_certificate)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    args        = ["eks", "get-token", "--cluster-name", "michael-cluster"]
    command     = "aws"
  }
}

provider "tls" {}
