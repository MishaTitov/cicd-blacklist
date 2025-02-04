#/bin/bash
echo "connect to cluster"
aws eks update-kubeconfig --region ap-south-1 --name michael-cluster

echo "argocd password"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

echo "connect to argocd"
kubectl port-forward svc/argocd-server -n argocd 8080:80


echo "grafana password"
kubectl get secret -n prometheus-stack prometheus-stack-grafana -o jsonpath='{.data.admin-password}' | base64 -d

# echo "for ip"
# dig +short a0c4a53021dfa4b53b6d8a7f16a8f082-699618137.ap-south-1.elb.amazonaws.com