import unittest
import random

import numpy as np

from source.node import Node
from source.TwoD.PlaneQuad.plane_quad import PlaneQuadModel


class TestRM2DPlate(unittest.TestCase):

    def setUp(self):
        n1 = Node(-3, -4, 0)
        n2 = Node(1, -2, 0)
        n3 = Node(1.5, 2, 0)
        n4 = Node(-1, 3, 0)

        model = PlaneQuadModel(
            nodes_=(n1, n2, n3, n4),
            elements_=(
                (n1.ID, n2.ID, n3.ID, n4.ID, 1.2, 210, 0.3),
            ),
            supports_={
                n1.ID: (0, 1, 2,),
                n2.ID: (0, 1, 2,),
                n3.ID: (0, 1, 2,),
                n4.ID: (0, 1, 2,),
            }
        )

        self.element = model.elements[0]

    def test_unity(self):

        np.testing.assert_almost_equal(sum(self.element._N(1, 1)), 1.)
        np.testing.assert_almost_equal(sum(self.element._N(0, 0)), 1.)

        xi = random.randrange(-100, 100) / 100
        eta = random.randrange(-100, 100) / 100
        np.testing.assert_almost_equal(sum(self.element._N(xi, eta)), 1.)



if __name__ == '__main__':
    unittest.main()
