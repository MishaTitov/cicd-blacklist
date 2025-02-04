output "eks_cluster_id" {
  value = aws_eks_cluster.michael_cluster.id
  description = "The ID of the EKS cluster"
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.michael_cluster.endpoint
}

output "eks_cluster_ca_certificate" {
  value = aws_eks_cluster.michael_cluster.certificate_authority[0].data
}

output "eks_cluster_name" {
  value = aws_eks_cluster.michael_cluster.name
}
