resource "aws_lambda_function" "lambda_function" {
  function_name    = var.lambda_name
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  filename         = "${path.module}/lambda/lambda_package.zip"
  source_code_hash = filebase64("${path.module}/lambda/lambda_package.zip")
  timeout          = 60
  role             = aws_iam_role.lambda_role.arn
}


