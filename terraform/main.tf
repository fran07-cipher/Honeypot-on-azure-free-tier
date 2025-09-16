# -------------------------
# 1. Resource Group (Free)
# -------------------------
resource "azurerm_resource_group" "rg" {
  name     = var.ressource_group_hostname
  location = var.ressource_group_region
}

# -------------------------
# 2. Virtual Network (Free)
# -------------------------
resource "azurerm_virtual_network" "vnet" {
  name                = var.azure_virtual_network_name
  address_space       = var.azure_virtual_network_address_range
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# -------------------------
# 3. Subnet (Free)
# -------------------------
resource "azurerm_subnet" "subnet" {
  name                 = var.ressource_group_hostname
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.azure_virtual_subnet_prefix
}

# -------------------------
# 4. Public IP (Dynamic = Free)
# -------------------------
resource "azurerm_public_ip" "public_ip" {
  name                = var.public_ip_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = var.public_ip_allocation_method # Dynamic is free, static costs money
  sku                 = var.public_ip_sku
}

# -------------------------
# 5. Network Interface (Free)
# -------------------------
resource "azurerm_network_interface" "nic" {
  name                = var.nic_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = var.ip_config_name
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = var.ip_private_allocation
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

# -------------------------
# 6. Virtual Machine (Free if B1s + <=64GB disk)
# -------------------------
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = var.vm_size # Free tier eligible
  admin_username      = var.vm_admin_user

  # Use your SSH public key
  admin_ssh_key {
    username   = var.vm_admin_user
    public_key = file("~/.ssh/id_rsa.pub")
  }

  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  os_disk {
    name                 = var.vm_os_disk_name
    caching              = "ReadWrite"
    storage_account_type = var.vm_os_disk_storage_account_type 
    disk_size_gb         = var.vm_disk_size           
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = var.vm_image
    sku       = var.vm_image_sku
    version   = var.vm_version
  }

  zone = var.vm_availibility_zone 
}





