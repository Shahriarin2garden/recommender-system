# =============================================================================
# outputs.tf — Values printed after `terraform apply`
# -----------------------------------------------------------------------------
# Outputs expose useful results and can be consumed by other configurations.
# Sensitive outputs are hidden in the CLI until requested with:
#   terraform output -raw admin_token
# =============================================================================

output "deployment_id" {
  description = "Unique id generated for this deployment."
  value       = random_pet.deployment.id
}

output "student" {
  description = "Submission metadata (personalization)."
  value = {
    name   = var.student_name
    id     = var.student_id
    course = var.course_title
  }
}

output "environment" {
  description = "Environment this demo was deployed with."
  value       = var.environment
}

output "endpoints" {
  description = "Derived endpoint URL for each application tier."
  value       = local.tier_endpoints
}

output "manifest_file" {
  description = "Path to the generated deployment manifest."
  value       = local_file.deployment_manifest.filename
}

output "tier_config_files" {
  description = "Paths to the generated per-tier config files."
  value       = [for f in local_file.tier_config : f.filename]
}

output "admin_token" {
  description = "Generated admin token (sensitive: not shown by default)."
  value       = random_password.admin_token.result
  sensitive   = true
}