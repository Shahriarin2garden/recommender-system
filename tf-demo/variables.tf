variable "aws_region" {
  description = "AWS region in which to create resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming and tags."
  type        = string
  default     = "shop"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)."
  type        = string
  default     = "dev"
}

# ---------------------------------------------------------------------------
# Networking
# ---------------------------------------------------------------------------

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zone_count" {
  description = "Number of availability zones to spread resources across."
  type        = number
  default     = 2
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets (one per AZ)."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets (one per AZ)."
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

variable "enable_nat_gateway" {
  description = "Create NAT gateway(s) so private subnets can reach the internet."
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use a single NAT gateway (cheaper, not highly available)."
  type        = bool
  default     = true
}

variable "alb_ingress_cidrs" {
  description = "CIDR blocks allowed to reach the load balancer."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "recommender_db"
}

variable "db_username" {
  description = "PostgreSQL master username."
  type        = string
  default     = "recommender_user"
}

variable "db_engine_version" {
  description = "PostgreSQL engine version."
  type        = string
  default     = "15"
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GiB."
  type        = number
  default     = 20
}

variable "db_multi_az" {
  description = "Enable Multi-AZ for the database."
  type        = bool
  default     = false
}

variable "db_backup_retention_days" {
  description = "Number of days to retain automated backups."
  type        = number
  default     = 7
}

variable "db_deletion_protection" {
  description = "Prevent accidental database deletion."
  type        = bool
  default     = false
}

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

variable "cache_node_type" {
  description = "ElastiCache node type."
  type        = string
  default     = "cache.t4g.micro"
}

variable "cache_num_nodes" {
  description = "Number of Redis cache nodes."
  type        = number
  default     = 1
}

variable "cache_engine_version" {
  description = "Redis engine version."
  type        = string
  default     = "7.1"
}

# ---------------------------------------------------------------------------
# Container images / ECS
# ---------------------------------------------------------------------------

variable "frontend_image" {
  description = "Full frontend image repository URL. Leave empty to use the ECR repository created by the ECS module."
  type        = string
  default     = ""
}

variable "frontend_image_tag" {
  description = "Frontend image tag to deploy."
  type        = string
  default     = "latest"
}

variable "backend_image" {
  description = "Full backend image repository URL. Leave empty to use the ECR repository created by the ECS module."
  type        = string
  default     = ""
}

variable "backend_image_tag" {
  description = "Backend image tag to deploy."
  type        = string
  default     = "latest"
}

variable "frontend_container_port" {
  description = "Port the frontend container listens on."
  type        = number
  default     = 3000
}

variable "backend_container_port" {
  description = "Port the backend container listens on."
  type        = number
  default     = 8000
}

variable "frontend_desired_count" {
  description = "Desired number of frontend tasks."
  type        = number
  default     = 2
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks."
  type        = number
  default     = 2
}

variable "frontend_cpu" {
  description = "CPU units for the frontend task (1024 = 1 vCPU)."
  type        = number
  default     = 256
}

variable "frontend_memory" {
  description = "Memory (MiB) for the frontend task."
  type        = number
  default     = 512
}

variable "backend_cpu" {
  description = "CPU units for the backend task (1024 = 1 vCPU)."
  type        = number
  default     = 512
}

variable "backend_memory" {
  description = "Memory (MiB) for the backend task."
  type        = number
  default     = 1024
}

variable "frontend_api_url" {
  description = "Value for NEXT_PUBLIC_API_URL. Use /api to route through the ALB."
  type        = string
  default     = "/api"
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

# ---------------------------------------------------------------------------
# Application / TLS / observability
# ---------------------------------------------------------------------------

variable "frontend_url" {
  description = "Public URL of the frontend, used for CORS and redirects."
  type        = string
  default     = "http://localhost"
}

variable "cors_origins" {
  description = "Comma-separated list of allowed CORS origins."
  type        = string
  default     = "http://localhost"
}

variable "certificate_arn" {
  description = "ACM certificate ARN. When set, an HTTPS listener is created and HTTP redirects to it."
  type        = string
  default     = ""
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 30
}

variable "secret_recovery_window_in_days" {
  description = "Recovery window for Secrets Manager secrets (0 deletes immediately; use 7-30 in prod)."
  type        = number
  default     = 0
}

variable "s3_force_destroy" {
  description = "Allow the ML artifacts bucket to be destroyed with contents."
  type        = bool
  default     = false
}
