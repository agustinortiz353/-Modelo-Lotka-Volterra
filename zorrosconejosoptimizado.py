import numpy as np
import matplotlib.pyplot as plt

# Parámetros
a = 0.1   # tasa de natalidad de conejos
b = 0.01  # tasa de depredación
d = 0.01 # tasa de reproducción de zorros
e = 0.1  # tasa de muertes de zorros

# Inicialización
n_conejos = 9  # Número inicial de conejos 
n_zorros = 1    # Número inicial de zorros
limite = 100    # Límite del espacio (no se usa en este modelo simplificado)

# Variables internas para poblaciones continuas
pop_conejos = float(n_conejos)
pop_zorros = float(n_zorros)

# Acumuladores para cambio fraccional
acum_conejos = 0.0
acum_zorros = 0.0

# Listas para guardar cantidades en cada paso
cant_conejos = []
cant_zorros = []

# Simulación
frames = 15000
dt = 1/10  # paso temporal

for t in range(frames):
    C = pop_conejos
    Z = pop_zorros

    # Ecuaciones de Lotka-Volterra
    dC = (a * C - b * C * Z) * dt
    dZ = (d * C * Z - e * Z) * dt

    pop_conejos += dC
    pop_zorros += dZ

    # Evita poblaciones negativas
    pop_conejos = max(pop_conejos, 0)
    pop_zorros = max(pop_zorros, 0)

    # Actualizamos acumuladores fraccionales
    acum_conejos += pop_conejos - n_conejos
    acum_zorros += pop_zorros - n_zorros

    # Añadir o quitar conejos si acumulador supera 1 o es menor que -1
    while acum_conejos >= 1:
        n_conejos += 1
        acum_conejos -= 1
    while acum_conejos <= -1 and n_conejos > 0:
        n_conejos -= 1
        acum_conejos += 1

    # Añadir o quitar zorros
    while acum_zorros >= 1:
        n_zorros += 1
        acum_zorros -= 1
    while acum_zorros <= -1 and n_zorros > 0:
        n_zorros -= 1
        acum_zorros += 1

    # Guardamos las cantidades actuales
    cant_conejos.append(n_conejos)
    cant_zorros.append(n_zorros)

# Graficar los resultados finales
plt.figure(figsize=(10, 6))
plt.plot(cant_conejos, label='Conejos', color='green')
plt.plot(cant_zorros, label='Zorros', color='red')
plt.title('Evolución de las poblaciones de conejos y zorros')
plt.xlabel('Tiempo')
plt.ylabel('Población')
plt.legend()
plt.grid(True)
plt.show()