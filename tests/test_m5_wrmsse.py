import unittest
import m5_wrmsse
import numpy as np

class TestWrmsse(unittest.TestCase):

    def test_m5_wrmsse(self):
        self.assertAlmostEqual(
            m5_wrmsse.wrmsse(np.zeros((30490,28))),
            5.446462854,
            places = 8,
            )
        self.assertAlmostEqual(
            m5_wrmsse.wrmsse(np.ones((30490,28))),
            2.563051076,
            places = 8,
            )
        self.assertRaises(TypeError, m5_wrmsse.wrmsse, 'string')       
        self.assertRaises(ValueError, m5_wrmsse.wrmsse, []) 


if __name__ == '__main__':
    unittest.main()
                             
