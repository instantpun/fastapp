resource "aws_security_group" "allow-ssh" {
  vpc_id      = aws_vpc.main.id
  name        = "allow-ssh"
  description = "security group that allows ssh and all egress traffic"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    ipv6_cidr_blocks = ["2600:1700:2643:6770:612c:b288:ec7:e0fd/128"]
    cidr_blocks = ["68.95.98.6/32"] # best practice to only whitelist home/office IP
  }
  tags = {
    Name = "allow-ssh"
  }
}

