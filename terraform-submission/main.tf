# =============================================================================
# main.tf — Terraform configuration (entry point)
# -----------------------------------------------------------------------------
# Author : Shahriar Hossain (Student ID: 30257)
# Course : DevOps And Cloud training batch 06
#
# This is a self-contained, runnable Terraform demo that needs NO cloud account.
# It uses the `local` and `random` providers to model a small 3-tier
# e-commerce application (web / api / cache) as generated configuration files.
#
# The same Terraform building blocks used here (providers, variables, locals,
# loops, templates, outputs, state) are exactly what the AWS modules in this
# repository use — just with different providers.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. Terraform settings + providers
#    Pinning versions (best practice) makes plans reproducible.
# -----------------------------------------------------------------------------
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "local" {}
provider "random" {}

# -----------------------------------------------------------------------------
# 2. Locals — computed values reused across resources.
#    Keeps names and tags consistent (DRY principle).
# -----------------------------------------------------------------------------
locals {
  name = "${var.project_name}-${var.environment}"

  # Metadata applied to every generated artifact.
  tags = {
    Student     = var.student_name
    StudentID   = var.student_id
    Course      = var.course_title
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  # Derive an endpoint URL for every declared tier, e.g. web -> http://localhost:8080
  tier_endpoints = {
    for tier, port in var.tiers :
    tier => "http://localhost:${port}"
  }
}

# -----------------------------------------------------------------------------
# 3. Random resources — generate a unique deployment id and an admin token.
#    (Proves the `random` provider and shows how values flow into other
#    resources and outputs.)
# -----------------------------------------------------------------------------
resource "random_pet" "deployment" {
  prefix = local.name
  length = 2
}

resource "random_password" "admin_token" {
  length  = 24
  special = false
}

# -----------------------------------------------------------------------------
# 4. Generate the deployment manifest (one JSON file describing everything).
#    `templatefile()` injects variables; `jsonencode()` keeps the JSON valid.
# -----------------------------------------------------------------------------
resource "local_file" "deployment_manifest" {
  filename = "${var.output_dir}/deployment.json"

  content = templatefile("${path.module}/templates/deployment.json.tftpl", {
    deployment_id  = random_pet.deployment.id
    app_name       = local.name
    environment    = var.environment
    student_name   = var.student_name
    student_id     = var.student_id
    course_title   = var.course_title
    endpoints_json = jsonencode(local.tier_endpoints)
    tags_json      = jsonencode(local.tags)
  })
}

# -----------------------------------------------------------------------------
# 5. Generate one config file per tier using `for_each` over a map.
#    `for_each` gives stable, key-based addresses (better than `count` when
#    items can be added/removed).
# -----------------------------------------------------------------------------
resource "local_file" "tier_config" {
  for_each = var.tiers

  filename = "${var.output_dir}/instances/${each.key}.conf"

  content = templatefile("${path.module}/templates/tier.conf.tftpl", {
    tier          = each.key
    port          = each.value
    endpoint      = local.tier_endpoints[each.key]
    deployment_id = random_pet.deployment.id
    environment   = var.environment
  })
}

# -----------------------------------------------------------------------------
# 6. Write the admin token to a file with restricted permissions.
#    `local_sensitive_file` mirrors the same idea as a real secret store.
# -----------------------------------------------------------------------------
resource "local_sensitive_file" "admin_token" {
  filename        = "${var.output_dir}/.admin_token"
  content         = random_password.admin_token.result
  file_permission = "0600"
}
