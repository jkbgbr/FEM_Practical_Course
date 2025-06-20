# Example calculation of the m_12_ element of the mass matrix

Um das Integral $$\int N_1 \cdot N_2 \, dx$$ entlang der Länge des Fachwerkelements zu berechnen, folgen wir diesen Schritten:

### 1. Definition der Formfunktionen
Die Formfunktionen $$N_1(x)$$ und $$N_2(x)$$ sind bereits definiert:
- $$N_1(x) = 1 - \frac{x}{L}$$
- $$N_2(x) = \frac{x}{L}$$

Hier ist $$L$$ die Länge des Fachwerkelements.

### 2. Produkt der Formfunktionen
Das Produkt $$N_1(x) \cdot N_2(x)$$ ergibt:
$$
N_1(x) \cdot N_2(x) = \left(1 - \frac{x}{L}\right) \cdot \frac{x}{L} = \frac{x}{L} - \frac{x^2}{L^2}
$$

### 3. Integral aufstellen
Das Integral lautet:
$$
\int_0^L \left(\frac{x}{L} - \frac{x^2}{L^2}\right) dx
$$

### 4. Integration durchführen
Wir integrieren die Terme einzeln:
$$
\int_0^L \frac{x}{L} dx = \frac{1}{L} \int_0^L x dx = \frac{1}{L} \cdot \left[\frac{x^2}{2}\right]_0^L = \frac{1}{L} \cdot \frac{L^2}{2} = \frac{L}{2}
$$

$$
\int_0^L \frac{x^2}{L^2} dx = \frac{1}{L^2} \int_0^L x^2 dx = \frac{1}{L^2} \cdot \left[\frac{x^3}{3}\right]_0^L = \frac{1}{L^2} \cdot \frac{L^3}{3} = \frac{L}{3}
$$

### 5. Ergebnis berechnen
Das Integral ergibt:
$$
\int_0^L \left(\frac{x}{L} - \frac{x^2}{L^2}\right) dx = \frac{L}{2} - \frac{L}{3} = \frac{3L}{6} - \frac{2L}{6} = \frac{L}{6}
$$

### Python-Code zur Berechnung
Hier ist der Python-Code, um das Integral numerisch oder symbolisch zu berechnen:

```python
import sympy as sp

# Variablen definieren
x = sp.Symbol('x')
L = sp.Symbol('L', positive=True)

# Formfunktionen
N1 = 1 - x / L
N2 = x / L

# Produkt der Formfunktionen
product = N1 * N2

# Integral berechnen
integral = sp.integrate(product, (x, 0, L))
print(f"Das Integral ist: {integral}")
```

Das Ergebnis des Codes ist:
```
Das Integral ist: L/6
```

# Next: the body loads are integrated.

Um das Integral $$\int_{V_e} (N_1, N_2)^T \cdot f_b \, dV$$ zu berechnen, folgen wir diesen Schritten:

### 1. Definition der Größen
- $$N_1(x)$$ und $$N_2(x)$$ sind die Formfunktionen, wie zuvor definiert.
- $$f_b$$ ist die Körperkraft pro Volumeneinheit (angenommen konstant entlang des Elements).
- Das Volumen $$V_e$$ des Fachwerkelements ist $$V_e = A \cdot l_e$$, wobei $$A$$ die Querschnittsfläche und $$l_e$$ die Länge des Elements ist.

### 2. Vereinfachung des Integrals
Da $$f_b$$ konstant ist, kann es aus dem Integral herausgezogen werden:
$$
\int_{V_e} (N_1, N_2)^T \cdot f_b \, dV = f_b \cdot \int_{V_e} (N_1, N_2)^T \, dV
$$

Das Integral über $$V_e$$ kann in ein Integral über die Länge $$l_e$$ umgewandelt werden:
$$
\int_{V_e} (N_1, N_2)^T \, dV = A \cdot \int_0^{l_e} (N_1, N_2)^T \, dx
$$

### 3. Berechnung des Integrals
Die Formfunktionen $$N_1(x)$$ und $$N_2(x)$$ sind:
$$
N_1(x) = 1 - \frac{x}{l_e}, \quad N_2(x) = \frac{x}{l_e}
$$

Das Integral wird für beide Komponenten berechnet:
$$
\int_0^{l_e} N_1(x) \, dx = \int_0^{l_e} \left(1 - \frac{x}{l_e}\right) dx = l_e \cdot \frac{1}{2}
$$

Das Ergebnis ist positiv, da das Integral von $N_1(x)$ über die Länge des Elements berechnet wird. Die Funktion $N_1(x) = 1 - \frac{x}{l_e}$ ist im Bereich von $x = 0$ bis $x = l_e$ positiv.

