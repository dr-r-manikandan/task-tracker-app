output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.main.name
}

output "location" {
  description = "Azure region of deployed resources"
  value       = azurerm_resource_group.main.location
}

output "container_app_url" {
  description = "URL of the deployed container app"
  value       = "https://${azurerm_container_app.main.latest_revision_fqdn}"
}

output "acr_login_server" {
  description = "ACR login server for Docker pushes"
  value       = azurerm_container_registry.main.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.main.admin_username
  sensitive   = true
}

output "acr_admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}

output "container_app_name" {
  description = "Name of the container app"
  value       = azurerm_container_app.main.name
}