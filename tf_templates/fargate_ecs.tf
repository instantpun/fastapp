locals {
  ecr_repo    = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.app_prefix}-repo"
  region      = "${data.aws_region.current.name}"
  log_group   = "${aws_cloudwatch_log_group.myapp_ecs_container_cloudwatch_loggroup.name}"
}

##################################################
# AWS Fargate
##################################################
resource "aws_ecs_cluster" "myapp_ecs_cluster" {
  name = "${var.app_prefix}-ECSCluster"

  tags = {
    Name = "${var.app_prefix}-ecs-fargate-cluster"
  }
}

resource "aws_ecs_task_definition" "myapp_ecs_task_definition" {
  family                   = "${var.app_prefix}-ECSTaskDefinition"
  task_role_arn            = "${aws_iam_role.myapp_ecs_task_role.arn}"
  execution_role_arn       = "${aws_iam_role.myapp_ecs_task_execution_role.arn}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  container_definitions = <<DEFINITION
[
  {
    "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "${local.log_group}",
            "awslogs-region": "${local.region}",
            "awslogs-stream-prefix": "/aws/ecs"
          }
        },
    "cpu":0,
    "dnsSearchDomains":[],
    "dnsServers":[],
    "dockerLabels":{},
    "dockerSecurityOptions":[],
    "essential":true,
    "extraHosts":[],
    "image": "${local.ecr_repo}",
    "links":[],
    "mountPoints":[],
    "name": "fargate-app",
    "portMappings":[
      {
        "containerPort": 80,
        "hostPort":80,
        "protocol": "tcp"
      }
    ],
    "ulimits":[],
    "volumesFrom":[],
    "environment": [
        {"name": "REGION", "value": "${local.region}"},
    ]
  }
]
DEFINITION
}