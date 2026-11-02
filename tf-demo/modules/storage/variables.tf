variable "name" {
  description = "Name prefix applied to the bucket."
  type        = string
}

variable "bucket_suffix" {
  description = "Globally-unique suffix appended to the bucket name (typically the account ID)."
  type        = string
}

variable "force_destroy" {
  description = "Allow the bucket to be destroyed with its contents."
  type        = bool
  default     = false
}
