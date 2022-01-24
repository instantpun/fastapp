# configure ecr service for app
resource "aws_ecr_repository" "myapp_ecs_ecr_repo" {
  name                 = "${var.app_prefix}-repo"
  
  tags = {
    Name = "${var.app_prefix}-ecr-repo"
  }
}