variable "bucket_name" {
  type = string
}

variable "upload_files" {
  type    = list(any)
  default = ["customers_20220130.csv", "items_20220130.csv", "orders_20220130.csv"]
}

variable "queue_name" {
  type    = string
  default = "customer-order-message-queue"
}

variable "lambda_name" {
  type    = string
  default = "data-processing-function"
}
