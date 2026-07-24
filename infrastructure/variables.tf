variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tasktracker"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "westeurope"
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default = {
    Environment = "development"
    ManagedBy   = "terraform"
    Project     = "task-tracker"
  }
}