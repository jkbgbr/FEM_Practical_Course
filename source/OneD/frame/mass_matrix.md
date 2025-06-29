# Consistent mass matrix for the 3D frame

You are right, presenting a $12 \times 12$ matrix with all its individual terms in a clear and readable format can be challenging. Let's try this again, focusing on clear presentation of the structure and the non-zero terms for the **consistent mass matrix** of a 3D Euler-Bernoulli beam element.

The consistent mass matrix, $[M_C]$, for a 3D beam element uses the same shape functions as the stiffness matrix to capture the continuous mass distribution and coupling effects. For a two-node element with 6 degrees of freedom per node, this results in a $12 \times 12$ symmetric matrix.

Let's define the local degrees of freedom at each node as:
Node 1: $(u_1, v_1, w_1, \theta_{x1}, \theta_{y1}, \theta_{z1})$
Node 2: $(u_2, v_2, w_2, \theta_{x2}, \theta_{y2}, \theta_{z2})$

Where:
* $u, v, w$: Translational displacements along the local x, y, z axes.
* $\theta_x, \theta_y, \theta_z$: Rotational displacements about the local x, y, z axes.

The parameters are:
* $\rho$: Mass density of the beam material
* $A$: Cross-sectional area
* $L$: Length of the beam element
* $I_y, I_z$: Area moments of inertia about the local y and z axes (for bending).
* $J_x$: Mass polar moment of inertia of the cross-section about the local x-axis (for torsion). Note that this is a mass moment of inertia, $\int_A r^2 \rho dA$.

The consistent mass matrix $[M_C]$ can be expressed as a sum of contributions from axial, bending, and torsional deformations, as these are uncoupled in the local coordinate system for an Euler-Bernoulli beam:

$[M_C] = [M_{axial}] + [M_{bending\_y}] + [M_{bending\_z}] + [M_{torsion}]$

Let's define the non-zero terms for each part and then show how they fit into the overall $12 \times 12$ matrix.

---

### 1. Axial Mass Contribution ($[M_{axial}]$)

This accounts for translation along the beam's longitudinal (x) axis.
The non-zero terms are:
* $M_{1,1} = M_{7,7} = \frac{\rho A L}{3}$
* $M_{1,7} = M_{7,1} = \frac{\rho A L}{6}$

This means:
$$
[M_{axial}] =
\begin{bmatrix}
\frac{\rho A L}{3} & 0 & 0 & 0 & 0 & 0 & \frac{\rho A L}{6} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
\frac{\rho A L}{6} & 0 & 0 & 0 & 0 & 0 & \frac{\rho A L}{3} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0
\end{bmatrix}
$$

---

### 2. Torsional Mass Contribution ($[M_{torsion}]$)

This accounts for rotation about the beam's longitudinal (x) axis.
The non-zero terms are:
* $M_{4,4} = M_{10,10} = \frac{\rho J_x L}{3}$
* $M_{4,10} = M_{10,4} = \frac{\rho J_x L}{6}$

This means:
$$
[M_{torsion}] =
\begin{bmatrix}
0 & \cdots & 0 \\
\vdots & \frac{\rho J_x L}{3} \text{ (at 4,4)} & \vdots \\
0 & \cdots & 0 \\
\vdots & \frac{\rho J_x L}{6} \text{ (at 4,10)} & \vdots \\
0 & \cdots & \frac{\rho J_x L}{3} \text{ (at 10,10)} \\
\end{bmatrix} \quad \text{(all other entries are zero)}
$$

---

### 3. Bending Mass Contribution (x-y plane: $v, \theta_z$) ($[M_{bending\_z}]$)

