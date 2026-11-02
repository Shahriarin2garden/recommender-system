output "bucket_name" {
  description = "Name of the ML artifacts bucket."
  value       = aws_s3_bucket.ml.id
}

output "bucket_arn" {
  description = "ARN of the ML artifacts bucket."
  value       = aws_s3_bucket.ml.arn
}
