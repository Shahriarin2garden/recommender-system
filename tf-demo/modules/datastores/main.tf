resource "random_password" "db" {
  length  = 32
  special = false
}

resource "random_password" "redis_auth" {
  length  = 32
  special = false
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.name}-db-subnet-group"
  }
}

resource "aws_db_instance" "this" {
  identifier = "${var.name}-postgres"

  engine         = "postgres"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  allocated_storage = var.db_allocated_storage
  storage_type      = "gp3"
  storage_encrypted = true

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [var.db_security_group_id]
  publicly_accessible    = false

  multi_az                  = var.db_multi_az
  backup_retention_period   = var.db_backup_retention_days
  deletion_protection       = var.db_deletion_protection
  skip_final_snapshot       = !var.db_deletion_protection
  final_snapshot_identifier = var.db_deletion_protection ? "${var.name}-final-snapshot" : null

  auto_minor_version_upgrade = true
  apply_immediately          = true

  tags = {
    Name = "${var.name}-postgres"
  }
}

resource "aws_elasticache_subnet_group" "this" {
  name       = "${var.name}-redis"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.name}-redis-subnet-group"
  }
}

resource "aws_elasticache_replication_group" "this" {
  replication_group_id = "${var.name}-redis"
  description          = "Redis cache for ${var.name}"
  engine               = "redis"
  engine_version       = var.cache_engine_version
  node_type            = var.cache_node_type
  port                 = 6379

  num_cache_clusters = var.cache_num_nodes

  subnet_group_name  = aws_elasticache_subnet_group.this.name
  security_group_ids = [var.cache_security_group_id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis_auth.result
  auth_token_update_strategy = "ROTATE"

  automatic_failover_enabled = var.cache_num_nodes > 1
  apply_immediately          = true

  tags = {
    Name = "${var.name}-redis"
  }
}