This accounts for transverse displacement $v$ (in y-direction) and rotation $\theta_z$ (about z-axis).
The $4 \times 4$ sub-matrix for degrees of freedom $(v_1, \theta_{z1}, v_2, \theta_{z2})$ is:
$$
[M_{v, \theta_z}] = \frac{\rho A L}{420}
\begin{bmatrix}
156 & 22L & 54 & -13L \\
22L & 4L^2 & 13L & -3L^2 \\
54 & 13L & 156 & -22L \\
-13L & -3L^2 & -22L & 4L^2
\end{bmatrix}
$$
These terms populate the rows/columns corresponding to $v_1 (2), \theta_{z1} (6), v_2 (8), \theta_{z2} (12)$ in the full $12 \times 12$ matrix. For example:
* $M_{2,2} = M_{8,8} = \frac{156 \rho A L}{420}$
* $M_{2,6} = M_{6,2} = \frac{22 \rho A L^2}{420}$
* $M_{2,8} = M_{8,2} = \frac{54 \rho A L}{420}$
* $M_{2,12} = M_{12,2} = -\frac{13 \rho A L^2}{420}$
* $M_{6,6} = M_{12,12} = \frac{4 \rho A L^3}{420}$
* $M_{6,8} = M_{8,6} = \frac{13 \rho A L^2}{420}$
* $M_{6,12} = M_{12,6} = -\frac{3 \rho A L^3}{420}$

**Note on Rotary Inertia:** If rotary inertia about the z-axis (due to $I_z$) is included (which is common in Timoshenko or advanced Euler-Bernoulli formulations), additional terms would be added to this sub-matrix. For basic Euler-Bernoulli, these are often neglected. If included, they would look like:
$$
+ \frac{\rho I_z}{L}
\begin{bmatrix}
0 & 0 & 0 & 0 \\
0 & 1 & 0 & -1 \\
0 & 0 & 0 & 0 \\
0 & -1 & 0 & 1
\end{bmatrix}
$$
These terms would add to the $\theta_z-\theta_z$ coefficients.

---

### 4. Bending Mass Contribution (x-z plane: $w, \theta_y$) ($[M_{bending\_y}]$)

This accounts for transverse displacement $w$ (in z-direction) and rotation $\theta_y$ (about y-axis).
The $4 \times 4$ sub-matrix for degrees of freedom $(w_1, \theta_{y1}, w_2, \theta_{y2})$ is:
$$
[M_{w, \theta_y}] = \frac{\rho A L}{420}
\begin{bmatrix}
156 & -22L & 54 & 13L \\
-22L & 4L^2 & -13L & -3L^2 \\
54 & -13L & 156 & 22L \\
13L & -3L^2 & 22L & 4L^2
\end{bmatrix}
$$
These terms populate the rows/columns corresponding to $w_1 (3), \theta_{y1} (5), w_2 (9), \theta_{y2} (11)$ in the full $12 \times 12$ matrix. Notice the sign changes for some off-diagonal terms compared to bending in the x-y plane, due to the coordinate system conventions. For example:
* $M_{3,3} = M_{9,9} = \frac{156 \rho A L}{420}$
* $M_{3,5} = M_{5,3} = -\frac{22 \rho A L^2}{420}$
* $M_{3,9} = M_{9,3} = \frac{54 \rho A L}{420}$
* $M_{3,11} = M_{11,3} = \frac{13 \rho A L^2}{420}$
* $M_{5,5} = M_{11,11} = \frac{4 \rho A L^3}{420}$
* $M_{5,9} = M_{9,5} = -\frac{13 \rho A L^2}{420}$
* $M_{5,11} = M_{11,5} = -\frac{3 \rho A L^3}{420}$

**Note on Rotary Inertia:** Similar to $I_z$, if rotary inertia about the y-axis (due to $I_y$) is included, additional terms would be added to this sub-matrix.

$$
\frac{\rho I_y}{L}
\begin{bmatrix}
0 & 0 & 0 & 0 \\
0 & 1 & 0 & -1 \\
0 & 0 & 0 & 0 \\
0 & -1 & 0 & 1
\end{bmatrix}
$$
These terms would add to the $\theta_y-\theta_y$ coefficients.

