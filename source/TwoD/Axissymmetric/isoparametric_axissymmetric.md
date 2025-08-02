Ja, für dieses 3-Knoten-Dreieckselement gibt es eine sehr gebräuchliche und elegante isoparametrische Formulierung. Tatsächlich ist dies der Standardansatz in den meisten modernen FEM-Programmen, da er die Berechnungen verallgemeinert und vereinfacht.

**Konzept der isoparametrischen Formulierung**

Der Kerngedanke ist, alle Berechnungen in einem einfachen, standardisierten "Elternelement" durchzuführen, das in einem lokalen "natürlichen" Koordinatensystem (oft `ξ` und `η` oder `s` und `t` genannt) definiert ist.

1.  **Elternelement (Parent Element):** Wir definieren ein einfaches Referenzdreieck, z. B. mit den Knoten an `(0,0)`, `(1,0)` und `(0,1)` im `ξ-η`-System. Die Formfunktionen in diesem System sind extrem einfach:
    *   `N1 = 1 - ξ - η`
    *   `N2 = ξ`
    *   `N3 = η`

2.  **Isoparametrische Abbildung:** Der entscheidende Schritt ist, dass wir dieselben Formfunktionen `N` verwenden, um sowohl die globalen Koordinaten `(r, z)` als auch die Verschiebungen `(u, w)` abzubilden:
    *   `r(ξ, η) = N1(ξ, η)*r1 + N2(ξ, η)*r2 + N3(ξ, η)*r3`
    *   `z(ξ, η) = N1(ξ, η)*z1 + N2(ξ, η)*z2 + N3(ξ, η)*z3`
    *   `u(ξ, η) = N1(ξ, η)*u1 + N2(ξ, η)*u2 + N3(ξ, η)*u3`
    *   `w(ξ, η) = N1(ξ, η)*w1 + N2(ξ, η)*w2 + N3(ξ, η)*w3`

3.  **Jacobian-Matrix:** Da die `B`-Matrix Ableitungen nach den globalen Koordinaten `r` und `z` benötigt, wir aber nur einfache Ableitungen nach `ξ` und `η` haben, verwenden wir die Kettenregel. Die Umrechnung erfolgt über die **Jacobian-Matrix `J`**:
    `J = [[∂r/∂ξ, ∂z/∂ξ], [∂r/∂η, ∂z/∂η]]`

4.  **Integration:** Die Integration zur Berechnung der Steifigkeitsmatrix `K` wird ebenfalls im einfachen `ξ-η`-System durchgeführt, wobei das Volumenelement (oder Flächenelement) transformiert wird:
    `dr dz = det(J) dξ dη`

**Vorteile:**

*   **Einfachheit:** Die Formfunktionen und ihre Ableitungen im natürlichen System sind immer gleich, unabhängig von der Form oder Größe des realen Elements.
*   **Allgemeinheit:** Der Ansatz funktioniert für gerade und gekrümmte Elemente (obwohl für dieses lineare Dreieck die Seiten gerade bleiben).
*   **Standardisierung:** Der gesamte Prozess ist standardisiert und leicht zu programmieren.

Ihr aktueller Ansatz verwendet eine direkte Formulierung in globalen Koordinaten, was für einfache Elemente wie dieses funktioniert. Die isoparametrische Formulierung ist jedoch leistungsfähiger und der übliche Weg für die allgemeine Finite-Elemente-Analyse.



Ja, das ist im Grunde genau der richtige Weg. Die Eleganz der isoparametrischen Formulierung liegt darin, dass sie ein komplexeres Problem auf eine Reihe von standardisierten Schritten in einem einfachen Koordinatensystem zurückführt. Es ist tatsächlich so elegant, dass es sich "zu einfach" anfühlt.

Hier sind die Schritte, die Sie unternehmen werden, und die bestätigen, dass Ihr Gedankengang korrekt ist:

1.  **Definieren Sie das Elternelement:** Sie arbeiten nicht mehr mit `r` und `z`, sondern mit natürlichen Koordinaten `ξ` und `η`. Das Elternelement ist ein einfaches rechtwinkliges Dreieck mit den Knoten bei `(0,0)`, `(1,0)` und `(0,1)`.

2.  **Verwenden Sie die einfachen Formfunktionen:** Die Formfunktionen in diesem System sind, wie Sie vermutet haben, extrem einfach:
    *   `N1 = 1 - ξ - η`
    *   `N2 = ξ`
    *   `N3 = η`

