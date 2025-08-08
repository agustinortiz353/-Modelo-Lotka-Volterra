import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# Parametros
a = 0.1 #tasa de natalidad de conejos
b = 0.01 #tasa de depredacion
d = 0.01#tasa de reproduccion de zorros
e = 0.1 #tasa de muertes de zorros


# Inicializacion
n_conejos = 40 # Numero de conejos 
n_zorros = 9 # Numero de zorros
limite = 100

# Posiciones iniciales
conejos_pos = np.random.rand(n_conejos, 2) * limite
zorros_pos = np.random.rand(n_zorros, 2) * limite

# Variables internas para poblaciones continuas
pop_conejos = float(n_conejos)
pop_zorros = float(n_zorros)

# Acumuladores para cambio fraccional
acum_conejos = 0.0
acum_zorros = 0.0

# Historia de posiciones
historia_conejos = []
historia_zorros = []

# Listas para guardar cantidades en cada frame
cant_conejos = []
cant_zorros = []

# Simulación
frames = 300
dt = 1  # paso temporal arbitrario

for t in range(frames):
    C = pop_conejos
    Z = pop_zorros

    dC = (a * C - b * C * Z) * dt #Cambio en la cantidad de conejos
    dZ = (d * C * Z - e * Z) * dt #Cambio en la cantidad de zorros

    pop_conejos += dC
    pop_zorros += dZ

    # Evita poblaciones negativas(Por ejemplo, -3 zorros)
    pop_conejos = max(pop_conejos, 0)
    pop_zorros = max(pop_zorros, 0)

    # Actualizamos acumuladores fraccionales
    acum_conejos += pop_conejos - n_conejos
    acum_zorros += pop_zorros - n_zorros

    # Añadir o quitar conejos si acumulador supera 1 o es menor que -1
    while acum_conejos >= 1:
        nuevos = np.random.rand(1, 2) * limite
        conejos_pos = np.vstack([conejos_pos, nuevos])
        n_conejos += 1
        acum_conejos -= 1
    while acum_conejos <= -1 and n_conejos > 0:
        conejos_pos = conejos_pos[:-1]
        n_conejos -= 1
        acum_conejos += 1

    # Añadir o quitar zorros, igual que el anterior misma logica
    while acum_zorros >= 1:
        nuevos = np.random.rand(1, 2) * limite
        zorros_pos = np.vstack([zorros_pos, nuevos])
        n_zorros += 1
        acum_zorros -= 1
    while acum_zorros <= -1 and n_zorros > 0:
        zorros_pos = zorros_pos[:-1]
        n_zorros -= 1
        acum_zorros += 1

    def mover(pos, paso=2): #Simplemente hace que se muevan aleatoriamente en el mapa
        return np.clip(pos + (np.random.rand(*pos.shape) - 0.5) * paso, 0, limite)

    conejos_pos = mover(conejos_pos)
    zorros_pos = mover(zorros_pos)

    historia_conejos.append(conejos_pos.copy())
    historia_zorros.append(zorros_pos.copy())

    cant_conejos.append(n_conejos)
    cant_zorros.append(n_zorros)

# === Animación(No tiene que ver con la simulación, solo es para representación) ===

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.set_xlim(0, limite)
ax1.set_ylim(0, limite)
ax1.set_title("Campo de interacción")
ax1.axis('on')

ax2.set_ylim(0, max(max(cant_conejos), max(cant_zorros)) + 20)
bar_conejos = ax2.bar(["Conejos"], [0], color='green')
bar_zorros = ax2.bar(["Zorros"], [0], color='red')
ax2.set_title("Población")

# Para cargar imágenes (Con los archivos "rabbit.png" y "fox.png" en el directorio)
img_conejo = mpimg.imread("rabbit.png")
img_zorro = mpimg.imread("fox.png")

conejo_objs = []
zorro_objs = []

def init_imagenes(ax, posiciones, img, escala=0.05):
    objetos = []
    for pos in posiciones:
        imagebox = OffsetImage(img, zoom=escala)
        ab = AnnotationBbox(imagebox, pos, frameon=False)
        ax.add_artist(ab)
        objetos.append(ab)
    return objetos

conejo_objs = init_imagenes(ax1, historia_conejos[0], img_conejo, escala=0.05)
zorro_objs = init_imagenes(ax1, historia_zorros[0], img_zorro, escala=0.07)

def update(frame):
    conejos = historia_conejos[frame]
    zorros = historia_zorros[frame]

    for i, pos in enumerate(conejos):
        if i < len(conejo_objs):
            conejo_objs[i].xybox = pos
        else:
            imgbox = OffsetImage(img_conejo, zoom=0.05)
            ab = AnnotationBbox(imgbox, pos, frameon=False)
            ax1.add_artist(ab)
            conejo_objs.append(ab)
    for i in range(len(conejo_objs) - 1, len(conejos) - 1, -1):
        conejo_objs[i].remove()
        conejo_objs.pop()

    for i, pos in enumerate(zorros):
        if i < len(zorro_objs):
            zorro_objs[i].xybox = pos
        else:
            imgbox = OffsetImage(img_zorro, zoom=0.07)
            ab = AnnotationBbox(imgbox, pos, frameon=False)
            ax1.add_artist(ab)
            zorro_objs.append(ab)
    for i in range(len(zorro_objs) - 1, len(zorros) - 1, -1):
        zorro_objs[i].remove()
        zorro_objs.pop()

    bar_conejos[0].set_height(len(conejos))
    bar_zorros[0].set_height(len(zorros))

    ax1.figure.canvas.draw_idle()

def on_close(event):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,5))
    plt.plot(cant_conejos, label='Conejos', color='green')
    plt.plot(cant_zorros, label='Zorros', color='red')
    plt.title('Evolución de poblaciones final')
    plt.xlabel('Tiempo')
    plt.ylabel('Cantidad')
    plt.legend()
    plt.grid(True)
    plt.show()

fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=False)
plt.tight_layout()

ani.save('zorros_conejos.gif', writer='pillow', fps=10)

plt.show()
