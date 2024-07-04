import time
from Management import dut_objects
from test_beds import test_bed_1


dut5 = test_bed_1.DUT5
dut7 = test_bed_1.DUT7
dut8 = test_bed_1.DUT8

DUT5 = dut_objects.DUT_Objects_TestBed(dut5)
DUT7 = dut_objects.DUT_Objects_TestBed(dut7)
DUT8 = dut_objects.DUT_Objects_TestBed(dut8)


class TestPerformanceSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")

        while True:

            DUT5.int.shut_interfaces(DUT5.ports["x3"], DUT5.ports["x4"])
            time.sleep(2)
            DUT5.int.no_shut_interfaces(DUT5.ports["x3"], DUT5.ports["x4"])
            time.sleep(5)