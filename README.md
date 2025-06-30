# Finite Element Method Implementation

This project aims to implement worked examples from the book "The Finite Element Method: A Practical Course" by G.R. Liu and S.S. Quek. It serves as a practical exercise in understanding and applying the finite element method (FEM) to structural mechanics problems using python.

Note that the package is:
- by no means coplete. 
- it is largely bug-free, but not optimized for speed or memory usage.
- aimed at educational purposes, not production use.


## Project Structure

The project is organized into sections based on dimensionality and element type:

**1D:** 
-   **Trusses**: Implementation of plane and spatial truss, static analysis.
-   **Beams**: Implementation of the Euler-Bernoulli 2D beam element, static and modal analysis.
-   **Frames**: Implementation of the spatial Euler-Bernoulli frame element, static and modal analysis.
   
**2D:**
- **Plates/Shells**: Implementation of plate and shell element analysis. (Planned)

The modules are tested, though not with the aim to achieve 100% coverage.

## Current Status, 1D Elements

Elements are implemented as listed:
- **Trusses**: Displacements, member forces, support reactions.
- **Beams and frames**: Displacements, support reactions, modal analysis.

Check out the notebooks in the `notebooks/` directory for examples of how to use the classes.

To avoid code repetition and get python out of the way certain aspects are implemented in a generic way which also shows which steps of the finite element procedure are common to all elements:
- A Model class is used to hold the nodes, elements, and boundary conditions, solve the problems etc.
- A Node class is used to hold the node coordinates.
- Support definition is done by defining a list of nodes and their _local_ degrees of freedom (DOFs) that are constrained.
- This makes model definition unified across different element types.
- Node and element IDs are given away automatically. If multiple models are created within the same session, first ``IDMixin.reset()`` is to be called.
