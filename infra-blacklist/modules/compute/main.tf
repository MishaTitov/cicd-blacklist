resource "aws_eks_cluster" "michael_cluster" {
  name     = "michael-cluster"
  role_arn = aws_iam_role.eks_service_role.arn
  vpc_config {
    subnet_ids = var.subnet_ids
    security_group_ids = [aws_security_group.k8s_sg.id]
  }

  tags = {
    Name = "michael-cluster"
  }
}

resource "aws_iam_role" "eks_service_role" {
  name = "michael-eks-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "eks.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_service_policy" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "vpc_policy" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
}

# Node group configuration
resource "aws_eks_node_group" "app_nodes" {
  cluster_name    = aws_eks_cluster.michael_cluster.name
  node_group_name = "michael-k8s-nodes"
  node_role_arn   = aws_iam_role.eks_worker_role.arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 3
    max_size     = 3
    min_size     = 2
  }

  instance_types = ["t3a.medium"]

  depends_on = [
    aws_eks_cluster.michael_cluster
  ]
}

resource "aws_iam_role" "eks_worker_role" {
  name = "michael-eks-worker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "ec2.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "worker_node_policy" {
  role       = aws_iam_role.eks_worker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  role       = aws_iam_role.eks_worker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "registry_policy" {
  role       = aws_iam_role.eks_worker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_policy" "ebs_csi_policy" {
  name        = "michael-eks-ebs-csi-policy"
  description = "Policy for EBS CSI driver"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ec2:CreateVolume",
          "ec2:DeleteVolume",
          "ec2:DescribeVolumes",
          "ec2:AttachVolume",
          "ec2:DetachVolume",
          "ec2:DescribeInstances"
        ],
        Resource = "*"
      }
    ]
  })
}

# Attach policy to worker role
resource "aws_iam_role_policy_attachment" "ebs_csi_attachment" {
  role       = aws_iam_role.eks_worker_role.name
  policy_arn = aws_iam_policy.ebs_csi_policy.arn
}

resource "aws_security_group" "k8s_sg" {
  name        = "michael-k8s-sg"
  description = "Security group for Kubernetes nodes"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# data "kubernetes_namespace" "argcd_exists"{
#   metadata {
#     name = "argocd"
#   }
# }

resource "kubernetes_namespace" "argocd_namespace" {
  # count = length(data.kubernetes_namespace.argcd_exists) == 0? 1: 0
  metadata {
    name = "argocd"
  }
}

resource "kubernetes_namespace" "mongodb_namespace" {
  metadata {
    name = "mongodb"
  }
}

resource "kubernetes_namespace" "bl_cd_namespace" {
  metadata {
    name = "bl-cd"
  }
}

resource "kubernetes_secret" "git_credentials" {
  metadata {
    name      = "github-credentials"
    namespace = "argocd"
  }

  data = {
    username = var.git_credentials.username
    token = var.git_credentials.token
  }

  type = "Opaque"
  depends_on = [ kubernetes_namespace.argocd_namespace ]
}

resource "kubernetes_secret" "mongodb_secret" {
  metadata {
    name      = "mongodb-secret"
    namespace = "mongodb"
  }

  data = {
    DB_USERNAME = var.mongodb_secret.username
    DB_PASSWORD = var.mongodb_secret.password
    DB_NAME = var.mongodb_secret.name
    ROOT_PASSWORD = var.mongodb_secret.rootpassword
  }

  type = "Opaque"
  depends_on = [ kubernetes_namespace.mongodb_namespace ]
}

resource "kubernetes_secret" "mongodb_secret" {
  metadata {
    name      = "mongodb-secret"
    namespace = "bl-cd"
  }

  data = {
    DB_USERNAME = var.mongodb_secret.username
    DB_PASSWORD = var.mongodb_secret.password
    DB_NAME = var.mongodb_secret.name
  }

  type = "Opaque"
  depends_on = [ kubernetes_namespace.bl_cd_namespace ]
}

resource "helm_release" "argocd" {
  name       = "argocd"
  namespace  = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  version    = "7.7.16"

  create_namespace = true

  values = [
    <<EOF
    server:
      service:
        type: ClusterIP
      extraArgs:
        - --insecure
    configs:
      cm:
        timeout.reconciliation: 180s
        application.instanceLabelKey: argocd.argoproj.io/instance
        repositories: |
          - url: https://github.com/MishaTitov/gitops-blacklist.git
            type: git
            project: default
            usernameSecret: 
              name: github-credentials
              key: username
            passwordSecret:
              name: github-credentials
              key: token
    EOF
  ]

  depends_on = [
    kubernetes_secret.git_credentials, 
    kubernetes_namespace.argocd_namespace
    ]
}


### ebs ###
# TLS needed for the thumbprint
# provider "tls" {}
terraform {
  required_providers {
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0" # Specify an appropriate version
    }
  }
}

data "tls_certificate" "oidc" {
  url = aws_eks_cluster.michael_cluster.identity[0].oidc[0].issuer
}

# EKS addon
resource "aws_eks_addon" "ebs_csi_driver" {
  cluster_name             = aws_eks_cluster.michael_cluster.name
  addon_name               = "aws-ebs-csi-driver"
  addon_version            = "v1.29.1-eksbuild.1"
  service_account_role_arn = aws_iam_role.ebs_csi_driver.arn
}

# AWS Identity and Access Management (IAM) OpenID Connect (OIDC) provider

resource "aws_iam_openid_connect_provider" "eks" {
  url             = aws_eks_cluster.michael_cluster.identity.0.oidc.0.issuer
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.oidc.certificates[0].sha1_fingerprint]
}

# IAM
resource "aws_iam_role" "ebs_csi_driver" {
  name               = "michael-ebs-csi-driver"
  assume_role_policy = data.aws_iam_policy_document.ebs_csi_driver_assume_role.json
}

data "aws_iam_policy_document" "ebs_csi_driver_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
    }

    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    condition {
      test     = "StringEquals"
      variable = "${aws_iam_openid_connect_provider.eks.url}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${aws_iam_openid_connect_provider.eks.url}:sub"
      values   = ["system:serviceaccount:kube-system:ebs-csi-controller-sa"]
    }

  }
}

resource "aws_iam_role_policy_attachment" "AmazonEBSCSIDriverPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
  role       = aws_iam_role.ebs_csi_driver.name
}