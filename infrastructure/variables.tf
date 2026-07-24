variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tasktracker"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
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

variable "vnet_address_space" {
  description = "Address space for the virtual network"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "subnet_address_prefixes" {
  description = "Address prefixes for the subnet"
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

variable "allowed_ssh_cidrs" {
  description = "CIDR blocks allowed to SSH into the VM"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "vm_size" {
  description = "Azure VM SKU"
  type        = string
  default     = "Standard_B1s"
}

variable "vm_admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "vm_admin_ssh_public_key" {
  description = "SSH public key for VM admin access"
  type        = string
  sensitive   = true
}