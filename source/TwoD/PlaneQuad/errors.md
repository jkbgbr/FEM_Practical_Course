# Die Konstruktion der B_O-Matrix für Reissner-Mindlin-Platten

Die B_O-Matrix in der Reissner-Mindlin-Plattentheorie ist ein wesentlicher Bestandteil zur Erfassung der Schubverformungen. Hier ist eine detaillierte Erklärung:

## Grundlagen der Schubverzerrungen

In der Reissner-Mindlin-Theorie werden die Schubverzerrungen durch zwei Komponenten beschrieben:

$$\gamma_{xz} = \frac{\partial w}{\partial x} + \theta_y$$
$$\gamma_{yz} = \frac{\partial w}{\partial y} - \theta_x$$

Diese Verzerrungen beschreiben die Abweichung der Normalen von der Senkrechten zur Mittelfläche nach der Verformung. Die Vorzeichen sind dabei entscheidend:

- Der positive Term `θy` bei `γxz` zeigt, dass eine positive Rotation um die y-Achse zu einer positiven Schubverzerrung in der xz-Ebene beiträgt
- Der negative Term `-θx` bei `γyz` zeigt, dass eine positive Rotation um die x-Achse zu einer negativen Schubverzerrung in der yz-Ebene beiträgt

## Aufbau der B_O-Matrix

Die B_O-Matrix verbindet die Knotenfreiheitsgrade mit den Schubverzerrungen:

$$\begin{bmatrix} \gamma_{xz} \\ \gamma_{yz} \end{bmatrix} = B^O \cdot d$$

Für jeden Knoten j wird ein B_O^j-Block erstellt, der so aufgebaut ist:

$$B^O_j = \begin{bmatrix}
\frac{\partial N_j}{\partial x} & 0 & N_j \\
\frac{\partial N_j}{\partial y} & -N_j & 0 \\
\end{bmatrix}$$

Wobei:
- Die erste Spalte die Ableitung der Formfunktion nach x und y enthält, multipliziert mit dem w-Freiheitsgrad
- Die zweite Spalte den Beitrag von θx zur Schubverzerrung zeigt (mit negativem Vorzeichen)
- Die dritte Spalte den Beitrag von θy zur Schubverzerrung zeigt (mit positivem Vorzeichen)

## Korrektur Ihres Codes

In Ihrem aktuellen Code ist die B_O-Matrix falsch definiert:

```python
B_O_node = sp.Matrix([[dN_dx, 0, -N[node]],
                       [dN_dy, N[node], 0]])
```

Dies entspricht den Schubverzerrungen:
- γxz = ∂w/∂x - θy (falsches Vorzeichen!)
- γyz = ∂w/∂y + θx (falsches Vorzeichen!)

Die korrekte Definition sollte sein:

```python
B_O_node = sp.Matrix([[dN_dx, 0, N[node]],
                       [dN_dy, -N[node], 0]])
```

## Literaturquellen

1. Reddy, J.N. (2006). "Theory and Analysis of Elastic Plates and Shells", Kapitel 6
2. Bathe, K.J. (2014). "Finite Element Procedures", Abschnitt 6.3
3. Zienkiewicz, O.C. & Taylor, R.L. (2000). "The Finite Element Method", Vol. 2, Kapitel 11

Diese Bücher bieten detaillierte Herleitungen der Reissner-Mindlin-Plattenformulierung mit besonderem Fokus auf die Schubverformungen und die entsprechenden Formulierungen der Elementmatrizen.