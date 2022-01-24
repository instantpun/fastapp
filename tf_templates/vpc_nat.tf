# Use NAT Gateway to allow machines inside a private subnet to communicate out to the internet
# example use cases:
# - OTA Updates
# - git clones
# nat gw
resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_nat_gateway" "nat-gw" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.main-public-1.id
  depends_on    = [aws_internet_gateway.main-gw]
}

# VPC setup for NAT
resource "aws_route_table" "main-private" {
  vpc_id = aws_vpc.main.id
  # create default route for traffic exiting the private network which maps to the NAT Gateway resource
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat-gw.id
  }

  tags = {
    Name = "main-private-1"
  }
}

# route associations private
resource "aws_route_table_association" "main-private-1-a" {
  subnet_id      = aws_subnet.main-private-1.id
  route_table_id = aws_route_table.main-private.id
}

# resource "aws_route_table_association" "main-private-2-a" {
#   subnet_id      = aws_subnet.main-private-2.id
#   route_table_id = aws_route_table.main-private.id
# }

# resource "aws_route_table_association" "main-private-3-a" {
#   subnet_id      = aws_subnet.main-private-3.id
#   route_table_id = aws_route_table.main-private.id
# }

