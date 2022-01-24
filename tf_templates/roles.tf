locals {
  iam_role_name       = "${var.app_prefix}-ECSRunTaskSyncExecutionRole"
  iam_policy_name     = "FargateTaskNotificationAccessPolicy"
  iam_task_role_policy_name = "${var.app_prefix}-ECS-Task-Role-Policy"
}

resource "aws_iam_role" "myapp_ecs_role" {
  name               = "${local.iam_role_name}"
  assume_role_policy = "${data.aws_iam_policy_document.myapp_ecs_policy_document.json}"
}


data "aws_iam_policy_document" "myapp_ecs_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "myapp_ecs_policy" {
  name = "${local.iam_policy_name}"
  role = "${aws_iam_role.myapp_ecs_role.id}"
  // Policy type: Inline policy
  // myappsGetEventsForECSTaskRule is AWS Managed Rule
  // policy = <<EOF
  // TODO
}

resource "aws_iam_role_policy_attachment" "myapp-ecs-role-policy-attachment" {
    role       = "${aws_iam_role.myapp_ecs_role.name}"
    // policy_arn = "arn:aws:iam::aws:policy/service-role/#TODO#"
}

resource "aws_iam_role" "myapp_ecs_task_role" {
  // #TODO
}

resource "aws_iam_role" "myapp_ecs_execution_role" {
  // #TODO
}