---

### Combining into the $12 \times 12$ Matrix

The final $12 \times 12$ consistent mass matrix is the sum of these contributions. You would place each non-zero term into its corresponding position.

For instance, the $(1,1)$ entry of $[M_C]$ would be $M_{1,1}$ from $[M_{axial}]$, as no other contributions affect this degree of freedom.
The $(2,2)$ entry of $[M_C]$ would be $M_{2,2}$ from $[M_{bending\_z}]$, as no other contributions affect this.
The $(4,4)$ entry of $[M_C]$ would be $M_{4,4}$ from $[M_{torsion}]$.

The full $12 \times 12$ matrix, representing the sum, would look like this (where blank entries are zero):

$$
[M_C] =
\begin{bmatrix}
\frac{\rho A L}{3} & 0 & 0 & 0 & 0 & 0 & \frac{\rho A L}{6} & 0 & 0 & 0 & 0 & 0 \\
0 & \frac{156 \rho A L}{420} & 0 & 0 & 0 & \frac{22 \rho A L^2}{420} & 0 & \frac{54 \rho A L}{420} & 0 & 0 & 0 & -\frac{13 \rho A L^2}{420} \\
0 & 0 & \frac{156 \rho A L}{420} & 0 & -\frac{22 \rho A L^2}{420} & 0 & 0 & 0 & \frac{54 \rho A L}{420} & 0 & \frac{13 \rho A L^2}{420} & 0 \\
0 & 0 & 0 & \frac{\rho J_x L}{3} & 0 & 0 & 0 & 0 & 0 & \frac{\rho J_x L}{6} & 0 & 0 \\
0 & 0 & -\frac{22 \rho A L^2}{420} & 0 & \frac{4 \rho A L^3}{420} & 0 & 0 & 0 & -\frac{13 \rho A L^2}{420} & 0 & -\frac{3 \rho A L^3}{420} & 0 \\
0 & \frac{22 \rho A L^2}{420} & 0 & 0 & 0 & \frac{4 \rho A L^3}{420} & 0 & \frac{13 \rho A L^2}{420} & 0 & 0 & 0 & -\frac{3 \rho A L^3}{420} \\
\frac{\rho A L}{6} & 0 & 0 & 0 & 0 & 0 & \frac{\rho A L}{3} & 0 & 0 & 0 & 0 & 0 \\
0 & \frac{54 \rho A L}{420} & 0 & 0 & 0 & \frac{13 \rho A L^2}{420} & 0 & \frac{156 \rho A L}{420} & 0 & 0 & 0 & -\frac{22 \rho A L^2}{420} \\
0 & 0 & \frac{54 \rho A L}{420} & 0 & -\frac{13 \rho A L^2}{420} & 0 & 0 & 0 & \frac{156 \rho A L}{420} & 0 & \frac{22 \rho A L^2}{420} & 0 \\
0 & 0 & 0 & \frac{\rho J_x L}{6} & 0 & 0 & 0 & 0 & 0 & \frac{\rho J_x L}{3} & 0 & 0 \\
0 & 0 & \frac{13 \rho A L^2}{420} & 0 & -\frac{3 \rho A L^3}{420} & 0 & 0 & 0 & \frac{22 \rho A L^2}{420} & 0 & \frac{4 \rho A L^3}{420} & 0 \\
0 & -\frac{13 \rho A L^2}{420} & 0 & 0 & 0 & -\frac{3 \rho A L^3}{420} & 0 & -\frac{22 \rho A L^2}{420} & 0 & 0 & 0 & \frac{4 \rho A L^3}{420}
\end{bmatrix}
$$

This matrix assumes that rotary inertia terms (terms proportional to $\rho I_y$ and $\rho I_z$) are neglected, as is common in the most basic Euler-Bernoulli formulation. If they were included, they would appear on the diagonal and off-diagonal terms related to rotations.