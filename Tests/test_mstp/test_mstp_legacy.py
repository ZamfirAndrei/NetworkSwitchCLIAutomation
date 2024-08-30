import time
from Management import dut_objects
from flows import mstp_flow
from test_beds import test_bed_1


dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

mstp_flow_ = mstp_flow.MSTPFlow()



class TestMSTPLegacy:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify MSTP (802.1S) root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        mstp_flow_.create_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"],
                                             ["1"],"mst", "Reg1", port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.create_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"],
                                             ["1"],"mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"],
                                             ["1"],"mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2,  instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3,  instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Change the bridge priority on DUT2 for Instance 1

        DUT2.stp.add_mst_priority(instance="1", priority="4096")

        # Check the new Root Bridge

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="4096",
                                                                      root_id=DUT2.mac_address, root_priority="4096")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3, instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT2.mac_address, root_priority="4096")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT2.mac_address, root_priority="4096")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Designated", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Root", "128", "20000",
                                           DUT3.ports["x1value"], "Alternate", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Root", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Remove the bridge-priority for Instance 1 and check that DUT2 is the root for Instance 1

        DUT2.stp.remove_mst_priority(instance="1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2,  instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3,  instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1,  instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                       root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                                    port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.remove_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify MSTP (802.1S) port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        mstp_flow_.create_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1", port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.create_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3, instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Configure to cost for instance 1 on the Root Port of DUT2 so the port becomes ALTERNATE

        DUT2.stp.add_mst_port_cost(instance="1", port=DUT2.ports["v1"], cost="50000")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "50000",
                                           DUT2.ports["h2value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Designated", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Remove the cost for Instance 1 and check that the first Port is back to be Root for Instance 1

        DUT2.stp.remove_mst_port_cost(instance="1", port=DUT2.ports["v1"])

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                                    port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.remove_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")


    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify MSTP (802.1S) port priority functionality #############")
        print("###### 2 DUTs ######")


        #    Topology
        #
        #  DUT2 == DUT1
        #

        mstp_flow_.create_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"],
                                             ["1"],"mst", "Reg1", port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.create_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address,bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")
        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address,bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["v2value"], "Alternate", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "128", "20000",
                                           instance="1")

        # Configure to port-priority for Instance 1 on the Alternate Port of DUT1 so the remote port becomes Root on DUT2

        DUT1.stp.add_mst_port_priority(instance="1", port=DUT1.ports["v2"], port_priority="16")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "20000",
                                           DUT2.ports["v2value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "16", "20000",
                                           instance="1")

        # Remove the port-priority for Instance 1 and check that the first Port is back to be Root on the remote DUT

        DUT1.stp.remove_mst_port_priority(instance="1", port=DUT1.ports["v2"])

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["v2value"], "Alternate", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "128", "20000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"],
                                                   "rst", port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.remove_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"],
                                                   "rst")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify MSTP (802.1S) root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        mstp_flow_.create_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1", port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.create_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1")
        mstp_flow_.create_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"],
                                             ["1"], "mst", "Reg1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3, instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Change the bridge priority on DUT2 for Instance 1

        DUT2.stp.add_mst_root_primary_secondary(instance="1", root="primary")

        # Check the new Root Bridge

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="24576",
                                                                      root_id=DUT2.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3, instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT2.mac_address, root_priority="24576")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT2.mac_address, root_priority="24576")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Designated", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Root", "128", "20000",
                                           DUT3.ports["x1value"], "Alternate", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Root", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        # Remove the root priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT2.stp.remove_mst_root_primary_secondary(instance="1")

        # Check the Root Bridge of each DUT

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT2, instance="1", bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT3, instance="1", bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        mstp_flow_.assert_mstp_bridge_and_root_id(DUT1, instance="1", bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                                      root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        mstp_flow_.assert_mstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000",
                                           instance="1")
        mstp_flow_.assert_mstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000",
                                           instance="1")

        print("########## Removing the config #############")

        mstp_flow_.remove_mstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                             port_cambium_lab=DUT2.ports["h3"])
        mstp_flow_.remove_mstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        mstp_flow_.remove_mstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

