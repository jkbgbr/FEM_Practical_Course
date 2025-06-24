import numpy as np

from source.beam.beam import BeamElement
from source.node import Node


# Example usage
n1 = Node(0, 0)
n2 = Node(0.5, 0)
beam = BeamElement(n1, n2, A=0.1 * 0.06, I=0.06**3 * 0.1 / 12, E=69e9)
# Calculate the stiffness matrix
ke = beam.ke

# add load
F = beam.load_vector(F2=-1000)  # Apply a force in the y-direction at node 2

# eliminating the first node (fixed) and the corresponding forces
F_eliminated = F[2:]  # Only keep forces at node 2
ke_eliminated = ke[2:, 2:]  # Only keep the stiffness matrix for node 2

# note: if instead of elimination the supported nodes are penalized, the stiffness matrix is larger but
# the reactions are easier to calculate later.

# Solve for displacements at node 2
displacements = np.linalg.solve(ke_eliminated, F_eliminated)
print("Displacements at node 2:", displacements)

# Calculate the reaction forces at node 1 (fixed)
# first the full displacements vector is created
u = np.zeros(4)  # Initialize displacements vector for both nodes
u[2:] = displacements  # set the displacements at node 2

# Calculate the reaction forces
# all nodes are considered, nodes without supports will have zero values
R = ke @ u - F  # Reaction forces
print("Reaction forces:", R)

# Deflections at a position along the x axis
xs = np.linspace(-beam.a, beam.a, 15)  # Local coordinates along the beam element
for x in xs:
    y = beam.base_functions(x) @ u  # Calculate deflections using the B matrix

beam.plot_deflections(xs, u)