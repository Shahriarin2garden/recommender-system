output "alb_sg_id" {
  description = "Security group attached to the load balancer."
  value       = aws_security_group.alb.id
}

output "app_sg_id" {
  description = "Security group attached to the application tasks."
  value       = aws_security_group.app.id
}

output "db_sg_id" {
  description = "Security group attached to the database."
  value       = aws_security_group.db.id
}

output "cache_sg_id" {
  description = "Security group attached to the cache."
  value       = aws_security_group.cache.id
}
