terraform {
  required_providers {
    aws = {
      version = "~> 5.0"
    }
  }
  required_version = "~> 1.4.6"
}

provider "aws" {
  profile = "provide-aws-profile-name-here"
  region  = "us-east-1"
}