Wenn du das Integral aufstellst: $\int_0^{l_e} \left(1 - \frac{x}{l_e}\right) dx$ wird jeder Term einzeln integriert: 

$$\int_0^{l_e} 1 dx = \left[x\right]_0^{l_e} = l_e $$ 

$$ \int_0^{l_e} -\frac{x}{l_e} , dx = -\frac{1}{l_e} \cdot \left[\frac{x^2}{2}\right]_0^{l_e} = -\frac{1}{l_e} \cdot \frac{l_e^2}{2} = -\frac{l_e}{2} $$

Das Endergebnis ist: $$ l_e - \frac{l_e}{2} = \frac{l_e}{2} $$

Es gibt keinen negativen Vorzeichenfehler, da die Funktion $N_1(x)$ im gesamten Integrationsbereich positiv bleibt.

$$
\int_0^{l_e} N_2(x) \, dx = \int_0^{l_e} \frac{x}{l_e} dx = l_e \cdot \frac{1}{2}
$$

Das Ergebnis ist:
$$
\int_0^{l_e} (N_1, N_2)^T \, dx = \frac{l_e}{2} \cdot (1, 1)^T
$$

### 4. Endergebnis
Das Integral ergibt:
$$
\int_{V_e} (N_1, N_2)^T \cdot f_b \, dV = f_b \cdot A \cdot \frac{l_e}{2} \cdot (1, 1)^T
$$

### Python-Code
Hier ist der Python-Code zur Berechnung:

```python
import sympy as sp

# Variablen definieren
x = sp.Symbol('x')
le = sp.Symbol('le', positive=True)
A = sp.Symbol('A', positive=True)
fb = sp.Symbol('fb', positive=True)

# Formfunktionen
N1 = 1 - x / le
N2 = x / le

# Integral berechnen
integral_N1 = sp.integrate(N1, (x, 0, le))
integral_N2 = sp.integrate(N2, (x, 0, le))

# Ergebnis zusammenstellen
result = fb * A * sp.Matrix([integral_N1, integral_N2])
print(f"Das Ergebnis ist: {result}")
```

Das Ergebnis des Codes ist:
```
Das Ergebnis ist: Matrix([[fb*A*le/2], [fb*A*le/2]])
```

# Getting the direction cosines to derive the transformation matrix

Um die Richtungskosinus des Fachwerkelements zu berechnen, kannst du die Koordinaten der beiden Knoten verwenden und den Einheitsvektor des Fachwerkelements bestimmen. Der Einheitsvektor gibt die Richtungskosinus an.

### Schritte:
1. Berechne den Richtungsvektor des Fachwerkelements:
   $$
   \text{Richtungsvektor} = \vec{d} = \vec{j} - \vec{i}
   $$
   Dabei sind \(\vec{i}\) und \(\vec{j}\) die Koordinaten der Knoten.

2. Berechne die Länge des Richtungsvektors:
   $$
   |\vec{d}| = \sqrt{d_x^2 + d_y^2 + d_z^2}
   $$

3. Bestimme den Einheitsvektor:
   $$
   \text{Einheitsvektor} = \frac{\vec{d}}{|\vec{d}|}
   $$

### Python-Code:
```python
import numpy as np

def direction_cosine(node_i, node_j):
    # Koordinaten der Knoten
    vec_i = np.array([node_i.x, node_i.y, node_i.z])
    vec_j = np.array([node_j.x, node_j.y, node_j.z])
    
    # Richtungsvektor
    direction_vector = vec_j - vec_i
    
    # Länge des Richtungsvektors
    length = np.linalg.norm(direction_vector)
    
    # Einheitsvektor (Richtungskosinus)
    unit_vector = direction_vector / length
    return unit_vector
```

### Beispiel:
Angenommen, die Knoten haben folgende Koordinaten:
- Knoten \(i\): (0, 0, 0)
- Knoten \(j\): (1, 0, 0)

Der Einheitsvektor ist:
```python
node_i = Node(1, 0, 0, 0)
node_j = Node(2, 1, 0, 0)
cosines = direction_cosine(node_i, node_j)
print(cosines)
```

Das Ergebnis ist:
```
[1. 0. 0.]
```

# Reaction forces at the supports

Um die Auflagerkräfte zu berechnen, verwenden Sie die grundlegende Gleichung des Finite-Elemente-Verfahrens für das gesamte System: R = K * u - F.

Dabei gilt:


R ist der Vektor der Auflagerkräfte.
K ist die vollständige globale Steifigkeitsmatrix (vor Anwendung der Randbedingungen).
u ist der vollständige globale Verschiebungsvektor (einschließlich der Nullen an den Auflagern).
F ist der ursprüngliche Vektor der externen Kräfte.
Sie können eine Methode zu Ihrer TrussModel-Klasse hinzufügen, um diese Berechnung durchzuführen.
