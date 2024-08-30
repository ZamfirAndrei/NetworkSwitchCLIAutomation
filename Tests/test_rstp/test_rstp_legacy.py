import time
from Management import dut_objects
from flows import rstp_flow
from test_beds import test_bed_1
from mocks import mocks_rstp

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

rstp_flow_ = rstp_flow.RSTPFlow()
rstp_mocks_ = mocks_rstp.rstp_mocks


class TestRSTPLegacy:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify RSTP (802.1W) root election #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        rstp_flow_.create_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.create_rstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.create_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT2, bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT3, bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT1, bridge_id=DUT1.mac_address,bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")

        # Change the bridge priority on DUT2

        DUT2.stp.add_rstp_bridge_priority(bridge_priority="4096")

        # Check the new Root Bridge

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT2, bridge_id=DUT2.mac_address, bridge_id_priority="4096",
                                                        root_id=DUT2.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT3, bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT2.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT1, bridge_id=DUT1.mac_address,bridge_id_priority="32768",
                                                        root_id=DUT2.mac_address, root_priority="4096")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Designated", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Root", "128", "20000",
                                           DUT3.ports["x1value"], "Alternate", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Root", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")

        # Remove the bridge-priority for DUT2

        DUT2.stp.remove_rstp_bridge_priority()

        # Check the Root Bridge

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT2, bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT3, bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT1, bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")

        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",  port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.remove_rstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.remove_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify RSTP (802.1W) port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        rstp_flow_.create_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                             port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.create_rstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.create_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT2, bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT3, bridge_id=DUT3.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT1, bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")

        # Configure to cost on the Root Port of DUT1 so the port becomes ALTERNATE

        DUT2.stp.add_rstp_port_cost(port=DUT2.ports["v1"], cost="50000")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "50000",
                                           DUT2.ports["h2value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Designated", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")

        # Remove the cost check that the first Port is back to be Root

        DUT2.stp.remove_rstp_port_cost(port=DUT2.ports["v1"])

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["h2value"], "Designated", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                           DUT3.ports["x1value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["x1value"], "Designated", "128", "20000")


        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                             port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.remove_rstp_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.remove_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")


    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify RSTP (802.1W) port-priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT2 == DUT1
        #

        rstp_flow_.create_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"], "rst",
                                                    port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.create_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT2, bridge_id=DUT2.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")
        rstp_flow_.assert_rstp_bridge_and_root_id(DUT1, bridge_id=DUT1.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT1.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["v2value"], "Alternate", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "128", "20000")

        # Configure to port-priority on the Alternate Port of DUT1 so the remote port becomes Root on DUT2

        DUT1.stp.add_rstp_port_priority(port=DUT1.ports["v2"], port_priority="16")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "20000",
                                           DUT2.ports["v2value"], "Root", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "16", "20000")

        # Remove the port-priority that the first Port is back to be Root on the remote DUT

        DUT1.stp.remove_rstp_port_priority(port=DUT1.ports["v2"])

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                           DUT2.ports["v2value"], "Alternate", "128", "20000")
        rstp_flow_.assert_rstp_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                           DUT1.ports["v2value"], "Designated", "128", "20000")

        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"], "rst",
                                                    port_cambium_lab=DUT2.ports["h3"])
        rstp_flow_.remove_rstp_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"], "rst")