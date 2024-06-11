import time
from Management import dut_objects
from flows import pvrst_flow
from test_beds import test_bed_1
from mocks import mocks_pvrst

dut4 = test_bed_1.DUT4
dut5 = test_bed_1.DUT5
dut6 = test_bed_1.DUT6

DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT5 = dut_objects.DUT_Objects_TestBed(dut5)
DUT6 = dut_objects.DUT_Objects_TestBed(dut6)

pvrst_flow_ = pvrst_flow.PVRSTFlow()
pvrst_mocks_ = mocks_pvrst.pvrst_mocks


class TestPVRSTSuite1FA:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify PVRST root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        pvrst_flow_.create_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "pvrst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.create_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                                       DUT4.ports["v6value"], "Alternate", "128", "2000",
                                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                                       DUT5.ports["x1value"], "Root", "128", "2000",
                                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                                       DUT6.ports["x1value"], "Designated", "128", "2000",
                                                       vlan="10")

        # Change the bridge priority on DUT4 for VLAN 10

        DUT4.stp.add_pvrst_bridge_priority(vlan="10", brg_priority="4096")

        # Check the new Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="4106",
                                                                     root_id=DUT4.mac_address, root_priority="4106")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="4106")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="4106")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                             DUT4.ports["v6value"], "Designated", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                             DUT5.ports["x1value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")

        # Remove the bridge-priority for VLAN 10 and check that DUT6 is the root for VLAN 10

        DUT4.stp.remove_pvrst_bridge_priority(vlan="10")

        # Check the Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                             DUT4.ports["v6value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                             DUT5.ports["x1value"], "Root", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")


        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.remove_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify PVRST root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        pvrst_flow_.create_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "pvrst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.create_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                                       DUT4.ports["v6value"], "Alternate", "128", "2000",
                                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                                       DUT5.ports["x1value"], "Root", "128", "2000",
                                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                                       DUT6.ports["x1value"], "Designated", "128", "2000",
                                                       vlan="10")

        # Change the bridge priority on DUT4 for VLAN 10

        DUT4.stp.add_prvst_root(vlan="10", root="primary")

        # Check the new Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="28682",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                             DUT4.ports["v6value"], "Designated", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                             DUT5.ports["x1value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")

        # Remove the Root Priority for VLAN 10 and check that DUT6 is the root for VLAN 10

        DUT4.stp.remove_pvrst_root(vlan="10")

        # Check the Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                             DUT4.ports["v6value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                             DUT5.ports["x1value"], "Root", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")


        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.remove_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify PVRST port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT4 -- DUT5
        #    \     /
        #     \   /
        #      FA-DUT6

        pvrst_flow_.create_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "pvrst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.create_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                             DUT4.ports["v6value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Designated", "128", "2000",
                                             DUT5.ports["x1value"], "Root", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")

        # Change the bridge priority on DUT4 for VLAN 10

        DUT4.stp.add_prvst_root(vlan="10", root="primary")

        # Check the new Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="28682",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT5, vlan="10", bridge_id=DUT5.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT4.mac_address, root_priority="28682")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                             DUT4.ports["v6value"], "Designated", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                             DUT5.ports["x1value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                             DUT6.ports["x1value"], "Designated", "128", "2000",
                                             vlan="10")

        # Configure to cost for VLAN 10 on the Root Port of DUT6 so the port becomes ALTERNATE

        DUT6.stp.add_pvrst_port_cost(vlan="10", port=DUT6.ports["v3"], cost="50000")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                       DUT4.ports["v6value"], "Designated", "128", "2000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                       DUT5.ports["x1value"], "Designated", "128", "2000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Alternate", "128", "50000",
                                       DUT6.ports["x1value"], "Root", "128", "2000",
                                       vlan="10")


        # Remove the cost for VLAN 10 and check that the first Port is back to be Root

        DUT6.stp.remove_pvrst_port_cost(vlan="10", port=DUT6.ports["v3"])

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Designated", "128", "2000",
                                       DUT4.ports["v6value"], "Designated", "128", "2000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT5, DUT5.ports["v4value"], "Root", "128", "2000",
                                       DUT5.ports["x1value"], "Alternate", "128", "2000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Root", "128", "2000",
                                       DUT6.ports["x1value"], "Designated", "128", "2000",
                                       vlan="10")

        # Remove the Root Priority for VLAN 10 on DUT4

        DUT4.stp.remove_pvrst_root(vlan="10")

        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v6"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.remove_pvrst_configuration(DUT5, [DUT5.ports["v4"], DUT5.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify PVRST port priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT4 == FA-DUT6
        #

        pvrst_flow_.create_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], "pvrst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.create_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT4, vlan="10", bridge_id=DUT4.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")
        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT6, vlan="10", bridge_id=DUT6.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT6.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                             DUT4.ports["v5value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["v4value"], "Designated", "128", "2000",
                                             vlan="10")

        # Configure to port-priority for VLAN 10 on the Alternate Port of DUT6 so the remote port becomes Root on DUT4

        DUT6.stp.add_pvrst_port_priority(vlan="10", port=DUT6.ports["v4"], port_priority="16")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Alternate", "128", "2000",
                                             DUT4.ports["v5value"], "Root", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["v4value"], "Designated", "16", "2000",
                                             vlan="10")


        # Remove the port-priority for VLAN 10 and check that the first Port is back to be Root on the remote DUT

        DUT6.stp.remove_pvrst_port_priority(vlan="10", port=DUT6.ports["v4"])

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT4, DUT4.ports["v4value"], "Root", "128", "2000",
                                             DUT4.ports["v5value"], "Alternate", "128", "2000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT6, DUT6.ports["v3value"], "Designated", "128", "2000",
                                             DUT6.ports["v4value"], "Designated", "128", "2000",
                                             vlan="10")

        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT4, [DUT4.ports["v4"], DUT4.ports["v5"]], ["10", "20", "30"], "rst", port_cambium_lab=DUT4.ports["x1"])
        pvrst_flow_.remove_pvrst_configuration(DUT6, [DUT6.ports["v3"], DUT6.ports["v4"]], ["10", "20", "30"], "rst")


    # def test_func_x(self):
    #
    #     print(pvrst_mocks_)
    #     print(pvrst_mocks_["default_bridge_priority"])
    #     print(pvrst_mocks_["bridge_priority_to_assert"])
    #     print(pvrst_mocks_["Port Roles"])
    #     print(pvrst_mocks_["Port Roles"]["Designated"])