import pygame
import random
import sys

pygame.init()

# =========================================================
# CONFIGURACIÓN
# =========================================================

ANCHO = 600
ALTO = 500
TAMANO = 20
HUD = 60

FILAS = (ALTO - HUD) // TAMANO
COLUMNAS = ANCHO // TAMANO

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi juego de la serpiente")

reloj = pygame.time.Clock()

fuente = pygame.font.SysFont("Arial", 25, bold=True)
fuente_grande = pygame.font.SysFont("Arial", 42, bold=True)

# =========================================================
# COLORES
# =========================================================

NEGRO = (18, 18, 28)
CUADRICULA = (35, 38, 50)

VERDE = (40, 220, 100)
VERDE_CABEZA = (100, 255, 130)

ROJO = (255, 65, 75)

BLANCO = (255, 255, 255)
AMARILLO = (255, 215, 70)

OBSTACULO = (130, 80, 45)
BORDE_OBSTACULO = (190, 120, 60)


# =========================================================
# CREAR OBSTÁCULOS
# =========================================================

def crear_obstaculos(nivel, serpiente):

    obstaculos = set()

    cantidad = 4 + (nivel - 1) * 3

    cantidad = min(cantidad, 35)

    intentos = 0

    while len(obstaculos) < cantidad and intentos < 1000:

        intentos += 1

        x = random.randint(1, COLUMNAS - 2)
        y = random.randint(1, FILAS - 2)

        posicion = (x, y)

        if posicion in serpiente:
            continue

        if 7 <= x <= 13 and 7 <= y <= 13:
            continue

        obstaculos.add(posicion)

    return obstaculos


# =========================================================
# CREAR COMIDA
# =========================================================

def crear_comida(serpiente, obstaculos):

    while True:

        comida = (
            random.randint(0, COLUMNAS - 1),
            random.randint(0, FILAS - 1)
        )

        if comida not in serpiente and comida not in obstaculos:
            return comida


# =========================================================
# REINICIAR JUEGO
# =========================================================

def reiniciar():

    serpiente = [
        (10, 10),
        (9, 10),
        (8, 10)
    ]

    direccion = (1, 0)
    siguiente = direccion

    nivel = 1

    obstaculos = crear_obstaculos(
        nivel,
        serpiente
    )

    comida = crear_comida(
        serpiente,
        obstaculos
    )

    puntos = 0

    perdido = False

    pausado = False

    return (
        serpiente,
        direccion,
        siguiente,
        comida,
        puntos,
        perdido,
        pausado,
        obstaculos
    )


# =========================================================
# DIBUJAR TEXTO
# =========================================================

def dibujar_texto(
    texto,
    fuente,
    color,
    x,
    y,
    centro=False
):

    imagen = fuente.render(
        texto,
        True,
        color
    )

    rect = imagen.get_rect()

    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    pantalla.blit(imagen, rect)


# =========================================================
# DIBUJAR OBSTÁCULOS
# =========================================================

def dibujar_obstaculos(obstaculos):

    for x, y in obstaculos:

        rect = (
            x * TAMANO + 1,
            HUD + y * TAMANO + 1,
            TAMANO - 2,
            TAMANO - 2
        )

        pygame.draw.rect(
            pantalla,
            OBSTACULO,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            pantalla,
            BORDE_OBSTACULO,
            rect,
            2,
            border_radius=4
        )


# =========================================================
# DIBUJAR TODO EL JUEGO
# =========================================================

def dibujar(
    serpiente,
    comida,
    puntos,
    nivel,
    perdido,
    pausado,
    obstaculos
):

    pantalla.fill(NEGRO)

    # =====================================================
    # BARRA SUPERIOR
    # =====================================================

    pygame.draw.rect(
        pantalla,
        (28, 30, 43),
        (0, 0, ANCHO, HUD)
    )

    dibujar_texto(
        f"Puntos: {puntos}",
        fuente,
        BLANCO,
        15,
        15
    )

    dibujar_texto(
        f"Nivel: {nivel}",
        fuente,
        AMARILLO,
        235,
        15
    )

    # =====================================================
    # VELOCIDAD MÁS LENTA
    # =====================================================

    velocidad = min(
        4 + (nivel - 1),
        10
    )

    dibujar_texto(
        f"Velocidad: {velocidad}",
        fuente,
        BLANCO,
        400,
        15
    )

    # =====================================================
    # CUADRÍCULA
    # =====================================================

    for x in range(
        0,
        ANCHO,
        TAMANO
    ):

        pygame.draw.line(
            pantalla,
            CUADRICULA,
            (x, HUD),
            (x, ALTO)
        )

    for y in range(
        HUD,
        ALTO,
        TAMANO
    ):

        pygame.draw.line(
            pantalla,
            CUADRICULA,
            (0, y),
            (ANCHO, y)
        )

    # =====================================================
    # OBSTÁCULOS
    # =====================================================

    dibujar_obstaculos(obstaculos)

    # =====================================================
    # COMIDA
    # =====================================================

    cx, cy = comida

    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            cx * TAMANO + 2,
            HUD + cy * TAMANO + 2,
            TAMANO - 4,
            TAMANO - 4
        ),
        border_radius=6
    )

    # =====================================================
    # SERPIENTE
    # =====================================================

    for i, (x, y) in enumerate(serpiente):

        if i == 0:
            color = VERDE_CABEZA
        else:
            color = VERDE

        pygame.draw.rect(
            pantalla,
            color,
            (
                x * TAMANO + 1,
                HUD + y * TAMANO + 1,
                TAMANO - 2,
                TAMANO - 2
            ),
            border_radius=5
        )

    # =====================================================
    # OJOS
    # =====================================================

    hx, hy = serpiente[0]

    pygame.draw.circle(
        pantalla,
        NEGRO,
        (
            hx * TAMANO + 7,
            HUD + hy * TAMANO + 7
        ),
        2
    )

    pygame.draw.circle(
        pantalla,
        NEGRO,
        (
            hx * TAMANO + 14,
            HUD + hy * TAMANO + 7
        ),
        2
    )

    # =====================================================
    # PAUSA
    # =====================================================

    if pausado:

        dibujar_texto(
            "PAUSA",
            fuente_grande,
            AMARILLO,
            ANCHO // 2,
            ALTO // 2,
            True
        )

        dibujar_texto(
            "Presiona ESPACIO para continuar",
            fuente,
            BLANCO,
            ANCHO // 2,
            ALTO // 2 + 45,
            True
        )

    # =====================================================
    # GAME OVER
    # =====================================================

    if perdido:

        dibujar_texto(
            "¡GAME OVER!",
            fuente_grande,
            ROJO,
            ANCHO // 2,
            ALTO // 2 - 35,
            True
        )

        dibujar_texto(
            f"Puntuacion: {puntos}",
            fuente,
            BLANCO,
            ANCHO // 2,
            ALTO // 2 + 15,
            True
        )

        dibujar_texto(
            "Pulsa R para volver a jugar",
            fuente,
            AMARILLO,
            ANCHO // 2,
            ALTO // 2 + 55,
            True
        )

    pygame.display.flip()


