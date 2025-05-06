variable "aws_region" {
  description = "AWS region to deploy into"
  default     = "eu-central-1" # Frankfurt
}

variable "ami_id" {
  description = "Ubuntu 22.04 LTS AMI for eu-central-1"
  default     = "ami-0faab6bdbac9486fb" # Ubuntu 22.04 LTS Version
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of the existing AWS key pair"
  default     = "mert-ec2-key"
}

variable "public_key_path" {
  description = "Path to your public SSH key"
  default = "/home/mert/.ssh/mert-ec2-key.pub"
}
