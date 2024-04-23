import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class Vector3:
    def __init__(self, e0=0, e1=0, e2=0):
        self.e = [e0, e1, e2]

class OrbitalEntity:
    def __init__(self, e0=0, e1=0, e2=0, e3=0, e4=0, e5=0, e6=0, name="", density=0, fluid_particles=None):
        self.e = [e0, e1, e2, e3, e4, e5, e6]
        self.name = name
        self.density = density
        self.fluid_particles = fluid_particles

# Definición de constantes
t_0 = 0
t = t_0
t_end = 86400 * 365 * 2  # reducir a 2 años en lugar de 10
dt = 86400 * 10  # aumentar el paso de tiempo a 10 días
BIG_G = 6.67e-11  # constante gravitacional

# Número de asteroides a agregar
N_ASTEROIDS = 0

# Inicialización de las entidades orbitales
orbital_entities = [
    OrbitalEntity(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.989e30, "Sol", density=1410),  # Una estrella similar al sol
    OrbitalEntity(57.909e9, 0.0, 0.0, 0.0, 47.36e3, 0.0, 0.33011e24, "Mercurio", density=5427),
    OrbitalEntity(108.209e9, 0.0, 0.0, 0.0, 35.02e3, 0.0, 4.8675e24, "Venus", density=5243),
    OrbitalEntity(149.596e9, 0.0, 0.0, 0.0, 29.78e3, 0.0, 5.9724e24, "Tierra", density=5514),
    OrbitalEntity(227.923e9, 0.0, 0.0, 0.0, 24.07e3, 0.0, 0.64171e24, "Marte", density=3933),
    OrbitalEntity(778.570e9, 0.0, 0.0, 0.0, 13e3, 0.0, 1898.19e24, "Jupiter", density=1326),
    OrbitalEntity(1433.529e9, 0.0, 0.0, 0.0, 9.68e3, 0.0, 568.34e24, "Saturno", density=687),
    OrbitalEntity(2872.463e9, 0.0, 0.0, 0.0, 6.80e3, 0.0, 86.813e24, "Urano", density=1270),
    OrbitalEntity(4495.060e9, 0.0, 0.0, 0.0, 5.43e3, 0.0, 102.413e24, "Neptuno", density=1638)
]

# Tamaño de los planetas (radio relativo para la visualización)
planet_radii = {
    "Sol": 0.2,
    "Mercurio": 0.02,
    "Venus": 0.05,
    "Tierra": 0.05,
    "Marte": 0.03,
    "Jupiter": 0.15,
    "Saturno": 0.12,
    "Urano": 0.1,
    "Neptuno": 0.1
}

# Imágenes de los planetas
planet_images = {
    "Sol": "sun.png",
    "Mercurio": "mercury.png",
    "Venus": "venus.png",
    "Tierra": "earth.png",
    "Marte": "mars.png",
    "Jupiter": "jupiter.png",
    "Saturno": "saturn.png",
    "Urano": "uranus.png",
    "Neptuno": "neptune.png"
}

# Bucle de simulación
for t in range(t_0, t_end, dt):
    for m1_idx in range(9 + N_ASTEROIDS):
        a_g = Vector3()
        for m2_idx in range(9 + N_ASTEROIDS):
            if m2_idx != m1_idx:
                r_vector = Vector3(
                    orbital_entities[m1_idx].e[0] - orbital_entities[m2_idx].e[0],
                    orbital_entities[m1_idx].e[1] - orbital_entities[m2_idx].e[1],
                    orbital_entities[m1_idx].e[2] - orbital_entities[m2_idx].e[2]
                )

                r_mag = math.sqrt(
                    r_vector.e[0] ** 2 +
                    r_vector.e[1] ** 2 +
                    r_vector.e[2] ** 2
                )
                r_unit_vector = Vector3(
                    r_vector.e[0] / r_mag,
                    r_vector.e[1] / r_mag,
                    r_vector.e[2] / r_mag
                )

                acceleration = -BIG_G * orbital_entities[m2_idx].e[6] / (r_mag ** 2)
                a_g.e[0] += acceleration * r_unit_vector.e[0]
                a_g.e[1] += acceleration * r_unit_vector.e[1]
                a_g.e[2] += acceleration * r_unit_vector.e[2]

        orbital_entities[m1_idx].e[3] += a_g.e[0] * dt
        orbital_entities[m1_idx].e[4] += a_g.e[1] * dt
        orbital_entities[m1_idx].e[5] += a_g.e[2] * dt

        orbital_entities[m1_idx].e[0] += orbital_entities[m1_idx].e[3] * dt
        orbital_entities[m1_idx].e[1] += orbital_entities[m1_idx].e[4] * dt
        orbital_entities[m1_idx].e[2] += orbital_entities[m1_idx].e[5] * dt

# Graficar las órbitas de las entidades orbitales
fig, ax = plt.subplots()

# Configuración del fondo del gráfico (espacio exterior)
ax.set_facecolor('black')

# Dibujar las órbitas visuales de los planetas
for planet in orbital_entities[1:]:
    orbita = Circle((0, 0), radius=planet.e[0], color='gray', fill=False, linestyle='--', linewidth=0.5)
    ax.add_patch(orbita)

# Dibujar los planetas con imágenes y etiquetas
for planet in orbital_entities[1:]:
    image_path = planet_images.get(planet.name)
    if image_path:
        image = plt.imread(image_path)
        imagebox = OffsetImage(image, zoom=planet_radii[planet.name])
        ab = AnnotationBbox(imagebox, (planet.e[0], planet.e[1]), frameon=False)
        ax.add_artist(ab)
        ax.annotate(planet.name, (planet.e[0], planet.e[1]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='white')

# Configuración del gráfico
plt.xlabel('Posición en X (m)')
plt.ylabel('Posición en Y (m)')
plt.title('Órbitas de las entidades orbitales y planetas')
plt.grid(True)

# Mostrar el gráfico
plt.show()
