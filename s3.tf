resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_object" "my_files" {
  for_each = toset(var.upload_files)
  bucket   = aws_s3_bucket.my_bucket.bucket
  key      = each.key
  source   = "${path.module}/csv_files/${each.key}"
}
