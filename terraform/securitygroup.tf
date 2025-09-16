## Security group 

resource "azurerm_network_security_group" "nsg" {
  name                = "securitygroup-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "AllowAnySSHInbound"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"   # ⚠️ Allows from all internet
    destination_address_prefix = "*"
  }
   security_rule {
    name                       = "AllowAnyCustom2222Inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "2222"
    source_address_prefix      = var.residential_ip
    destination_address_prefix = "*"
  }
}



resource "azurerm_network_interface_security_group_association" "nic_nsg"{
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

