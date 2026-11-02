terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Remote state is strongly recommended for any shared/team environment.
  # Create the bucket and lock table out-of-band, then uncomment:
  #
  # backend "s3" {
  #   bucket         = "my-terraform-state"
  #   key            = "shop/dev/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-locks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.default_tags
  }
}

data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  name = "${var.project_name}-${var.environment}"

  default_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  availability_zones = slice(
    data.aws_availability_zones.available.names,
    0,
    var.availability_zone_count,
  )

  container_ports = [var.frontend_container_port, var.backend_container_port]
}

module "network" {
  source = "./modules/network"

  name                 = local.name
  vpc_cidr             = var.vpc_cidr
  availability_zones   = local.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = var.enable_nat_gateway
  single_nat_gateway   = var.single_nat_gateway
}

module "security" {
  source = "./modules/security"

  name                = local.name
  vpc_id              = module.network.vpc_id
  app_container_ports = local.container_ports
  alb_ingress_cidrs   = var.alb_ingress_cidrs
  enable_https        = var.certificate_arn != ""
}

module "datastores" {
  source = "./modules/datastores"

  name                    = local.name
  private_subnet_ids      = module.network.private_subnet_ids
  db_security_group_id    = module.security.db_sg_id
  cache_security_group_id = module.security.cache_sg_id

  db_name                  = var.db_name
  db_username              = var.db_username
  db_engine_version        = var.db_engine_version
  db_instance_class        = var.db_instance_class
  db_allocated_storage     = var.db_allocated_storage
  db_multi_az              = var.db_multi_az
  db_backup_retention_days = var.db_backup_retention_days
  db_deletion_protection   = var.db_deletion_protection

  cache_node_type      = var.cache_node_type
  cache_num_nodes      = var.cache_num_nodes
  cache_engine_version = var.cache_engine_version
}

module "storage" {
  source = "./modules/storage"

  name          = local.name
  bucket_suffix = data.aws_caller_identity.current.account_id
  force_destroy = var.s3_force_destroy
}

module "ecs" {
  source = "./modules/ecs"

  name           = local.name
  environment    = var.environment
  region         = var.aws_region
  aws_account_id = data.aws_caller_identity.current.account_id

  vpc_id                = module.network.vpc_id
  public_subnet_ids     = module.network.public_subnet_ids
  private_subnet_ids    = module.network.private_subnet_ids
  alb_security_group_id = module.security.alb_sg_id
  app_security_group_id = module.security.app_sg_id

  certificate_arn = var.certificate_arn

  frontend_image         = var.frontend_image
  frontend_image_tag     = var.frontend_image_tag
  frontend_port          = var.frontend_container_port
  frontend_cpu           = var.frontend_cpu
  frontend_memory        = var.frontend_memory
  frontend_desired_count = var.frontend_desired_count
  frontend_api_url       = var.frontend_api_url

  backend_image         = var.backend_image
  backend_image_tag     = var.backend_image_tag
  backend_port          = var.backend_container_port
  backend_cpu           = var.backend_cpu
  backend_memory        = var.backend_memory
  backend_desired_count = var.backend_desired_count
  backend_environment = {
    ENVIRONMENT   = var.environment
    ROOT_PATH     = "/api"
    MODEL_PATH    = "/app/ml/models"
    ML_BUCKET     = module.storage.bucket_name
    FRONTEND_URL  = var.frontend_url
    CORS_ORIGINS  = var.cors_origins
    ALLOW_SEED    = "false"
    COOKIE_SECURE = "true"
  }

  # Values are injected from Secrets Manager at task start.
  secrets = {
    DATABASE_URL = aws_secretsmanager_secret.database_url.arn
    REDIS_URL    = aws_secretsmanager_secret.redis_url.arn
    JWT_SECRET   = aws_secretsmanager_secret.jwt.arn
  }

  ml_bucket_arn = module.storage.bucket_arn

  log_retention_days    = var.log_retention_days
  enable_autoscaling    = var.enable_autoscaling
  autoscaling_max_count = var.autoscaling_max_count
}
