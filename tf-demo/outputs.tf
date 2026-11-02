output "aws_region" {
  description = "Configured AWS region."
  value       = var.aws_region
}

output "name_prefix" {
  description = "Generated resource name prefix."
  value       = local.name
}

output "vpc_id" {
  description = "VPC identifier."
  value       = module.network.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet identifiers."
  value       = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet identifiers."
  value       = module.network.private_subnet_ids
}

output "load_balancer_dns_name" {
  description = "Public DNS name of the application load balancer."
  value       = module.ecs.alb_dns_name
}

output "application_url" {
  description = "Convenience URL for the deployed application."
  value       = var.certificate_arn != "" ? "https://${module.ecs.alb_dns_name}" : "http://${module.ecs.alb_dns_name}"
}

output "ecr_repository_urls" {
  description = "ECR repository URLs for pushing images."
  value       = module.ecs.ecr_repository_urls
}

output "database_address" {
  description = "RDS PostgreSQL hostname."
  value       = module.datastores.db_address
  sensitive   = true
}

output "redis_address" {
  description = "ElastiCache Redis primary endpoint."
  value       = module.datastores.redis_address
  sensitive   = true
}

output "ml_artifacts_bucket" {
  description = "S3 bucket that stores ML model artifacts."
  value       = module.storage.bucket_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = module.ecs.cluster_name
}

output "backend_log_group" {
  description = "CloudWatch log group for the backend service."
  value       = module.ecs.backend_log_group_name
}

output "frontend_log_group" {
  description = "CloudWatch log group for the frontend service."
  value       = module.ecs.frontend_log_group_name
}
