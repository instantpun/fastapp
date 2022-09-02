resource "aws_ecs_task_definition" "demo_fastapi" {
  family                   = "${var.app_prefix}"
  task_role_arn            = "${aws_iam_role.ecs_task_role.arn}"
  execution_role_arn       = "${aws_iam_role.ecs_task_execution_role.arn}"
  
  // Integrate with AWS Fargate
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu                      = "512"
  memory                   = "1024"
  container_definitions = <<EOF
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
        {"name": "REGION", "value": "${local.region}"}
    ]
  }
]
EOF

}

# resource "aws_ecs_service" "demo_fastapi" {
#  name                               = "${var.app_prefix}"
#  cluster                            = aws_ecs_cluster.demo_fleet.id
#  task_definition                    = aws_ecs_task_definition.demo_fastapi.arn
#  desired_count                      = 2
#  deployment_minimum_healthy_percent = 50
#  deployment_maximum_percent         = 200
#  launch_type                        = "FARGATE"
#  scheduling_strategy                = "REPLICA"
 
#  network_configuration {
#    security_groups  = var.ecs_service_security_groups
#    subnets          = var.subnets.*.id
#    assign_public_ip = false
#  }
 
#  load_balancer {
#    target_group_arn = var.aws_alb_target_group_arn
#    container_name   = "${var.name}-container-${var.environment}"
#    container_port   = var.container_port
#  }
 
#  lifecycle {
#    ignore_changes = [task_definition, desired_count]
#  }
# }

