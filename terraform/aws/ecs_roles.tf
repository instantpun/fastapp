locals {
  iam_role_name       = "${var.app_prefix}-ECSRunTaskSyncExecutionRole"
  iam_policy_name     = "FargateTaskNotificationAccessPolicy"
  iam_task_role_policy_name = "${var.app_prefix}-ECS-Task-Role-Policy"
  # # can validate with: jq . values-local.json
  ecs_task_role = file("${path.module}/iam/ecs_task_role.json")
  private_registry_policy = file("${path.module}/iam/private_registry_auth_policy.json")
}

// AWS Identity for ECS Tasks to perform work
resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.app_prefix}-ECSTaskRole"
  assume_role_policy = "${local.ecs_task_role}"
  
  tags = var.common_tags
}

// AWS Identity for ECS Tasks to run on compute cluster
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.app_prefix}-ECSTaskExecutionRole"
  assume_role_policy = "${local.ecs_task_role}"

  tags = var.common_tags
}

# data "aws_iam_policy_document" "myapp_ecs_policy_document" {
#   statement {
#     actions = ["sts:AssumeRole"]
#     principals {
#       type        = "Service"
#       identifiers = ["states.amazonaws.com"]
#     }
#   }
# }

# resource "aws_iam_role_policy" "myapp_ecs_policy" {
#   name = "${local.iam_policy_name}"
#   role = "${aws_iam_role.myapp_ecs_role.id}"
#   // Policy type: Inline policy
#   // myappsGetEventsForECSTaskRule is AWS Managed Rule
#   policy = 
# }


// Allow ECS tasks to access private Image Registries
resource "aws_iam_policy" "allow_private_registry_auth" {
  name        = "task-policy-private-registry-auth"
  description = "Policy that allows access to private Image Repositories"
 
  policy = "${local.private_registry_policy}"

  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "allow_private_registry_auth" {
    role       = "${aws_iam_role.ecs_task_role.name}"
    policy_arn = "${aws_iam_policy.allow_private_registry_auth.arn}"
}