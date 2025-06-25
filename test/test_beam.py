import pprint
import unittest

import numpy as np

from source.node import Node
from source.beam.beam import BeamElement, BeamModel
from source.utils import IDMixin


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

class TesBeamModel(unittest.TestCase):

    def setUp(self):
        IDMixin.reset()  # Reset ID counters for consistent testing
        A = 0.1  # Cross-sectional area
        I = 0.2  # Second moment of inertia
        E = 7e10  # Young's modulus
        ro = 1.0  # Density

        # number of elements for the A model; B has one element more
        NE = 100
        L = 10

        mesh = np.linspace(0, L, NE + 1)  # mesh points along the beam
        # Create nodes based on the mesh
        nodes = tuple(Node(x, 0, None) for x in mesh)  # nodes in the X-Y plane, Z=0
        elements = tuple(
            (nodes[i].ID, nodes[i + 1].ID, A, I, E, ro) for i in range(NE)
        )

        self.model_A = BeamModel(
            nodes_=nodes,
            elements_=elements,
            supports_={0: (0, 1)},
        )

        IDMixin.reset()  # Reset ID counters for consistent testing
        NE = NE + 1
        mesh = np.linspace(0, L, NE + 1)  # mesh points along the beam
        # Create nodes based on the mesh
        nodes = tuple(Node(x, 0, None) for x in mesh)  # nodes in the X-Y plane, Z=0
        elements = tuple(
            (nodes[i].ID, nodes[i + 1].ID, A, I, E, ro) for i in range(NE)
        )

        self.model_B = BeamModel(
            nodes_=nodes,
            elements_=elements,
            supports_={0: (0, 1)},
        )

    def test_max_deflection(self):
        "Cantilever beams with different number of elements should have the same maximum deflection"

        self.load_A = np.zeros(self.model_A.ND * len(self.model_A.nodes))
        self.load_A[-2] = -1000  # Load applied at the last node in the y-direction

        self.load_B = np.zeros(self.model_B.ND * len(self.model_B.nodes))
        self.load_B[-2] = -1000  # Load applied at the last node in the y-direction

        # defleiction, model A
        _K, _F = self.model_A.apply_boundary_conditions(self.load_A)  # Apply boundary conditions
        _U_A = np.linalg.solve(_K, _F)
        R_A = self.model_A.reaction_forces(_U_A, _F)

        # defleiction, model B
        _K, _F = self.model_B.apply_boundary_conditions(self.load_B)  # Apply boundary conditions
        _U_B = np.linalg.solve(_K, _F)
        R_B = self.model_B.reaction_forces(_U_B, _F)

        self.assertAlmostEqual(_U_A[-2] / _U_B[-2], 1, delta=1e-8)
        np.testing.assert_allclose(R_A[:2] / R_B[:2], 1, atol=1e-8)


if __name__ == '__main__':
    unittest.main()
