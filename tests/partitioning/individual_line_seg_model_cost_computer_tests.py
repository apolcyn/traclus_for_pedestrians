'''
Created on Jan 9, 2016

@author: Alex
'''
import unittest
from tests.unit_base_tests import UnitBaseTests
from partitioning.trajectory_partitioning import individual_line_seg_model_cost_computer
import math

class IndividualLineSegModelCostComputerTest(UnitBaseTests):

    def test_get_cost_normal_case(self):
        line_seg = self.create_simple_line_seg(start=(0, 0), end=(1, 1))
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 1)
        
        line_seg = self.create_simple_line_seg(start=(0, 0), end=(4, 4))
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 3)

        line_seg = self.create_simple_line_seg(start=(1, 0), end=(1 + math.sqrt(3) + 0.1, 1))
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 2)
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 2)
        
        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 4.000001))
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 1) 
        
        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 4))
        self.assertEquals(individual_line_seg_model_cost_computer(line_seg), 0) 
        
    def test_get_cost_bad_inputs(self):
        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 3.99999))
        self.assertRaises(ValueError, individual_line_seg_model_cost_computer, line_seg) 

        line_seg = self.create_simple_line_seg(start=(2, 3), end=(2, 3))
        self.assertRaises(ValueError, individual_line_seg_model_cost_computer, line_seg) 
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()