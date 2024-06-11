import time
from Management import dut_objects
from flows import rstp_flow
from test_beds import test_bed_1
from mocks import mocks_rstp

dut4 = test_bed_1.DUT4
dut5 = test_bed_1.DUT5
dut6 = test_bed_1.DUT6

DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT5 = dut_objects.DUT_Objects_TestBed(dut5)
DUT6 = dut_objects.DUT_Objects_TestBed(dut6)

rstp_flow_ = rstp_flow.RSTPFlow()
rstp_mocks_ = mocks_rstp.rstp_mocks


class TestRSTPSuite1FA:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify RSTP (802.1W) root election #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        rstp_flow_.create_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.create_rstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.create_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT5, bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address,bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        # Change the bridge priority on DUT4

        DUT4.stp.add_rstp_bridge_priority(bridge_priority=rstp_mocks_["bridge_priority_to_set"])

        # Check the new Root Bridge

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="4096",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT5, bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address,bridge_id_priority="32768",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        # Remove the bridge-priority for VLAN 10 and check that DUT6

        DUT4.stp.remove_rstp_bridge_priority()

        # Check the Root Bridge

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT5, bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst",  port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.remove_rstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.remove_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify RSTP (802.1W) port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        rstp_flow_.create_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.create_rstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.create_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT5, bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v6value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                           DUT5.ports["x1value"], "Root", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        # Change the bridge priority on DUT4

        DUT4.stp.add_rstp_bridge_priority(bridge_priority="4096")

        # Check the new Root Bridge

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="4096",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT5, bridge_id=DUT5.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT4.mac_address, root_priority="4096")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        # Configure to cost on the Root Port of DUT6 so the port becomes ALTERNATE

        DUT6.stp.add_rstp_port_cost(port=DUT6.ports["v3"], cost="50000")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Designated", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Alternate", "128", "50000",
                                           DUT6.ports["x1value"], "Root", "128", "2000")


        # Remove the cost check that the first Port is back to be Root

        DUT6.stp.remove_rstp_port_cost(port=DUT6.ports["v3"])

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                           DUT4.ports["v6value"], "Designated", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                           DUT5.ports["x1value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                           DUT6.ports["x1value"], "Designated", "128", "2000")

        # Remove the Bridge Priority for DUT4

        DUT4.stp.remove_rstp_bridge_priority()

        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.remove_rstp_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        rstp_flow_.remove_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify RSTP (802.1W) port-priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT4 == FA-DUT6
        #

        rstp_flow_.create_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.create_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], "rst")

        # Check the Root Bridge of each DUT

        rstp_flow_.assert_rstp_bridge_and_root_id(DUT4, bridge_id=DUT4.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")
        rstp_flow_.assert_rstp_bridge_and_root_id(DUT6, bridge_id=DUT6.mac_address, bridge_id_priority="32768",
                                                        root_id=DUT6.mac_address, root_priority="32768")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v5value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "128", "2000")

        # Configure to port-priority on the Alternate Port of DUT6 so the remote port becomes Root on DUT4

        DUT6.stp.add_rstp_port_priority(port=DUT6.ports["v4"], port_priority="16")

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Alternate", "128", "2000",
                                           DUT4.ports["v5value"], "Root", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "16", "2000")

        # Remove the port-priority that the first Port is back to be Root on the remote DUT

        DUT6.stp.remove_rstp_port_priority(port=DUT6.ports["v4"])

        # Check the Ports Role of each DUT

        rstp_flow_.assert_rstp_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                           DUT4.ports["v5value"], "Alternate", "128", "2000")
        rstp_flow_.assert_rstp_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                           DUT6.ports["v4value"], "Designated", "128", "2000")

        print("########## Removing the config #############")

        rstp_flow_.remove_rstp_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        rstp_flow_.remove_rstp_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], "rst")