3.  **Berechnen Sie die Jacobian-Matrix `J`:** Dies ist der entscheidende Schritt, der die realen Koordinaten `(r, z)` mit den natürlichen Koordinaten `(ξ, η)` verbindet. Die Ableitungen für `J` sind sehr einfach zu berechnen.

4.  **Stellen Sie die `B`-Matrix auf:** Sie verwenden die Kettenregel, um die Ableitungen nach `r` und `z` zu erhalten (`[∂N/∂r, ∂N/∂z] = inv(J) * [∂N/∂ξ, ∂N/∂η]`). Die `B`-Matrix wird dann mit diesen Ableitungen aufgebaut. Der knifflige `1/r`-Term bleibt bestehen, aber `r` wird jetzt selbst durch die Formfunktionen ausgedrückt: `r = N1*r1 + N2*r2 + N3*r3`.

5.  **Integrieren Sie über das Elternelement:** Die Berechnung der Steifigkeitsmatrix `K` wird zu einem Integral über `ξ` und `η` von 0 bis 1, wobei das Flächenelement `dr dz` durch `det(J) dξ dη` ersetzt wird.

Der Prozess ist standardisiert und sehr leistungsfähig. Die "Schwierigkeit" liegt in der korrekten Handhabung der Matrixalgebra, aber die zugrunde liegenden Konzepte sind genau so geradlinig, wie Sie es sich vorgestellt haben.


Of course. Here is the derivation for the `B_i` matrix block for a single node `i` in an isoparametric axisymmetric formulation.

The strain-displacement relationship in axisymmetric coordinates is given by:

$$
{\epsilon} =
\begin{Bmatrix}
\epsilon_r \\
\epsilon_z \\
\gamma_{rz} \\
\epsilon_\theta
\end{Bmatrix}
=
\begin{Bmatrix}
\frac{\partial u}{\partial r} \\
\frac{\partial w}{\partial z} \\
\frac{\partial u}{\partial z} + \frac{\partial w}{\partial r} \\
\frac{u}{r}
\end{Bmatrix}
$$

In the isoparametric formulation, the displacements `u` and `w` are interpolated from the nodal displacements `u_i` and `w_i` using the shape functions `N_i(\xi, \eta)`:

$$
u(\xi, \eta) = \sum_{i=1}^{3} N_i(\xi, \eta) u_i \quad \quad w(\xi, \eta) = \sum_{i=1}^{3} N_i(\xi, \eta) w_i
$$

The strain vector `ε` can be related to the nodal displacement vector `d` through the `B` matrix: `ε = B d`. The `B` matrix is composed of blocks `B_i` for each node: `B = [B_1, B_2, B_3]`.

The block `B_i` for node `i` connects the strains to the displacements `u_i` and `w_i`. By substituting the interpolation for `u` and `w` into the strain definitions, we get the structure of `B_i`:

$$
\mathbf{B}_i =
\begin{bmatrix}
\frac{\partial N_i}{\partial r} & 0 \\
0 & \frac{\partial N_i}{\partial z} \\
\frac{\partial N_i}{\partial z} & \frac{\partial N_i}{\partial r} \\
\frac{N_i}{r} & 0
\end{bmatrix}
$$

The core of the isoparametric method is to find the global derivatives (`∂/∂r`, `∂/∂z`) from the natural derivatives (`∂/∂ξ`, `∂/∂η`) using the chain rule and the inverse of the Jacobian matrix `J`:

$$
\begin{Bmatrix}
\frac{\partial N_i}{\partial r} \\
\frac{\partial N_i}{\partial z}
\end{Bmatrix}
=
\mathbf{J}^{-1}
\begin{Bmatrix}
\frac{\partial N_i}{\partial \xi} \\
\frac{\partial N_i}{\partial \eta}
\end{Bmatrix}
$$

The Jacobian matrix J relates the derivatives in the global coordinate system (r, z) to the derivatives in the natural coordinate system (ξ, η).

It is defined as:

$$\mathbf{J} = \begin{bmatrix} \frac{\partial r}{\partial \xi} & \frac{\partial z}{\partial \xi} \\ \frac{\partial r}{\partial \eta} & \frac{\partial z}{\partial \eta} \end{bmatrix}$$

Using the isoparametric mapping $$ r = \sum N_i r_i $$ and $$ z = \sum N_i z_i$$ for a 3-node linear triangle, we can compute the specific terms. For example, $$\frac{\partial r}{\partial \xi} = \sum \frac{\partial N_i}{\partial \xi} r_i$$.

Since the derivatives of the linear shape functions $$(\frac{\partial N_i}{\partial \xi}, \frac{\partial N_i}{\partial \eta})$$ are constants, the resulting Jacobian matrix is also constant for the element. Its components are:

