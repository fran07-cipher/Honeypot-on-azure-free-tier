## ressource group

variable "ressource_group_hostname" {
    type = string
    default = "Cybersec-homelab"
}

variable "ressource_group_region" {
    type = string
    default = "East US 2"
}


## Network 

variable "azure_virtual_network_name" {
    type = string
    default = "Cybersecurity-homelab"
  
}

variable "azure_virtual_network_address_range" {
    type = list(string)
    default = ["10.0.0.0/24"]
}

variable "azure_virtual_subnet_prefix" {
    type = list(string)
    default = [ "10.0.0.0/28" ]
}

variable "public_ip_name" {
    type = string
    default = "cybersec-homelab-ip"
  
}

variable "public_ip_allocation_method" {
    type = string
    default = "Static"
  
}

variable "public_ip_sku" {
    type = string
    default = "Standard"
}



variable "nic_name" {
    type = string
    default = "cybersec-homelab-nic"
  
}

variable "ip_config_name" {
    type = string
    default = "internal"
  
}

variable "ip_private_allocation" {
    type = string
    default = "Dynamic"
  
}


## VM config

variable "vm_name" {
    type = string
    default = "cybersec-homelab-vm"  
}


variable "vm_size" {
    type = string
    default = "Standard_B1s"

}

variable "vm_admin_user" {
    type = string
    default = "azureuser"
  
}



variable "vm_os_disk_name" {
    type = string
    default = "cybersec-homelab-osdisk"
  
}

variable "vm_os_disk_storage_account_type" {
    type = string
    default = "Standard_LRS"
}



variable "vm_disk_size" {
    description = "Must be <=64GB for free tier"
    type = number
    default = 30
  
}


variable "vm_image" {
    type = string

    default = "0001-com-ubuntu-server-focal"
  
}

variable "vm_image_sku" {

    type = string
    default = "20_04-lts"
  
}

variable "vm_version" {
    type = string
    default = "latest"
  
}

variable "vm_availibility_zone"{
    type = number
    default = 2
}  


## Security group 

variable "residential_ip" {
    type = string
    default = "x.x.x.x/32"
  
}
