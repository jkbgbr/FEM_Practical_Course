# What if the distributed load is not uniform? Can you show me in detail (e.g. derivation) what happens then?

Wenn die verteilte Last nicht gleichmäßig ist, sondern beispielsweise linear oder quadratisch variiert, muss die Last entlang der Länge des Balkenelements integriert werden, um die äquivalenten Knotenkräfte und Momente zu berechnen. Dies erfordert die Verwendung der Basisfunktionen des Elements, da die Lastverteilung $ q(x) $ in Bezug auf die lokalen Koordinaten $ \xi $ ausgedrückt wird.

### Herleitung:
1. **Lastverteilung $ q(x) $:**
   Die Lastverteilung $ q(x) $ wird in lokalen Koordinaten $ \xi $ umgeschrieben:
   $$
   x = \frac{L}{2} (\xi + 1), \quad dx = \frac{L}{2} d\xi
   $$
   wobei $ L $ die Länge des Balkenelements ist.

2. **Äquivalente Knotenkräfte:**
   Die äquivalenten Knotenkräfte $ f_e $ werden durch die Integration der Lastverteilung $ q(x) $ mit den Basisfunktionen $ N_i(\xi) $ berechnet:
   $$
   f_{e,i} = \int_{-1}^{1} q(x) N_i(\xi) \frac{L}{2} d\xi
   $$

3. **Beispiel: Lineare Lastverteilung $ q(x) = q_0 + q_1 x $:**
   Die Lastverteilung wird in lokale Koordinaten umgeschrieben:
   $$
   q(x) = q_0 + q_1 \frac{L}{2} (\xi + 1)
   $$
   Die äquivalenten Knotenkräfte werden dann berechnet, indem $ q(x) $ mit den Basisfunktionen $ N_i(\xi) $ integriert wird.

### Implementierung:
Hier ist der Python-Code, der die äquivalenten Knotenkräfte für eine beliebige Lastverteilung $ q(\xi) $ berechnet:

```python
import numpy as np

def distributed_load_vector_custom(q_func, length, base_functions):
    """
    Berechnet den Lastvektor für eine nicht-uniforme verteilte Last.

    :param q_func: Funktion der Lastverteilung q(ksi).
    :param length: Länge des Balkenelements.
    :param base_functions: Basisfunktionen des Elements.
    :return: Lastvektor (4x1).
    """
    f_e = np.zeros(4)
    a = length / 2  # Halbe Länge des Elements

    # Numerische Integration über die Basisfunktionen
    ksi_values = np.linspace(-1, 1, 100)  # Diskretisierung des Integrals
    for i in range(4):  # Für jede Basisfunktion
        integrand = q_func(ksi_values) * base_functions(ksi_values)[i]
        f_e[i] = np.trapz(integrand, ksi_values) * a  # Numerische Integration

    return f_e

# Beispiel: Lineare Lastverteilung q(ksi) = q0 + q1 * ksi
def q_linear(ksi):
    q0 = 10  # Konstante Komponente
    q1 = 5   # Lineare Komponente
    return q0 + q1 * ksi

# Basisfunktionen des Balkenelements
def base_functions(ksi):
    return np.array([
        1/4 * (2 - 3 * ksi + ksi**3),
        1/4 * (1 - ksi - ksi**2 + ksi**3),
        1/4 * (2 + 3 * ksi - ksi**3),
        1/4 * (-1 - ksi + ksi**2 + ksi**3)
    ])

# Länge des Balkenelements
length = 2.0

# Berechnung des Lastvektors
f_e = distributed_load_vector_custom(q_linear, length, base_functions)
print("Lastvektor:", f_e)
```

### Erklärung:
- Die Funktion `distributed_load_vector_custom` integriert die Lastverteilung $ q(\xi) $ numerisch über die Basisfunktionen.
- Die Lastverteilung $ q(\xi) $ kann beliebig definiert werden, z.B. linear, quadratisch oder eine andere Funktion.
- Die numerische Integration erfolgt mit der Trapezregel (`np.trapz`).

Dieser Ansatz ermöglicht die Berechnung des Lastvektors für beliebige Lastverteilungen.