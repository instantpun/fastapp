resource "aws_cloudwatch_log_group" "myapp_ecs_container_cloudwatch_loggroup" {
  name = "${var.app_prefix}-cloudwatch-log-group"

  tags = merge(
    var.common_tags,
    {
      Name        = "${var.app_prefix}-cloudwatch-log-group"
    }
  )
}

resource "aws_cloudwatch_log_stream" "myapp_ecs_container_cloudwatch_logstream" {
  name           = "${var.app_prefix}-cloudwatch-log-stream"
  log_group_name =  "${aws_cloudwatch_log_group.myapp_ecs_container_cloudwatch_loggroup.name}"
}