variable "name" {
  description = "Name prefix applied to all security group resources."
  type        = string
}

variable "vpc_id" {
  description = "VPC identifier in which to create the security groups."
  type        = string
}

variable "app_container_ports" {
  description = "Container ports exposed by the application tasks (frontend/backend)."
  type        = list(number)
}

variable "alb_ingress_cidrs" {
  description = "CIDR blocks allowed to reach the load balancer."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_https" {
  description = "Whether to open port 443 on the load balancer security group."
  type        = bool
  default     = false
}
