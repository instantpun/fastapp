locals {
  ecr_repo    = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.app_prefix}-repo"
  region      = "${data.aws_region.current.name}"
  log_group   = "${aws_cloudwatch_log_group.myapp_ecs_container_cloudwatch_loggroup.name}"
}

##################################################
# AWS Fargate
##################################################
resource "aws_ecs_cluster" "demo-fleet" {
  name = "${var.app_prefix}-ECSCluster"

  tags = var.common_tags
}

