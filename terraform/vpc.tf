resource "aws_vpc" "app_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "cup-app-vpc"
  }
}

resource "aws_subnet" "public1a" {
  vpc_id                  = aws_vpc.app_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
  tags = {
    Name = "cup-app-public-1a"
  }
}
resource "aws_subnet" "public1b" {
  vpc_id                  = aws_vpc.app_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1b"
  tags = {
    Name = "cup-app-public-1b"
  }
}
resource "aws_subnet" "private1a" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "cup-app-private-1a"
  }
}
resource "aws_subnet" "private1b" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "us-east-1b"
  tags = {
    Name = "cup-app-private-1b"
  }
}

resource "aws_internet_gateway" "app_igw" {
  vpc_id = aws_vpc.app_vpc.id

  tags = {
    Name = "IGW"
  }
}

resource "aws_route_table" "app_route_table" {
  vpc_id = aws_vpc.app_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.app_igw.id
  }
  tags = {
    Name = "cup-app-public-route-table"
  }
}

resource "aws_route_table_association" "rta_public1a" {
  subnet_id      = aws_subnet.public1a.id
  route_table_id = aws_route_table.app_route_table.id
}
resource "aws_route_table_association" "rta_public1b" {
  subnet_id      = aws_subnet.public1b.id
  route_table_id = aws_route_table.app_route_table.id
}