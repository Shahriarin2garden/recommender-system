output "alb_dns_name" {
  description = "Public DNS name of the application load balancer."
  value       = aws_lb.this.dns_name
}

output "ecr_repository_urls" {
  description = "ECR repository URLs for pushing images."
  value = {
    frontend = aws_ecr_repository.frontend.repository_url
    backend  = aws_ecr_repository.backend.repository_url
  }
}

output "cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.this.name
}

output "frontend_log_group_name" {
  description = "CloudWatch log group for the frontend service."
  value       = aws_cloudwatch_log_group.frontend.name
}

output "backend_log_group_name" {
  description = "CloudWatch log group for the backend service."
  value       = aws_cloudwatch_log_group.backend.name
}
