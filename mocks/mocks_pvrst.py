
Port_Roles = {

    "Root": "Root",
    "Alternate": "Alternate",
    "Designated": "Designated",
    "Disabled": "Disabled"
}

pvrst_mocks = {

    "vlan": "10",
    "vlans": ["10", "20", "30"],
    "default_stp_mode": "rst",
    "stp_mode": "pvrst",
    "default_bridge_priority": "32768",
    "bridge_priority_to_set": "4096",
    "bridge_priority_to_assert": "4096",
    "root_primary": "primary",
    "root_secondary": "secondary",
    "default_cost": "128",
    "cost_to_set": "50000",
    "default_port_priority": "128",
    "port_priority_to_set": "16",
    "Port Roles": Port_Roles

}

# print(pvrst_mocks)
pvrst_mocks["default_bridge_priority"] = str(int(pvrst_mocks["default_bridge_priority"]) + int(pvrst_mocks["vlan"]))
pvrst_mocks["bridge_priority_to_assert"] = str(int(pvrst_mocks["bridge_priority_to_assert"]) + int(pvrst_mocks["vlan"]))
# print(pvrst_mocks)