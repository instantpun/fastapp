# configure ecr service for app
resource "aws_ecr_repository" "demo_fastapi" {
  name                 = "${var.common_tags["Application"]}"
  image_tag_mutability = "MUTABLE"

  tags = var.common_tags
}

resource "aws_ecr_lifecycle_policy" "demo_fastapi" {
  repository = aws_ecr_repository.demo_fastapi.name
 
  policy = jsonencode({
   rules = [{
     rulePriority = 1
     description  = "keep last 10 images"
     action       = {
       type = "expire"
     }
     selection     = {
       tagStatus   = "any"
       countType   = "imageCountMoreThan"
       countNumber = 10
     }
   }]
  })
}