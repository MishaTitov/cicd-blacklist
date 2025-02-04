output "aws_vpc_id" {
  value = aws_vpc.k8s_vpc.id
  description = "ID of the VPC created for the Kubernetes cluster"
}

output "public_subnet_ids" {
  value = aws_subnet.public_subnets[*].id
  description = "IDs of the public subnets"
}