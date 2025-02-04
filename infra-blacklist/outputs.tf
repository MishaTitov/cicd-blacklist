output "vpc_id" {
  value = module.network.aws_vpc_id
  description = "The VPC ID created by the network module"
}

output "eks_cluster_id" {
  value = module.compute.eks_cluster_id
  description = "The EKS Cluster ID created by the compute module"
}