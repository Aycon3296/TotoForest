from bisect import bisect_left, bisect_right
import unittest
from implements import BisectFinder

class TestBisectFinder(unittest.TestCase):
    def setUp(self):
        # 10
        self.empty_list = []
        
        # 2, 5, 7
        self.one_element_list = [5]
        
        # 2, 3, 6, 8, 9
        self.two_element_list = [3, 8]
        
        # 1, 2, 4, 7, 8
        self.three_element_list = [2, 7, 7]
        
        # 1, 2, 4, 5, 6
        self.four_element_list = [2, 2, 2, 5]
        
        # 0, 1, 2, 5, 7, 9, 10
        self.five_element_list = [1, 5, 5, 5, 9]


    # Tests for the find_left_lt function

    def test_find_left_lt_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.empty_list, 10)

    def test_find_left_lt_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.one_element_list, 2)
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.one_element_list, 5)
        self.assertEqual(BisectFinder.find_left_lt(self.one_element_list, 7), 0)

    def test_find_left_lt_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.two_element_list, 2)
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.two_element_list, 3)
        self.assertEqual(BisectFinder.find_left_lt(self.two_element_list, 6), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.two_element_list, 8), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.two_element_list, 9), 1)
        
    def test_find_left_lt_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.three_element_list, 1)
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.three_element_list, 2)
        self.assertEqual(BisectFinder.find_left_lt(self.three_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.three_element_list, 7), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.three_element_list, 8), 1)
        
    def test_find_left_lt_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.four_element_list, 1)
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.four_element_list, 2)
        self.assertEqual(BisectFinder.find_left_lt(self.four_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.four_element_list, 5), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.four_element_list, 6), 3)

    def test_find_left_lt_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.five_element_list, 0)
        self.assertRaises(ValueError, BisectFinder.find_left_lt, self.five_element_list, 1)
        self.assertEqual(BisectFinder.find_left_lt(self.five_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.five_element_list, 5), 0)
        self.assertEqual(BisectFinder.find_left_lt(self.five_element_list, 7), 1)
        self.assertEqual(BisectFinder.find_left_lt(self.five_element_list, 9), 1)
        self.assertEqual(BisectFinder.find_left_lt(self.five_element_list, 10), 4)


    # Tests for the find_left_le function

    def test_find_left_le_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.empty_list, 10)

    def test_find_left_le_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.one_element_list, 2)
        self.assertEqual(BisectFinder.find_left_le(self.one_element_list, 5), 0)
        self.assertEqual(BisectFinder.find_left_le(self.one_element_list, 7), 0)

    def test_find_left_le_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.two_element_list, 2)
        self.assertEqual(BisectFinder.find_left_le(self.two_element_list, 3), 0)
        self.assertEqual(BisectFinder.find_left_le(self.two_element_list, 6), 0)
        self.assertEqual(BisectFinder.find_left_le(self.two_element_list, 8), 1)
        self.assertEqual(BisectFinder.find_left_le(self.two_element_list, 9), 1)
        
    def test_find_left_le_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.three_element_list, 1)
        self.assertEqual(BisectFinder.find_left_le(self.three_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_le(self.three_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_left_le(self.three_element_list, 7), 1)
        self.assertEqual(BisectFinder.find_left_le(self.three_element_list, 8), 1)
        
    def test_find_left_le_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.four_element_list, 1)
        self.assertEqual(BisectFinder.find_left_le(self.four_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_le(self.four_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_left_le(self.four_element_list, 5), 3)
        self.assertEqual(BisectFinder.find_left_le(self.four_element_list, 6), 3)

    def test_find_left_le_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_le, self.five_element_list, 0)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 5), 1)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 7), 1)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 9), 4)
        self.assertEqual(BisectFinder.find_left_le(self.five_element_list, 10), 4)


    # Tests for the find_left_eq function

    def test_find_left_eq_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.empty_list, 10)

    def test_find_left_eq_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.one_element_list, 2)
        self.assertEqual(BisectFinder.find_left_eq(self.one_element_list, 5), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.one_element_list, 7)

    def test_find_left_eq_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.two_element_list, 2)
        self.assertEqual(BisectFinder.find_left_eq(self.two_element_list, 3), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.two_element_list, 6)
        self.assertEqual(BisectFinder.find_left_eq(self.two_element_list, 8), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.two_element_list, 9)
        
    def test_find_left_eq_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.three_element_list, 1)
        self.assertEqual(BisectFinder.find_left_eq(self.three_element_list, 2), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.three_element_list, 4)
        self.assertEqual(BisectFinder.find_left_eq(self.three_element_list, 7), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.three_element_list, 8)
        
    def test_find_left_eq_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.four_element_list, 1)
        self.assertEqual(BisectFinder.find_left_eq(self.four_element_list, 2), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.four_element_list, 4)
        self.assertEqual(BisectFinder.find_left_eq(self.four_element_list, 5), 3)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.four_element_list, 6)

    def test_find_left_eq_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.five_element_list, 0)
        self.assertEqual(BisectFinder.find_left_eq(self.five_element_list, 1), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.five_element_list, 2)
        self.assertEqual(BisectFinder.find_left_eq(self.five_element_list, 5), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.five_element_list, 7)
        self.assertEqual(BisectFinder.find_left_eq(self.five_element_list, 9), 4)
        self.assertRaises(ValueError, BisectFinder.find_left_eq, self.five_element_list, 10)


    # Tests for the find_left_ge function

    def test_find_left_ge_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.empty_list, 10)

    def test_find_left_ge_one_element_list(self):
        self.assertEqual(BisectFinder.find_left_ge(self.one_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.one_element_list, 5), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.one_element_list, 7)

    def test_find_left_ge_two_element_list(self):
        self.assertEqual(BisectFinder.find_left_ge(self.two_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.two_element_list, 3), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.two_element_list, 6), 1)
        self.assertEqual(BisectFinder.find_left_ge(self.two_element_list, 8), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.two_element_list, 9)

    def test_find_left_ge_three_element_list(self):
        self.assertEqual(BisectFinder.find_left_ge(self.three_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.three_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.three_element_list, 4), 1)
        self.assertEqual(BisectFinder.find_left_ge(self.three_element_list, 7), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.three_element_list, 8)
        
    def test_find_left_ge_four_element_list(self):
        self.assertEqual(BisectFinder.find_left_ge(self.four_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.four_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.four_element_list, 4), 3)
        self.assertEqual(BisectFinder.find_left_ge(self.four_element_list, 5), 3)
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.four_element_list, 6)
        
    def test_find_left_ge_five_element_list(self):
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 0), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 2), 1)
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 5), 1)
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 7), 4)
        self.assertEqual(BisectFinder.find_left_ge(self.five_element_list, 9), 4)
        self.assertRaises(ValueError, BisectFinder.find_left_ge, self.five_element_list, 10)


    # Tests for the find_left_gt function

    def test_find_left_gt_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.empty_list, 10)

    def test_find_left_gt_one_element_list(self):
        self.assertEqual(BisectFinder.find_left_gt(self.one_element_list, 2), 0)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.one_element_list, 5)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.one_element_list, 7)

    def test_find_left_gt_two_element_list(self):
        self.assertEqual(BisectFinder.find_left_gt(self.two_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_left_gt(self.two_element_list, 3), 1)
        self.assertEqual(BisectFinder.find_left_gt(self.two_element_list, 6), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.two_element_list, 8)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.two_element_list, 9)

    def test_find_left_gt_three_element_list(self):
        self.assertEqual(BisectFinder.find_left_gt(self.three_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_gt(self.three_element_list, 2), 1)
        self.assertEqual(BisectFinder.find_left_gt(self.three_element_list, 4), 1)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.three_element_list, 7)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.three_element_list, 8)
        
    def test_find_left_gt_four_element_list(self):
        self.assertEqual(BisectFinder.find_left_gt(self.four_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_left_gt(self.four_element_list, 2), 3)
        self.assertEqual(BisectFinder.find_left_gt(self.four_element_list, 4), 3)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.four_element_list, 5)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.four_element_list, 6)
    
    def test_find_left_gt_five_element_list(self):
        self.assertEqual(BisectFinder.find_left_gt(self.five_element_list, 0), 0)
        self.assertEqual(BisectFinder.find_left_gt(self.five_element_list, 1), 1)
        self.assertEqual(BisectFinder.find_left_gt(self.five_element_list, 2), 1)
        self.assertEqual(BisectFinder.find_left_gt(self.five_element_list, 5), 4)
        self.assertEqual(BisectFinder.find_left_gt(self.five_element_list, 7), 4)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.five_element_list, 9)
        self.assertRaises(ValueError, BisectFinder.find_left_gt, self.five_element_list, 10)


    # Tests for the find_right_lt function

    def test_find_right_lt_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.empty_list, 10)

    def test_find_right_lt_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.one_element_list, 2)
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.one_element_list, 5)
        self.assertEqual(BisectFinder.find_right_lt(self.one_element_list, 7), 0)

    def test_find_right_lt_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.two_element_list, 2)
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.two_element_list, 3)
        self.assertEqual(BisectFinder.find_right_lt(self.two_element_list, 6), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.two_element_list, 8), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.two_element_list, 9), 1)
        
    def test_find_right_lt_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.three_element_list, 1)
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.three_element_list, 2)
        self.assertEqual(BisectFinder.find_right_lt(self.three_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.three_element_list, 7), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.three_element_list, 8), 2)
        
    def test_find_right_lt_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.four_element_list, 1)
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.four_element_list, 2)
        self.assertEqual(BisectFinder.find_right_lt(self.four_element_list, 4), 2)
        self.assertEqual(BisectFinder.find_right_lt(self.four_element_list, 5), 2)
        self.assertEqual(BisectFinder.find_right_lt(self.four_element_list, 6), 3)

    def test_find_right_lt_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.five_element_list, 0)
        self.assertRaises(ValueError, BisectFinder.find_right_lt, self.five_element_list, 1)
        self.assertEqual(BisectFinder.find_right_lt(self.five_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.five_element_list, 5), 0)
        self.assertEqual(BisectFinder.find_right_lt(self.five_element_list, 7), 3)
        self.assertEqual(BisectFinder.find_right_lt(self.five_element_list, 9), 3)
        self.assertEqual(BisectFinder.find_right_lt(self.five_element_list, 10), 4)


    # Tests for the find_right_le function

    def test_find_right_le_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.empty_list, 10)

    def test_find_right_le_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.one_element_list, 2)
        self.assertEqual(BisectFinder.find_right_le(self.one_element_list, 5), 0)
        self.assertEqual(BisectFinder.find_right_le(self.one_element_list, 7), 0)

    def test_find_right_le_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.two_element_list, 2)
        self.assertEqual(BisectFinder.find_right_le(self.two_element_list, 3), 0)
        self.assertEqual(BisectFinder.find_right_le(self.two_element_list, 6), 0)
        self.assertEqual(BisectFinder.find_right_le(self.two_element_list, 8), 1)
        self.assertEqual(BisectFinder.find_right_le(self.two_element_list, 9), 1)
        
    def test_find_right_le_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.three_element_list, 1)
        self.assertEqual(BisectFinder.find_right_le(self.three_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_le(self.three_element_list, 4), 0)
        self.assertEqual(BisectFinder.find_right_le(self.three_element_list, 7), 2)
        self.assertEqual(BisectFinder.find_right_le(self.three_element_list, 8), 2)
        
    def test_find_right_le_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.four_element_list, 1)
        self.assertEqual(BisectFinder.find_right_le(self.four_element_list, 2), 2)
        self.assertEqual(BisectFinder.find_right_le(self.four_element_list, 4), 2)
        self.assertEqual(BisectFinder.find_right_le(self.four_element_list, 5), 3)
        self.assertEqual(BisectFinder.find_right_le(self.four_element_list, 6), 3)

    def test_find_right_le_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_le, self.five_element_list, 0)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 5), 3)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 7), 3)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 9), 4)
        self.assertEqual(BisectFinder.find_right_le(self.five_element_list, 10), 4)


    # Tests for the find_right_eq function

    def test_find_right_eq_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.empty_list, 10)

    def test_find_right_eq_one_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.one_element_list, 2)
        self.assertEqual(BisectFinder.find_right_eq(self.one_element_list, 5), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.one_element_list, 7)

    def test_find_right_eq_two_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.two_element_list, 2)
        self.assertEqual(BisectFinder.find_right_eq(self.two_element_list, 3), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.two_element_list, 6)
        self.assertEqual(BisectFinder.find_right_eq(self.two_element_list, 8), 1)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.two_element_list, 9)
        
    def test_find_right_eq_three_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.three_element_list, 1)
        self.assertEqual(BisectFinder.find_right_eq(self.three_element_list, 2), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.three_element_list, 4)
        self.assertEqual(BisectFinder.find_right_eq(self.three_element_list, 7), 2)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.three_element_list, 8)
        
    def test_find_right_eq_four_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.four_element_list, 1)
        self.assertEqual(BisectFinder.find_right_eq(self.four_element_list, 2), 2)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.four_element_list, 4)
        self.assertEqual(BisectFinder.find_right_eq(self.four_element_list, 5), 3)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.four_element_list, 6)

    def test_find_right_eq_five_element_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.five_element_list, 0)
        self.assertEqual(BisectFinder.find_right_eq(self.five_element_list, 1), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.five_element_list, 2)
        self.assertEqual(BisectFinder.find_right_eq(self.five_element_list, 5), 3)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.five_element_list, 7)
        self.assertEqual(BisectFinder.find_right_eq(self.five_element_list, 9), 4)
        self.assertRaises(ValueError, BisectFinder.find_right_eq, self.five_element_list, 10)


    # Tests for the find_right_ge function

    def test_find_right_ge_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.empty_list, 10)

    def test_find_right_ge_one_element_list(self):
        self.assertEqual(BisectFinder.find_right_ge(self.one_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.one_element_list, 5), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.one_element_list, 7)

    def test_find_right_ge_two_element_list(self):
        self.assertEqual(BisectFinder.find_right_ge(self.two_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.two_element_list, 3), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.two_element_list, 6), 1)
        self.assertEqual(BisectFinder.find_right_ge(self.two_element_list, 8), 1)
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.two_element_list, 9)

    def test_find_right_ge_three_element_list(self):
        self.assertEqual(BisectFinder.find_right_ge(self.three_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.three_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.three_element_list, 4), 2)
        self.assertEqual(BisectFinder.find_right_ge(self.three_element_list, 7), 2)
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.three_element_list, 8)
        
    def test_find_right_ge_four_element_list(self):
        self.assertEqual(BisectFinder.find_right_ge(self.four_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.four_element_list, 2), 2)
        self.assertEqual(BisectFinder.find_right_ge(self.four_element_list, 4), 3)
        self.assertEqual(BisectFinder.find_right_ge(self.four_element_list, 5), 3)
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.four_element_list, 6)

    def test_find_right_ge_five_element_list(self):
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 0), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 2), 3)
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 5), 3)
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 7), 4)
        self.assertEqual(BisectFinder.find_right_ge(self.five_element_list, 9), 4)
        self.assertRaises(ValueError, BisectFinder.find_right_ge, self.five_element_list, 10)


    # Tests for the find_right_gt function

    def test_find_right_gt_empty_list(self):
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.empty_list, 10)

    def test_find_right_gt_one_element_list(self):
        self.assertEqual(BisectFinder.find_right_gt(self.one_element_list, 2), 0)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.one_element_list, 5)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.one_element_list, 7)

    def test_find_right_gt_two_element_list(self):
        self.assertEqual(BisectFinder.find_right_gt(self.two_element_list, 2), 0)
        self.assertEqual(BisectFinder.find_right_gt(self.two_element_list, 3), 1)
        self.assertEqual(BisectFinder.find_right_gt(self.two_element_list, 6), 1)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.two_element_list, 8)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.two_element_list, 9)

    def test_find_right_gt_three_element_list(self):
        self.assertEqual(BisectFinder.find_right_gt(self.three_element_list, 1), 0)
        self.assertEqual(BisectFinder.find_right_gt(self.three_element_list, 2), 2)
        self.assertEqual(BisectFinder.find_right_gt(self.three_element_list, 4), 2)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.three_element_list, 7)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.three_element_list, 8)
        
    def test_find_right_gt_four_element_list(self):
        self.assertEqual(BisectFinder.find_right_gt(self.four_element_list, 1), 2)
        self.assertEqual(BisectFinder.find_right_gt(self.four_element_list, 2), 3)
        self.assertEqual(BisectFinder.find_right_gt(self.four_element_list, 4), 3)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.four_element_list, 5)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.four_element_list, 6)

    def test_find_right_gt_five_element_list(self):
        self.assertEqual(BisectFinder.find_right_gt(self.five_element_list, 0), 0)
        self.assertEqual(BisectFinder.find_right_gt(self.five_element_list, 1), 3)
        self.assertEqual(BisectFinder.find_right_gt(self.five_element_list, 2), 3)
        self.assertEqual(BisectFinder.find_right_gt(self.five_element_list, 5), 4)
        self.assertEqual(BisectFinder.find_right_gt(self.five_element_list, 7), 4)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.five_element_list, 9)
        self.assertRaises(ValueError, BisectFinder.find_right_gt, self.five_element_list, 10)


