variable "name" {
  description = "Name prefix applied to all datastore resources."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet identifiers used for subnet groups."
  type        = list(string)
}

variable "db_security_group_id" {
  description = "Security group attached to the database."
  type        = string
}

variable "cache_security_group_id" {
  description = "Security group attached to the cache."
  type        = string
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
}

variable "db_username" {
  description = "PostgreSQL master username."
  type        = string
}

variable "db_engine_version" {
  description = "PostgreSQL engine version."
  type        = string
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
}

variable "db_allocated_storage" {
  description = "Allocated storage in GiB."
  type        = number
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

variable "cache_node_type" {
  description = "ElastiCache node type."
  type        = string
}

variable "cache_num_nodes" {
  description = "Number of Redis cache nodes."
  type        = number
}

variable "cache_engine_version" {
  description = "Redis engine version."
  type        = string
}
