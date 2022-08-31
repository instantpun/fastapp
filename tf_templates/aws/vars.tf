variable "AWS_REGION" {
  default = "us-east-1"
}

variable "app_prefix" {
  description = "Application prefix for the AWS services that are built"
  default = "my-ecs-app"
}

# variable "stage_name" {
#   default = "dev"
#   type    = string
# }

variable "common_tags" {
  type    = map(string)
  default = {
    ServiceName = "demo-webservice"
    Owner       = "instantpun@gmail.com"
    Environment = "dev"
    Application = "demo-fastapi"
  }
}