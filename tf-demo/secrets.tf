resource "random_password" "jwt" {
  length  = 64
  special = false
}

resource "aws_secretsmanager_secret" "jwt" {
  name                    = "${local.name}/jwt-secret"
  description             = "JWT signing secret for the ${local.name} backend."
  recovery_window_in_days = var.secret_recovery_window_in_days
}

resource "aws_secretsmanager_secret_version" "jwt" {
  secret_id     = aws_secretsmanager_secret.jwt.id
  secret_string = random_password.jwt.result
}

resource "aws_secretsmanager_secret" "database_url" {
  name                    = "${local.name}/database-url"
  description             = "PostgreSQL connection string for the ${local.name} backend."
  recovery_window_in_days = var.secret_recovery_window_in_days
}

resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id = aws_secretsmanager_secret.database_url.id
  secret_string = format(
    "postgresql://%s:%s@%s:%s/%s",
    module.datastores.db_username,
    urlencode(module.datastores.db_password),
    module.datastores.db_address,
    module.datastores.db_port,
    module.datastores.db_name,
  )
}

resource "aws_secretsmanager_secret" "redis_url" {
  name                    = "${local.name}/redis-url"
  description             = "Redis connection string for the ${local.name} backend."
  recovery_window_in_days = var.secret_recovery_window_in_days
}

resource "aws_secretsmanager_secret_version" "redis_url" {
  secret_id = aws_secretsmanager_secret.redis_url.id
  secret_string = format(
    "redis://:%s@%s:%s",
    urlencode(module.datastores.redis_auth_token),
    module.datastores.redis_address,
    module.datastores.redis_port,
  )
}
