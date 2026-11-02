output "db_address" {
  description = "RDS PostgreSQL hostname."
  value       = aws_db_instance.this.address
}

output "db_port" {
  description = "RDS PostgreSQL port."
  value       = aws_db_instance.this.port
}

output "db_name" {
  description = "PostgreSQL database name."
  value       = aws_db_instance.this.db_name
}

output "db_username" {
  description = "PostgreSQL master username."
  value       = aws_db_instance.this.username
}

output "db_password" {
  description = "PostgreSQL master password."
  value       = random_password.db.result
  sensitive   = true
}

output "redis_address" {
  description = "ElastiCache Redis primary endpoint."
  value       = aws_elasticache_replication_group.this.primary_endpoint_address
}

output "redis_port" {
  description = "ElastiCache Redis port."
  value       = aws_elasticache_replication_group.this.port
}

output "redis_auth_token" {
  description = "ElastiCache Redis auth token."
  value       = random_password.redis_auth.result
  sensitive   = true
}