# =========================================================
# INICIAR EL JUEGO
# =========================================================

(
    serpiente,
    direccion,
    siguiente,
    comida,
    puntos,
    perdido,
    pausado,
    obstaculos
) = reiniciar()

acumulado = 0

nivel_anterior = 1


# =========================================================
# BUCLE PRINCIPAL
# =========================================================

while True:

    dt = reloj.tick(60) / 1000

    # =====================================================
    # EVENTOS
    # =====================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            # ESC = salir
            if evento.key == pygame.K_ESCAPE:

                pygame.quit()
                sys.exit()

            # R = reiniciar
            if evento.key == pygame.K_r and perdido:

                (
                    serpiente,
                    direccion,
                    siguiente,
                    comida,
                    puntos,
                    perdido,
                    pausado,
                    obstaculos
                ) = reiniciar()

                acumulado = 0

                nivel_anterior = 1

            # ESPACIO = pausa
            if evento.key == pygame.K_SPACE and not perdido:

                pausado = not pausado

            # =================================================
            # CONTROLES
            # =================================================

            if not perdido and not pausado:

                if evento.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    if direccion != (0, 1):

                        siguiente = (0, -1)

                elif evento.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    if direccion != (0, -1):

                        siguiente = (0, 1)

                elif evento.key in (
                    pygame.K_LEFT,
                    pygame.K_a
                ):

                    if direccion != (1, 0):

                        siguiente = (-1, 0)

                elif evento.key in (
                    pygame.K_RIGHT,
                    pygame.K_d
                ):

                    if direccion != (-1, 0):

                        siguiente = (1, 0)

    # =====================================================
    # ACTUALIZAR JUEGO
    # =====================================================

    if not perdido and not pausado:

        nivel = puntos // 5 + 1

        # =================================================
        # CAMBIO DE NIVEL
        # =================================================

        if nivel != nivel_anterior:

            nivel_anterior = nivel

            obstaculos = crear_obstaculos(
                nivel,
                serpiente
            )

            comida = crear_comida(
                serpiente,
                obstaculos
            )

        # =================================================
        # VELOCIDAD MÁS LENTA
        # =================================================

        velocidad = min(
            4 + (nivel - 1),
            10
        )

        intervalo = 1 / velocidad

        acumulado += dt

        # =================================================
        # MOVIMIENTO
        # =================================================

        while acumulado >= intervalo:

            acumulado -= intervalo

            direccion = siguiente

            hx, hy = serpiente[0]

            dx, dy = direccion

            nueva_cabeza = (
                hx + dx,
                hy + dy
            )

            nx, ny = nueva_cabeza

            # =================================================
            # CHOQUE CON LAS PAREDES
            # =================================================

            if (
                nx < 0
                or nx >= COLUMNAS
                or ny < 0
                or ny >= FILAS
            ):

                perdido = True
                break

            # =================================================
            # CHOQUE CON OBSTÁCULOS
            # =================================================

            if nueva_cabeza in obstaculos:

                perdido = True
                break

            # =================================================
            # COMIDA
            # =================================================

            comio = nueva_cabeza == comida

            # =================================================
            # CUERPO
            # =================================================

            if comio:

                cuerpo = serpiente

            else:

                cuerpo = serpiente[:-1]

            # =================================================
            # CHOQUE CON LA SERPIENTE
            # =================================================

            if nueva_cabeza in cuerpo:

                perdido = True
                break

            # =================================================
            # AGREGAR CABEZA
            # =================================================

            serpiente.insert(
                0,
                nueva_cabeza
            )

            # =================================================
            # COMER
            # =================================================

            if comio:

                puntos += 1

                comida = crear_comida(
                    serpiente,
                    obstaculos
                )

            else:

                serpiente.pop()

    # =====================================================
    # NIVEL
    # =====================================================

    nivel = puntos // 5 + 1

    # =====================================================
    # DIBUJAR
    # =====================================================

    dibujar(
        serpiente,
        comida,
        puntos,
        nivel,
        perdido,
        pausado,
        obstaculos
    )