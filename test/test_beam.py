import unittest

import numpy as np

from source.node import Node
from source.beam.beam import BeamElement


class TestBeam(unittest.TestCase):

    def setUp(self):
        self.i = Node(0, 0)
        self.j = Node(1, 0)
        self.e1 = BeamElement(self.i, self.j, A=1, I=2, E=1, ro=1)

    def test_length(self):
        self.assertEqual(self.e1.a, 0.5)

    def test_shape_functions(self):
        # Test the base functions at specific points
        # this shows that the N3 function is correct
        x = -1.0
        self.assertAlmostEqual(self.e1.base_functions(x)[0], 1)
        self.assertAlmostEqual(self.e1.base_functions(x)[2], 0)
        x = 1.0
        self.assertAlmostEqual(self.e1.base_functions(x)[0], 0)
        self.assertAlmostEqual(self.e1.base_functions(x)[2], 1)

        xs = list(np.linspace(-1, 1, 5))
        for x in xs:
            bf = self.e1.base_functions(x)
            self.assertAlmostEqual(bf[0] + bf[2], 1)

    def test_element_stiffness_matrix(self):
        ke = self.e1.ke
        np.testing.assert_allclose(ke, ke.T)  # Check symmetry

    def test_element_mass_matrix(self):
        me = self.e1.me
        np.testing.assert_allclose(me, me.T)  # Check symmetry


if __name__ == '__main__':
    unittest.main()
