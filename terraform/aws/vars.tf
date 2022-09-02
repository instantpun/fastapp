variable "AWS_REGION" {
  default = "us-east-1"
}

variable "app_prefix" {
  description = "Application prefix for the AWS services that are built"
  default = "my-ecs-app"
}

# variable "container_port" {
#   default = 8443
#   type    = integer
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