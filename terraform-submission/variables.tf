# =============================================================================
# variables.tf — Inputs for the demo
# -----------------------------------------------------------------------------
# Every input has a type, a description and (where sensible) a default so the
# configuration can run with zero arguments. `validation` blocks reject bad
# input early with a clear message instead of failing halfway through.
# =============================================================================

# ----------------------------- Personalization -------------------------------

variable "student_name" {
  description = "Full name of the student submitting this demo."
  type        = string
  default     = "Shahriar Hossain"
}

variable "student_id" {
  description = "Student ID."
  type        = string
  default     = "30257"
}

variable "course_title" {
  description = "Course / batch title."
  type        = string
  default     = "DevOps And Cloud training batch 06"
}

# ------------------------------- Application ---------------------------------

variable "project_name" {
  description = "Short project name used in the deployment id."
  type        = string
  default     = "ecommerce-demo"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name may only contain lowercase letters, numbers and hyphens."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

variable "tiers" {
  description = "Map of application tier name to the port it listens on."
  type        = map(number)
  default = {
    web   = 8080
    api   = 8000
    cache = 6379
  }

  validation {
    condition     = length(var.tiers) > 0
    error_message = "At least one tier must be defined."
  }
}

variable "output_dir" {
  description = "Directory where the generated files are written."
  type        = string
  default     = "output"
}