$$\mathbf{J} = \begin{bmatrix} r_2 - r_1 & z_2 - z_1 \\ r_3 - r_1 & z_3 - z_1 \end{bmatrix}$$

where $(r_1, z_1)$, $(r_2, z_2)$, and $(r_3, z_3)$ are the global coordinates of the three element nodes.

The derivatives of the shape functions with respect to the natural coordinates (`∂N_i/∂ξ`, `∂N_i/∂η`) are simple constants. The Jacobian `J` is also constant for a linear triangle.

The final key point is that the radius `r` in the fourth row (`N_i/r`) is not a constant. It must also be interpolated from the nodal coordinates at the specific Gauss point being evaluated:

$$
r = \sum_{j=1}^{3} N_j(\xi, \eta) r_j
$$

This `r` in the denominator is why the `B` matrix is not constant across the element and why numerical integration (Gaussian quadrature) is necessary.



You are correct to be cautious, as there are two common conventions for defining the Jacobian matrix, one being the transpose of the other. Both are valid, as long as they are used consistently.

Let's clarify the definition I used, which is very common in finite element literature.

The goal is to relate the derivatives in the global system (r, z) to the derivatives in the natural system (ξ, η). The chain rule gives us:

$$\begin{Bmatrix} \frac{\partial f}{\partial \xi} \\ \frac{\partial f}{\partial \eta} \end{Bmatrix} = \begin{bmatrix} \frac{\partial r}{\partial \xi} & \frac{\partial z}{\partial \xi} \\ \frac{\partial r}{\partial \eta} & \frac{\partial z}{\partial \eta} \end{bmatrix} \begin{Bmatrix} \frac{\partial f}{\partial r} \\ \frac{\partial f}{\partial z} \end{Bmatrix}$$

This can be written compactly as:

$$\nabla_{\xi} f = \mathbf{J} \nabla_{r} f$$

Here, the Jacobian matrix J is defined as:

$$\mathbf{J} = \begin{bmatrix} \frac{\partial r}{\partial \xi} & \frac{\partial z}{\partial \xi} \\ \frac{\partial r}{\partial \eta} & \frac{\partial z}{\partial \eta} \end{bmatrix}$$

This is the definition I provided previously. To compute the B matrix, we need the derivatives with respect to the global coordinates (r, z). Therefore, we must invert the relationship:

$$\nabla_{r} f = \mathbf{J}^{-1} \nabla_{\xi} f$$

The other convention defines the Jacobian as the transpose of the above:

$$\mathbf{J}_{\text{alt}} = \begin{bmatrix} \frac{\partial r}{\partial \xi} & \frac{\partial r}{\partial \eta} \\ \frac{\partial z}{\partial \xi} & \frac{\partial z}{\partial \eta} \end{bmatrix}$$

If this alternative definition is used, the chain rule relationship changes accordingly.

The definition I have used is consistent with many standard FEM textbooks (e.g., Zienkiewicz & Taylor, Cook et al.). The key is that the matrix used to transform the derivatives must be inverted to get the global derivatives from the natural ones. My previous explanations are consistent with this formulation.


**OK. I have some textbooks that have a adifferent order of the elements in the B matrix as they define the differential operator differently. Should not be a problem right?**

You are absolutely right. It should not be a problem, and it's a very important point. The order of the rows in the `B` matrix depends directly on the definition of the strain vector `ε`.

The key is **consistency**.

In my previous explanations, I used the following definition for the strain vector, which is common in structural mechanics:

$$
{\epsilon} =
\begin{Bmatrix}
\epsilon_r \\
\epsilon_z \\
\gamma_{rz} \\
\epsilon_\theta
\end{Bmatrix}
$$

This definition leads to the `B_i` matrix block I showed you:

$$
\mathbf{B}_i =
\begin{bmatrix}
\frac{\partial N_i}{\partial r} & 0 \\
0 & \frac{\partial N_i}{\partial z} \\
\frac{\partial N_i}{\partial z} & \frac{\partial N_i}{\partial r} \\
\frac{N_i}{r} & 0
\end{bmatrix}
$$

However, some textbooks, particularly those coming from a continuum mechanics perspective, might define the strain vector differently, for example:

$$
{\epsilon}_{\text{alt}} =
\begin{Bmatrix}
\epsilon_r \\
\epsilon_\theta \\
\epsilon_z \\
\gamma_{rz}
\end{Bmatrix}
$$

If you use this alternative definition, the rows of your `B` matrix must be reordered to match:

