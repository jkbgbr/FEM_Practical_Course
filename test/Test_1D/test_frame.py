import unittest

import numpy as np

from source.OneD.node import Node
from source.OneD.frame.spatial_frame import SpatialFrameElement, SpatialFrameModel



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


class TestSpatialFrameModel(unittest.TestCase):

    def setUp(self):
        n1 = Node(0, 0, 0)
        n2 = Node(1, 0, 0)
        self.model = SpatialFrameModel(
            nodes_=(n1, n2),
            elements_=(
                (n1.ID, n2.ID, 1, 1, 1, 1, 1, 1, 0.3),
            ),
            supports_={
                n1.ID: (0, 1, 2, 3, 4, 5),
            }
        )

    def test_reaction(self):
        for i in range(self.model.ND):
            print()
            print(i)
            _F = np.zeros(self.model.ND * len(self.model.nodes))
            _F[self.model.ND + i] = 1
            print(_F[6:])
            u, r = self.model.solve(F=_F)
            print(r.reshape(len(self.model.nodes), 6))
            # print(u)
            # print(r[self.model.ND + i])

            # self.assertAlmostEqual(r[self.model.ND + i], 1, places=5)




if __name__ == '__main__':
    unittest.main()
