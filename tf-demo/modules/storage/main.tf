resource "aws_s3_bucket" "ml" {
  bucket        = "${var.name}-ml-artifacts-${var.bucket_suffix}"
  force_destroy = var.force_destroy

  tags = {
    Name = "${var.name}-ml-artifacts"
  }
}

resource "aws_s3_bucket_versioning" "ml" {
  bucket = aws_s3_bucket.ml.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ml" {
  bucket = aws_s3_bucket.ml.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "ml" {
  bucket = aws_s3_bucket.ml.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "ml" {
  bucket = aws_s3_bucket.ml.id

  rule {
    id     = "expire-noncurrent-versions"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}