$$
\mathbf{B}_{i, \text{alt}} =
\begin{bmatrix}
\frac{\partial N_i}{\partial r} & 0 \\
\frac{N_i}{r} & 0 \\
0 & \frac{\partial N_i}{\partial z} \\
\frac{\partial N_i}{\partial z} & \frac{\partial N_i}{\partial r}
\end{bmatrix}
$$

This is not a problem as long as your constitutive matrix `D` is also ordered to be consistent with your chosen strain vector definition. The calculation of the stiffness matrix `K = ∫ B^T D B * 2πr dV` will yield the same correct result, because the terms are just being multiplied in a different, but consistent, order.

Your code seems to use a different `D` matrix than the standard one for plane stress, but as long as your `B` and `D` matrices are consistent with each other and your underlying theory, the result is valid.


**I have the feeling my B is not consitent with my D.**

That is a very common and critical issue to check. If your `B` and `D` matrices are inconsistent, the resulting stiffness matrix will be incorrect.

Here is how you can verify the consistency between your `B` and `D` matrices. The key is that both must be based on the **exact same definition of the strain vector `ε`**.

**Step 1: Write down your strain vector `ε`**

First, explicitly define the order of strains you are using. For example, let's assume you chose this common order:

$$
{\epsilon} =
\begin{Bmatrix}
\epsilon_r \\  \epsilon_z \\ \gamma_{rz} \\ \epsilon_\theta
\end{Bmatrix}
=
\begin{Bmatrix}
\text{1st component} \\ \text{2nd component} \\ \text{3rd component} \\ \text{4th component}
\end{Bmatrix}
$$

**Step 2: Check your `B` Matrix**

The rows of your `B` matrix must be constructed to produce the components of your chosen `ε` vector in that specific order. For the example above, the rows of the `B_i` block must correspond to:

$$
\mathbf{B}_i =
\begin{bmatrix}
\frac{\partial N_i}{\partial r} & 0 \\   & \leftarrow \text{Row 1 computes } \epsilon_r \\
0 & \frac{\partial N_i}{\partial z} \\   & \leftarrow \text{Row 2 computes } \epsilon_z \\
\frac{\partial N_i}{\partial z} & \frac{\partial N_i}{\partial r} \\ & \leftarrow \text{Row 3 computes } \gamma_{rz} \\
\frac{N_i}{r} & 0 \\ & \leftarrow \text{Row 4 computes } \epsilon_\theta
\end{bmatrix}
$$

If your `B` matrix has the rows in a different order, your definition of `ε` must also have its components in that different order.

**Step 3: Check your `D` (Constitutive) Matrix**

The constitutive relationship is `σ = D ε`. The `D` matrix maps the strain vector `ε` to the stress vector `σ`. By convention, the stress vector `σ` is ordered identically to the strain vector `ε`.

$$
\begin{Bmatrix}
\sigma_r \\ \sigma_z \\ \tau_{rz} \\ \sigma_\theta
\end{Bmatrix}
=
\begin{bmatrix}
D_{11} & D_{12} & D_{13} & D_{14} \\
D_{21} & D_{22} & D_{23} & D_{24} \\
D_{31} & D_{32} & D_{33} & D_{34} \\
D_{41} & D_{42} & D_{43} & D_{44}
\end{bmatrix}
\begin{Bmatrix}
\epsilon_r \\ \epsilon_z \\ \gamma_{rz} \\ \epsilon_\theta
\end{Bmatrix}
$$

To verify your `D` matrix, check a single row. For example, the first row of the equation `σ = D ε` calculates `σ_r`:
`σ_r = D_11 * ε_r + D_12 * ε_z + D_13 * γ_rz + D_14 * ε_θ`

The coefficients `D_11`, `D_12`, etc., in your code must match the material law for `σ_r` based on the strain components in the order you defined in Step 1. If your `D` matrix was built for a different strain order (e.g., `ε = {ε_r, ε_θ, ε_z, γ_rz}`), then the columns would be swapped, and the `D` matrix would be incorrect for the `B` matrix shown above.

By performing these three steps, you can ensure that the `ε` you use to build `B` is the same `ε` that your `D` matrix expects.




# Sie haben absolut recht, und ich entschuldige mich. 
Meine vorherige Analyse war falsch. Sie haben den Kern des Problems korrekt identifiziert, indem Sie die Rolle der Jacobi-Determinante in Frage gestellt haben.

Lassen Sie uns dies von Grund auf neu aufbauen.

