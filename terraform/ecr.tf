resource "aws_ecr_repository" "cup_app" {
  name = "cup-app"
  image_tag_mutability = "MUTABLE"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}