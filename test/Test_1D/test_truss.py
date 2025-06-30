import unittest

import numpy as np

from source.node import Node
from source.OneD.truss.truss import TrussElement, TrussModel
from source.utils import IDMixin


class TestTruss(unittest.TestCase):

    def setUp(self):
        IDMixin.reset()  # Reset ID counters for consistent testing
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


class SingleElementTest(unittest.TestCase):

    """
    A single horizontal truss element, left end fixed in x and y, right end fixed in y and loaded in x
    """

    def setUp(self):
        IDMixin.reset()  # Reset ID counters for consistent testing

        A = 0.1  # Cross-sectional area
        E = 7e10  # Young's modulus
        ro = 1.0  # Density

        n1 = Node(0, 0,)
        n2 = Node(1, 0,)
        self.model = TrussModel(
            nodes_=(n1, n2),
            elements_=((n1.ID, n2.ID, A, E, ro),),
            supports_={0: (0, 1), 1: (1, )},
        )

        self.load = np.zeros(self.model.ND * len(self.model.nodes))  # No external forces
        self.load[self.model.ND] = -1000  # Apply a load of -1000 N at node 1 in the x-direction

    def test_single_element(self):
        self.assertEqual(len(self.model.nodes), 2)
        self.assertEqual(len(self.model.elements), 1)
        self.assertEqual(self.model.elements[0].length, 1.0)
        self.assertEqual(self.model.elements[0].A, 0.1)
        self.assertEqual(self.model.elements[0].E, 7e10)
        self.assertEqual(self.model.elements[0].ro, 1.0)

    def test_member_forces(self):
        _K, _F = self.model.apply_boundary_conditions(self.load)  # Apply boundary conditions

        _U = np.linalg.solve(_K, _F)
        member_forces = self.model.member_forces(_U)
        self.assertTrue(np.isclose(member_forces[0][0], -1000))


class MultiElementTest(unittest.TestCase):

    """
    A truss like a pyramide with a single vertical load at the top node.
    """

    def setUp(self):
        IDMixin.reset()  # Reset ID counters for consistent testing

        A = 0.1  # Cross-sectional area
        E = 7e10  # Young's modulus
        ro = 1.0  # Density

        n1 = Node(1, 1, 0)
        n2 = Node(-1, 1, 0)
        n3 = Node(-1, -1, 0)
        n4 = Node(1, -1, 0)
        n5 = Node(0, 0, 1)

        self.model = TrussModel(
            nodes_=(n1, n2, n3, n4, n5),
            elements_=(
                (n1.ID, n5.ID, A, E, ro),
                (n2.ID, n5.ID, A, E, ro),
                (n3.ID, n5.ID, A, E, ro),
                (n4.ID, n5.ID, A, E, ro),
                       ),
            supports_={k: list(range(3)) for k in range(4)}
        )

        self.load = np.zeros(self.model.ND * len(self.model.nodes))  # No external forces
        self.load[14] = -1000  # Apply a load of -1000 N at node 1 in the x-direction

    def test_member_forces(self):
        _K, _F = self.model.apply_boundary_conditions(self.load)  # Apply boundary conditions

        _U = np.linalg.solve(_K, _F)
        member_forces = self.model.member_forces(_U)

        # all member forces are the same
        self.assertTrue(len(set(x[0] for x in member_forces)) == 1)


if __name__ == '__main__':
    unittest.main()
