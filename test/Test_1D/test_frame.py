import unittest

import numpy as np

from source.OneD.node import Node
from source.OneD.frame.spatial_frame import SpatialFrameElement, SpatialFrameModel
from source.OneD.utils import IDMixin



class TestBeam(unittest.TestCase):

    def setUp(self):
        self.i = Node(0, 0, 0)
        self.j = Node(1, 1, 1)
        self.e1 = SpatialFrameElement(self.i, self.j, A=1, Iy=1, Iz=2, J=5, E=2, ro=1, nu=0.3)

    def test_ke(self):
        ke = self.e1.ke
        np.testing.assert_allclose(ke, ke.T)

    def test_length(self):
        self.assertEqual(self.e1.a, 3 ** 0.5 / 2)


class TestSpatialFrameModelStatics(unittest.TestCase):

    def setUp(self):
        """
        Sets up a single-element and a multi-element spatial frame model for testing.
        The single-element model consists of two nodes and one element, while the multi-element model
        consists of a number of nodes with multiple elements connecting them.

        Checked is the reaction and the tip displacement of both models for the same load case.

        :return:
        """
        n1 = Node(0, 0, 0)
        n2 = Node(2, 3, 4)
        self.model1 = SpatialFrameModel(
            nodes_=(n1, n2),
            elements_=(
                (n1.ID, n2.ID, 1, 1, 1, 1, 1, 1, 0.3),
            ),
            supports_={
                n1.ID: (0, 1, 2, 3, 4, 5),
            }
        )

        # a second model with N elements on the same geometry
        IDMixin.reset()  # Reset ID counters so both model's numbering starts at zero
        meshx = np.linspace(0, 2, 20)
        meshy = np.linspace(0, 3, 20)
        meshz = np.linspace(0, 4, 20)
        nodes = tuple(Node(x, y, z) for x, y, z in zip(meshx, meshy, meshz))

        self.model2 = SpatialFrameModel(
            nodes_=nodes,
            elements_=tuple((x.ID, y.ID, 1, 1, 1, 1, 1, 1, 0.3) for x, y in zip(nodes, nodes[1:])),
            supports_={nodes[0].ID: (0, 1, 2, 3, 4, 5),}
        )

    def test_reaction_and_displacement(self):
        for i in range(self.model1.ND):

            ndof = self.model1.ND * len(self.model1.nodes)
            _F = np.zeros(ndof)
            _F[ndof - 1 - i] = 1
            u1, r1 = self.model1.solve(F=_F)

            ndof2 = self.model2.ND * len(self.model2.nodes)
            _F = np.zeros(ndof2)
            _F[ndof2 - 1 - i] = 1
            u2, r2 = self.model2.solve(F=_F)

            np.testing.assert_allclose(u1[-6:], u2[-6:], atol=1e-8)
            np.testing.assert_allclose(r1[:6], r2[:6], atol=1e-8)


class TestSpatialFrameModelModal(unittest.TestCase):

    def setUp(self):
        """
        Sets up a single-element and a multi-element spatial frame model for testing.
        The single-element model consists of two nodes and one element, while the multi-element model
        consists of a number of nodes with multiple elements connecting them.

        Checked is the reaction and the tip displacement of both models for the same load case.

        :return:
        """
        n1 = Node(0, 0, 0)
        n2 = Node(20, 0, 0)
        self.model1 = SpatialFrameModel(
            nodes_=(n1, n2),
            elements_=(
                (n1.ID, n2.ID, 1, 1, 1, 1, 1, 1, 0.3),
            ),
            supports_={
                n1.ID: (0, 1, 2, 3, 4, 5),
            }
        )

        # a second model with N elements on the same geometry
        IDMixin.reset()  # Reset ID counters so both model's numbering starts at zero
        meshx = np.linspace(0, 20, 20)
        meshy = np.linspace(0, 30, 20)
        meshz = np.linspace(0, 40, 20)
        # nodes = tuple(Node(x, y, z) for x, y, z in zip(meshx, meshy, meshz))
        nodes = tuple(Node(x, 0, 0) for x, y, z in zip(meshx, meshy, meshz))

        self.model2 = SpatialFrameModel(
            nodes_=nodes,
            elements_=tuple((x.ID, y.ID, 1, 1, 1.1, 1, 1, 1, 0.3) for x, y in zip(nodes, nodes[1:])),
            supports_={nodes[0].ID: (0, 1, 2, 3, 4, 5), }
        )

        E = Iy = ro = A = 1
        L = 20

        f1 = 1.875 ** 2 * np.sqrt(E * Iy / (ro * A * L ** 4)) / (2 * np.pi)  # first natural frequency [Hz]
        print(f1)

    def test_modal(self):
        # freqs1, shapes1 = self.model1.solve_modal()
        # print(freqs1)
        freqs2, shapes2 = self.model2.solve_modal()
        print(freqs2)
        for i in range(10):
            self.model2.plot_frame(shapes2[:, i])



if __name__ == '__main__':
    unittest.main()
