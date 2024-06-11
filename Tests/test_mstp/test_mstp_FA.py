import time
from Management import dut_objects
from flows import mstp_flow
from test_beds import test_bed_1


dut4 = test_bed_1.DUT4
dut5 = test_bed_1.DUT5
dut6 = test_bed_1.DUT6

DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT5 = dut_objects.DUT_Objects_TestBed(dut5)
DUT6 = dut_objects.DUT_Objects_TestBed(dut6)

mstp_flow_ = mstp_flow.MSTPFlow()



class TestMSTPSuite1FA:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify MSTP (802.1S) root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        mstp_flow_.create_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], ["1"],"mst", "Reg1", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.create_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], ["1"],"mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], ["1"],"mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4,  instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5,  instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Change the bridge priority on DUT4 for Instance 1

        DUT4.stp.add_mst_priority(instance="1", priority="4096")

        # Check the new Root Bridge

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="4096",
                                                                      root_id=DUT4.mac_address, root_priority="4096")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="4096")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="4096")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Remove the bridge-priority for Instance 1 and check that DUT6 (FA) is the root for Instance 1

        DUT4.stp.remove_mst_priority(instance="1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4,  instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5,  instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6,  instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.remove_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify MSTP (802.1S) port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        mstp_flow_.create_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.create_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Change the bridge priority on DUT4 for Instance 1

        DUT4.stp.add_mst_root_primary_secondary(instance="1", root="primary")

        # Check the new Root Bridge

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="24576",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Configure to cost for instance 1 on the Root Port of DUT6 so the port becomes ALTERNATE

        DUT6.stp.add_mst_port_cost(instance="1", port=DUT6.ports["v3"], cost="50000")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Alternate", "128", "50000",
                                           DUT6.ports["x1value"], "Root", "128", "2000",
                                           instance="1")

        # Remove the cost for Instance 1 and check that the first Port is back to be Root for Instance 1

        DUT6.stp.remove_mst_port_cost(instance="1", port=DUT6.ports["v3"])

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Remove the root priority for Instance 1 and check that DUT6 (FA) is the root for Instance 1

        DUT4.stp.remove_mst_root_primary_secondary(instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.remove_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")


    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify MSTP (802.1S) port priority functionality #############")
        print("###### 2 DUTs ######")


        #    Topology
        #
        #  DUT4 == FA-DUT6
        #

        mstp_flow_.create_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.create_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address,bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")
        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address,bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v5value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "128", "2000",
                                           instance="1")

        # Configure to port-priority for Instance 1 on the Alternate Port of DUT6 so the remote port becomes Root on DUT4

        DUT6.stp.add_mst_port_priority(instance="1", port=DUT6.ports["v4"], port_priority="16")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Alternate", "128", "2000",
                                           DUT4.ports["v5value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "16", "2000",
                                           instance="1")

        # Remove the port-priority for Instance 1 and check that the first Port is back to be Root on the remote DUT

        DUT6.stp.remove_mst_port_priority(instance="1", port=DUT6.ports["v4"])

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v5value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "128", "2000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.remove_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], "rst")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify MSTP (802.1S) root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        mstp_flow_.create_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.create_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], ["1"],
                                             "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address,bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Change the bridge priority on DUT4 for Instance 1

        DUT4.stp.add_mst_root_primary_secondary(instance="1", root="primary")

        # Check the new Root Bridge

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address, bridge_id_priority="24576",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT4.mac_address, root_priority="24576")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")

        # Remove the root priority for Instance 1 and check that DUT6 (FA) is the root for Instance 1

        DUT4.stp.remove_mst_root_primary_secondary(instance="1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT4, instance="1", bridge_id=DUT4.mac_address,  bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT5, instance="1", bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT6, instance="1", bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000",
                                           instance="1")


        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        mstp_flow_.remove_mstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

