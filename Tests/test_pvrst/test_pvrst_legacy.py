import time
from Management import dut_objects
from flows import pvrst_flow
from test_beds import test_bed_1
from mocks import mocks_pvrst

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

pvrst_flow_ = pvrst_flow.PVRSTFlow()
pvrst_mocks_ = mocks_pvrst.pvrst_mocks


class TestPVRSTLegacy:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify PVRST root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        pvrst_flow_.create_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "pvrst",
                                                      port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.create_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        # Change the bridge priority on DUT2 for VLAN 10

        DUT2.stp.add_pvrst_bridge_priority(vlan="10", brg_priority="4096")

        # Check the new Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="4106",
                                                                     root_id=DUT2.mac_address, root_priority="4106")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT2.mac_address, root_priority="4106")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT2.mac_address, root_priority="4106")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Designated", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Root", "128", "20000",
                                             DUT3.ports["x1value"], "Alternate", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Root", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        # Remove the bridge-priority for VLAN 10 and check that DUT1 is the root for VLAN 10

        DUT2.stp.remove_pvrst_bridge_priority(vlan="10")

        # Check the Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")


        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                                      port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.remove_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify PVRST root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        pvrst_flow_.create_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "pvrst",
                                               port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.create_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        # Change the bridge priority on DUT2 for VLAN 10

        DUT2.stp.add_prvst_root(vlan="10", root="primary")

        # Check the new Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="28682",
                                                                     root_id=DUT2.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT2.mac_address, root_priority="28682")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT2.mac_address, root_priority="28682")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Designated", "128", "20000",
                                       DUT2.ports["h2value"], "Designated", "128", "20000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Root", "128", "20000",
                                       DUT3.ports["x1value"], "Alternate", "128", "20000",
                                       vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Root", "128", "20000",
                                       DUT1.ports["x1value"], "Designated", "128", "20000",
                                       vlan="10")

        # Remove the Root Priority for VLAN 10 and check that DUT1 is the root for VLAN 10

        DUT2.stp.remove_pvrst_root(vlan="10")

        # Check the Root Bridge

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                               port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.remove_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify PVRST port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT2 -- DUT3
        #    \     /
        #     \   /
        #      DUT1

        pvrst_flow_.create_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "pvrst",
                                               port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.create_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "pvrst")
        pvrst_flow_.create_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT3, vlan="10", bridge_id=DUT3.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        # Configure to cost for VLAN 10 on the Root Port of DUT1 so the port becomes ALTERNATE

        DUT2.stp.add_pvrst_port_cost(vlan="10", port=DUT2.ports["v1"], cost="50000")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "50000",
                                             DUT2.ports["h2value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Designated", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1,DUT1.ports["v1value"], "Designated", "128", "20000",
                                            DUT1.ports["x1value"], "Designated", "128", "20000",
                                            vlan="10")

        # Remove the cost for VLAN 10 and check that the first Port is back to be Root

        DUT2.stp.remove_pvrst_port_cost(vlan="10", port=DUT2.ports["v1"])

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["h2value"], "Designated", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT3, DUT3.ports["h2value"], "Alternate", "128", "20000",
                                             DUT3.ports["x1value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["x1value"], "Designated", "128", "20000",
                                             vlan="10")

        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["h2"]], ["10", "20", "30"], "rst",
                                               port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.remove_pvrst_configuration(DUT3, [DUT3.ports["h2"], DUT3.ports["x1"]], ["10", "20", "30"], "rst")
        pvrst_flow_.remove_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["x1"]], ["10", "20", "30"], "rst")


    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify PVRST port priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT2 == DUT1
        #

        pvrst_flow_.create_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"], "pvrst",
                                                      port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.create_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"], "pvrst")

        # Check the Root Bridge of each DUT

        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT2, vlan="10", bridge_id=DUT2.mac_address, bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")
        pvrst_flow_.assert_pvrst_bridge_and_root_id(DUT1, vlan="10", bridge_id=DUT1.mac_address,bridge_id_priority="32778",
                                                                     root_id=DUT1.mac_address, root_priority="32778")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["v2value"], "Alternate", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["v2value"], "Designated", "128", "20000",
                                             vlan="10")

        # Configure to port-priority for VLAN 10 on the Alternate Port of DUT1 so the remote port becomes Root on DUT2

        DUT1.stp.add_pvrst_port_priority(vlan="10", port=DUT1.ports["v2"], port_priority="16")

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Alternate", "128", "20000",
                                             DUT2.ports["v2value"], "Root", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["v2value"], "Designated", "16", "20000",
                                             vlan="10")


        # Remove the port-priority for VLAN 10 and check that the first Port is back to be Root on the remote DUT

        DUT1.stp.remove_pvrst_port_priority(vlan="10", port=DUT1.ports["v2"])

        # Check the Ports Role of each DUT

        pvrst_flow_.assert_pvrst_ports(DUT2, DUT2.ports["v1value"], "Root", "128", "20000",
                                             DUT2.ports["v2value"], "Alternate", "128", "20000",
                                             vlan="10")
        pvrst_flow_.assert_pvrst_ports(DUT1, DUT1.ports["v1value"], "Designated", "128", "20000",
                                             DUT1.ports["v2value"], "Designated", "128", "20000",
                                             vlan="10")

        print("########## Removing the config #############")

        pvrst_flow_.remove_pvrst_configuration(DUT2, [DUT2.ports["v1"], DUT2.ports["v2"]], ["10", "20", "30"], "rst",
                                                      port_cambium_lab=DUT2.ports["h3"])
        pvrst_flow_.remove_pvrst_configuration(DUT1, [DUT1.ports["v1"], DUT1.ports["v2"]], ["10", "20", "30"], "rst")


    # def test_func_x(self):
    #
    #     print(pvrst_mocks_)
    #     print(pvrst_mocks_["default_bridge_priority"])
    #     print(pvrst_mocks_["bridge_priority_to_assert"])
    #     print(pvrst_mocks_["Port Roles"])
    #     print(pvrst_mocks_["Port Roles"]["Designated"])