if __name__ == '__main__':
    unittest.main()
class BisectFinder:
    ''' Этот класс содержит все возможные функции бинарного поиска элемента в списке '''
        
    @staticmethod
    def find_left_lt(a, x):
        'Finds the index of the leftmost element that is strictly less than x'
        index = bisect_left(a, x)
        
        if index == len(a):
            if a[index - 1] < x:
                return index - 1
        elif index > 0:
            if a[index - 1] < x:
                return bisect_left(a, a[index - 1])
        else:
            raise ValueError
        

    @staticmethod
    def find_left_le(a, x):
        'Finds the index of the leftmost element that is less than or equal to x'
        index = bisect_left(a, x) - 1
        
        if index == len(a):
            if a[index - 1] < x:
                return index - 1
        elif index >= -1:
            if a[index] < x:
                return bisect_left(a, a[index])
        else:
            raise ValueError

    @staticmethod
    def find_left_eq(a, x):
        'Finds the index of the leftmost element that is equal to x'
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    @staticmethod
    def find_left_ge(a, x):
        'Finds the index of the leftmost element that is greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return i
        raise ValueError

    @staticmethod
    def find_left_gt(a, x):
        'Finds the index of the leftmost element that is strictly greater than x'
        i = bisect_right(a, x)
        if i != len(a):
            return i
        raise ValueError

    @staticmethod
    def find_right_lt(a, x):
        'Finds the index of the rightmost element that is strictly less than x'
        i = bisect_left(a, x)
        if i:
            return i-1
        raise ValueError

    @staticmethod
    def find_right_le(a, x):
        'Finds the index of the rightmost element that is less than or equal to x'
        i = bisect_right(a, x)
        if i:
            return i-1
        raise ValueError

    @staticmethod
    def find_right_eq(a, x):
        'Finds the index of the rightmost element that is equal to x'
        i = bisect_right(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    @staticmethod
    def find_right_ge(a, x):
        'Finds the index of the rightmost element that is greater than or equal to x'
        i = bisect_left(a, x)
        if i != len(a):
            return i
        raise ValueError

    @staticmethod
    def find_right_gt(a, x):
        'Finds the index of the rightmost element that is strictly greater than x'
        i = bisect_right(a, x)
        if i != len(a):
            return i
        raise ValueError
