import numpy as np

from source.node import Node
from source.truss import TrussModel


A = 0.1  # Cross-sectional area
E = 7e10  # Young's modulus
ro = 1.0  # Density

n1 = Node(0, 0, 0)
n2 = Node(1, 0, 0)
n3 = Node(0, 1, 0)
model = TrussModel(
    nodes_=(n1, n2, n3),
    elements_=((n1.ID, n2.ID, A, E, ro),
               (n1.ID, n3.ID, A, E, ro),
               (n2.ID, n3.ID, A, E, ro),),
    supports_=((0, 'x'), (0, 'y'), (2, 'x'),
               (0, 'z'), (1, 'z'), (2, 'z')
               ),
)

_F = np.zeros(model.ND * len(model.nodes))  # Global force vector, initialized to zero
_F[model.ND + 1] = -1000  # Apply a force of -1000 N in the y-direction at node 2 (index 1)

np.set_printoptions(precision=3, suppress=True, linewidth=120)
print("Global stiffness matrix K before applying the BCs:\n", model.K)

_K, _F = model.apply_boundary_conditions(_F)  # Apply boundary conditions

# set the numpy printout options for better readability
print("Global stiffness matrix K after adding the BCs:\n", _K)
print('Global force vector F:\n', _F)

# Solve the system of equations K * u = F for the displacements u
_U = np.linalg.solve(_K, _F)
np.set_printoptions(precision=3, suppress=False, linewidth=120)
print()
print('Results:')
print("Global displacements:", _U)
# Calculate the member force using the local stiffness matrix
print('Member forces:', model.member_forces(_U))

# Calculate the reaction forces
print('Reaction forces:', model.reaction_forces(_U, _F))
