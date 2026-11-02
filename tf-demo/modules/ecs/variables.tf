variable "name" {
  description = "Name prefix applied to all ECS resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment name (dev, staging, prod)."
  type        = string
}

variable "region" {
  description = "AWS region (used for logging configuration)."
  type        = string
}

variable "aws_account_id" {
  description = "AWS account ID."
  type        = string
}

variable "vpc_id" {
  description = "VPC identifier."
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet identifiers for the load balancer."
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet identifiers for the ECS tasks."
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "Security group for the load balancer."
  type        = string
}

variable "app_security_group_id" {
  description = "Security group for the ECS tasks."
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN. When set, an HTTPS listener is created."
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = "Frontend image repository URL. Leave empty to use the ECR repository created here."
  type        = string
  default     = ""
}

variable "frontend_image_tag" {
  description = "Frontend image tag to deploy."
  type        = string
  default     = "latest"
}

variable "frontend_port" {
  description = "Port the frontend container listens on."
  type        = number
}

variable "frontend_cpu" {
  description = "CPU units for the frontend task."
  type        = number
}

variable "frontend_memory" {
  description = "Memory (MiB) for the frontend task."
  type        = number
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks."
  type        = number
}

variable "frontend_api_url" {
  description = "Value for NEXT_PUBLIC_API_URL."
  type        = string
}

variable "backend_image" {
  description = "Backend image repository URL. Leave empty to use the ECR repository created here."
  type        = string
  default     = ""
}

variable "backend_image_tag" {
  description = "Backend image tag to deploy."
  type        = string
  default     = "latest"
}

variable "backend_port" {
  description = "Port the backend container listens on."
  type        = number
}

variable "backend_cpu" {
  description = "CPU units for the backend task."
  type        = number
}

variable "backend_memory" {
  description = "Memory (MiB) for the backend task."
  type        = number
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks."
  type        = number
}

variable "backend_environment" {
  description = "Non-secret environment variables for the backend container."
  type        = map(string)
  default     = {}
}

variable "secrets" {
  description = "Mapping of backend environment variable name to Secrets Manager ARN."
  type        = map(string)
  default     = {}
}

variable "ml_bucket_arn" {
  description = "ARN of the S3 bucket holding ML artifacts, granted to the task role."
  type        = string
  default     = ""
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 30
}

variable "enable_autoscaling" {
  description = "Enable ECS service autoscaling based on CPU utilization."
  type        = bool
  default     = true
}

variable "autoscaling_max_count" {
  description = "Maximum task count when autoscaling is enabled."
  type        = number
  default     = 6
}
