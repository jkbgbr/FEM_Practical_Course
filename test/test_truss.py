import unittest

import numpy as np

from source.node import Node
from source.truss import TrussElement


class TestTruss(unittest.TestCase):

    def setUp(self):
        self.n1 = Node(0, 0, 0)
        self.n2 = Node(1, 0, 0)
        self.e1 = TrussElement(self.n1, self.n2, A=1, E=1, ro=1)

    def test_length(self):
        self.assertEqual(self.e1.length, 1.0)

    def test_shape_functions(self):
        x = 0.0
        np.testing.assert_allclose(self.e1.N(x), np.array([1.0, 0.0]))
        x = 1.0
        np.testing.assert_allclose(self.e1.N(x), np.array([0.0, 1.0]))

        x = 0.5
        N = self.e1.N(x)
        self.assertAlmostEqual(N[0], 0.5)
        self.assertAlmostEqual(N[1], 0.5)

        with self.assertRaises(AssertionError):
            self.e1._N1(-0.1)

    def test_element_stiffness_matrix(self):
        ke = self.e1.ke
        expected_ke = np.array([[1.0, -1.0], [-1.0, 1.0]])
        np.testing.assert_allclose(ke, expected_ke)

    def test_element_mass_matrix(self):
        me = self.e1.me
        expected_me = np.array([[2/6, 1/6], [1/6, 2/6]])
        np.testing.assert_allclose(me, expected_me)

    def test_transformation_matrix(self):
        T = self.e1.transformation_matrix
        np.testing.assert_allclose(T @ T.T, np.eye(2))  # Check orthogonality


if __name__ == '__main__':
    unittest.main()
