resource "aws_security_group" "alb_sg" {
  name        = "alb_sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.app_vpc.id

  tags = {
    Name = "alb_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_internet_http" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_out_alb" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_security_group" "ecs_sg" {
  name        = "ecs security group"
  description = "Allow inbound traffic from ALB to the ECS instances"
  vpc_id      = aws_vpc.app_vpc.id

  tags = {
    Name = "ECS Security Group"
  }
}
resource "aws_vpc_security_group_ingress_rule" "ecs_sg" {
  security_group_id            = aws_security_group.ecs_sg.id
  referenced_security_group_id = aws_security_group.alb_sg.id
  from_port                    = 8000
  ip_protocol                  = "tcp"
  to_port                      = 8000
}
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_out_ecs" {
  security_group_id = aws_security_group.ecs_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_security_group" "rds_sg" {
  name        = "rds security group"
  description = "Allow traffic only from the Web App to the Postgres database"
  vpc_id      = aws_vpc.app_vpc.id

  tags = {
    Name = "RDS Security Group"
  }
}
resource "aws_vpc_security_group_ingress_rule" "rds_sg" {
  security_group_id            = aws_security_group.rds_sg.id
  referenced_security_group_id = aws_security_group.ecs_sg.id
  from_port                    = 5432
  ip_protocol                  = "tcp"
  to_port                      = 5432
}
resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_out_rds" {
  security_group_id = aws_security_group.rds_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

