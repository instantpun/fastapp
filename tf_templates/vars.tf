variable "AWS_REGION" {
  default = "us-east-1"
}

variable "PATH_TO_PRIVATE_KEY" {
  default = "./.ssh-test/mykey"
}

variable "PATH_TO_PUBLIC_KEY" {
  default = "./.ssh-test/mykey.pub"
}

variable "AMIS" {
  type = map(string)
  default = {
    us-east-1 = "ami-06c8ff16263f3db59"
  }
}

variable "app_prefix" {
  description = "Application prefix for the AWS services that are built"
  default = "my-ecs-app"
}

variable "stage_name" {
  default = "dev"
  type    = "string"
}
