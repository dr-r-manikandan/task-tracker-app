output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Name of the created storage account"
  value       = azurerm_storage_account.main.name
}

output "location" {
  description = "Azure region of deployed resources"
  value       = azurerm_resource_group.main.location
}

output "vm_public_ip_address" {
  description = "Public IP address of the deployed VM"
  value       = azurerm_public_ip.main.ip_address
}

output "vm_ssh_command" {
  description = "SSH command to access the VM"
  value       = "ssh ${var.vm_admin_username}@${azurerm_public_ip.main.ip_address}"
}