1.  **Die Integrationsformel:** Die Steifigkeitsmatrix wird durch ein Integral über die *Fläche des Elternelements* berechnet, nicht über die physische Fläche. Die Transformation vom physischen zum natürlichen Koordinatensystem führt die Jacobi-Determinante ein:
    $$ K = \int_{\text{Eltern}} (B^T D B \cdot 2 \pi r) \cdot |J| \, d\xi d\eta $$
    Hier ist `B` die isoparametrische B-Matrix, die *keinen* `1/two_A`-Term enthält.

2.  **Die Jacobi-Determinante `|J|`:** Für ein lineares Dreieckselement ist die Jacobi-Determinante `|J|` konstant und entspricht der **doppelten Fläche des physischen Elements (`two_A`)**. Das ist ein Standardergebnis in der FEM. Ihre Annahme ist also korrekt.

3.  **Numerische Integration (Gauß-Quadratur):** Wenn wir das Integral numerisch lösen, wird es zu einer Summe. Die Standard-Gauß-Quadraturformel für ein Dreieck lautet:
    $$ \int_{\text{Eltern}} f(\xi, \eta) \, d\xi d\eta = (\text{Fläche des Elternelements}) \cdot \sum_{i} w_i f(\xi_i, \eta_i) $$
    Das Standard-Elternelement (Knoten bei (0,0), (1,0), (0,1)) hat eine Fläche von **0.5**.

4.  **Zusammensetzen der Formel:** Wir setzen nun alles in die Formel für `K` ein:
    $$ K = (\text{Fläche des Elternelements}) \cdot \sum_{gp} (B^T D B \cdot 2 \pi r)_{gp} \cdot |J| \cdot w_{gp} $$
    $$ K = (0.5) \cdot \sum_{gp} (B^T D B \cdot 2 \pi r)_{gp} \cdot (\text{two\_A}) \cdot w_{gp} $$

**Das ist der entscheidende Punkt.** Die Formel enthält sowohl den Faktor `0.5` (aus der Quadraturregel) als auch den Faktor `two_A` (die Jacobi-Determinante). Da `two_A` die doppelte Fläche ist, heben sich die Faktoren `0.5` und `two_A` gegenseitig auf, und es bleibt die einfache Fläche `A` übrig.
$$ K = A \cdot \sum_{gp} (B^T D B \cdot 2 \pi r)_{gp} \cdot w_{gp} $$

**Analyse Ihres Codes:**

Ihre vorherige, funktionierende Implementierung lautete:
```python
K += B_evaluated.T * D * B_evaluated * 2 * sp.pi * r_physical_at_gp * det_J * w
```
Hier ist `det_J` gleich `two_A`. Ihr Code berechnet also:
$$ K = \sum (B^T D B \cdot 2 \pi r)_{gp} \cdot (\text{two\_A}) \cdot w_{gp} $$
Wenn man dies mit der korrekten Formel vergleicht, fehlt in Ihrem Code der Faktor **0.5** von der Fläche des Elternelements. Das erklärt exakt, warum Ihre Ergebnisse **doppelt so groß** sind wie erwartet.

**Lösung:**

Sie müssen den Faktor `0.5` in Ihre Berechnung einbeziehen.

```python
def K_matrix_1(ng=1):
    """ Gauss integration, 1 or 3 integration points. This is method 1 from the book."""
    B_sym = B_symbolic()
    D = D_matrix()
    B_element = B_sym.subs(physical_coords_map)

    N_map = sp.Matrix([1 - R - Z, R, Z])
    r_map = N_map.dot(sp.Matrix([r1, r2, r3])).subs(physical_coords_map)
    z_map = N_map.dot(sp.Matrix([z1, z2, z3])).subs(physical_coords_map)

    # Jacobi-Determinante ist die doppelte physische Fläche
    det_J = two_A.subs(physical_coords_map)

    K = sp.zeros(ND * NNODE, ND * NNODE)

    # Die Fläche des Elternelements ist 0.5
    parent_area = 0.5

    for p, w in zip(gi_data[ng]['point'], gi_data[ng]['weight']):
        R_gp, Z_gp = p[0], p[1]
        r_physical_at_gp = r_map.subs({R: R_gp, Z: Z_gp})
        z_physical_at_gp = z_map.subs({R: R_gp, Z: Z_gp})
        B_evaluated = B_element.subs({'R': r_physical_at_gp, 'Z': z_physical_at_gp})

        # Korrekte Formel: A_parent * (...) * |J| * w
        K += parent_area * (B_evaluated.T * D * B_evaluated * 2 * sp.pi * r_physical_at_gp) * det_J * w

    return K
```