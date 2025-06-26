"""
The 2D beam element from Chapter 5,
worked example 5.4

There is an error in the 2nd edition (Elsevier, 2014)
in (5.14) correctly: N3 = 1/4 * (2 + 3 * ksi - ksi**3)
in (5.20) correctly: N3" = -3/2 * ksi
"""

from dataclasses import dataclass
from source.OneD.beam.beam import BeamElement, BeamModel

import numpy as np



@dataclass
class TimoshenkoBeamElement(BeamElement):
    """
    A 2D Timoshenko beam element that accounts for shear deformation.
    It uses linear interpolation for displacement and rotation.
    DOFs per node are still [vertical displacement, rotation].
    """
    poisson_ratio: float = 0.3  # Poisson's ratio, needed for shear modulus G
    shear_correction_factor: float = 5 / 6  # Kappa, 5/6 is common for rectangular cross-sections

    @property
    def G(self) -> float:
        """Shear Modulus."""
        return self.E / (2 * (1 + self.poisson_ratio))

    @property
    def ke(self):
        """
        Local stiffness matrix (4x4) for the Timoshenko beam element.
        This formulation includes shear deformation.
        """
        E = self.E
        I = self.I
        L = self.length
        A = self.A
        G = self.G
        kappa = self.shear_correction_factor

        # Shear deformation parameter Phi
        phi = (12 * E * I) / (kappa * G * A * L ** 2)

        # Stiffness matrix coefficients
        c1 = E * I / (L ** 3 * (1 + phi))

        ke = np.zeros((4, 4))
        ke[0, :] = [12, 6 * L, -12, 6 * L]
        ke[1, :] = [6 * L, (4 + phi) * L ** 2, -6 * L, (2 - phi) * L ** 2]
        ke[2, :] = [-12, -6 * L, 12, -6 * L]
        ke[3, :] = [6 * L, (2 - phi) * L ** 2, -6 * L, (4 + phi) * L ** 2]

        ke *= c1
        return ke

    def _distributed_load(self, q: float) -> np.ndarray:
        """
        Calculates the consistent load vector for a uniformly distributed load 'q'
        for a Timoshenko beam element.
        """
        L = self.length
        E = self.E
        I = self.I
        A = self.A
        G = self.G
        kappa = self.shear_correction_factor

        # Shear deformation parameter Phi
        phi = (12 * E * I) / (kappa * G * A * L ** 2)

        f_e = np.array([
            q * L / 2,
            q * L ** 2 / 12 * (1 + phi),
            q * L / 2,
            -q * L ** 2 / 12 * (1 + phi)
        ])
        return f_e


class TimoschenkoBeamModel(BeamModel):
    """
    A model for a 2D Timoshenko beam, which can be used to analyze the beam's behavior under various loads.
    It uses TimoshenkoBeamElement for the elements.
    """
    def __post_init__(self):
        # Convert nodes and elements to dictionaries for easy access
        # This allows for quick lookups by node ID and element ID
        self.nodes = {node.ID: node for node in self.nodes_}  # Convert nodes to a dictionary for easy access
        elements_ = tuple(
            TimoshenkoBeamElement(i=self.nodes[x[0]], j=self.nodes[x[1]], A=x[2], I=x[3], E=x[4], ro=x[5]) for x in self.elements_)
        self.elements = {x.ID: x for x in elements_}  # Convert elements to a dictionary for easy access
        self.supports = self.supports_ if self.supports_ is not None else tuple()  # Supports, a tuple of (node_id, direction)

        # set the DOF indices for each element
        self.elements = self.set_element_dof_indices()