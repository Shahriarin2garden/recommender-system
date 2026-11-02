locals {
  frontend_repo_url = aws_ecr_repository.frontend.repository_url
  backend_repo_url  = aws_ecr_repository.backend.repository_url

  frontend_image     = var.frontend_image != "" ? var.frontend_image : local.frontend_repo_url
  backend_image      = var.backend_image != "" ? var.backend_image : local.backend_repo_url
  frontend_image_uri = "${local.frontend_image}:${var.frontend_image_tag}"
  backend_image_uri  = "${local.backend_image}:${var.backend_image_tag}"

  https_enabled = var.certificate_arn != ""
}
