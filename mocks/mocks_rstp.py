Port_Roles = {

    "Root": "Root",
    "Alternate": "Alternate",
    "Designated": "Designated",
    "Disabled": "Disabled"
}

rstp_mocks = {

    "vlan": "10",
    "vlans": ["10", "20", "30"],
    "default_stp_mode": "rst",
    "stp_mode": "rst",
    "default_bridge_priority": "32768",
    "bridge_priority_to_set": "4096",
    "bridge_priority_to_assert": "4096",
    "default_cost": "128",
    "cost_to_set": "50000",
    "default_port_priority": "128",
    "port_priority_to_set": "16",
    "Port Roles": Port_Roles

}

# print(rstp_mocks)