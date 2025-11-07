import pygame
import random
import sys

# ----------------------------------------
# JUEGO: HAZ CLIC EN LOS CÍRCULOS ROSADOS
# Con fondo, beso, sonidos y marco del puntaje
# ----------------------------------------

try:
    # Inicializar Pygame
    pygame.init()

    # Configurar pantalla
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Haz clic en los círculos rosados 💖")

    # Colores
    ROSA = (255, 105, 180)
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    FUCSIA = (255, 20, 147)

    # Reloj del juego
    clock = pygame.time.Clock()

    # Variables del juego
    radio = 40
    puntaje = 0
    tiempo_circulo = 1000
    ultimo_cambio = pygame.time.get_ticks()
    circulo_visible = True
    besos = []  # lista para guardar las posiciones de los besos

    # Cargar fondo
    try:
        fondo = pygame.image.load("imagenes/fondoo.jpg")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except pygame.error:
        fondo = None
        print("⚠️ No se encontró la imagen de fondo.")

    # Cargar imagen de beso
    try:
        beso_img = pygame.image.load("imagenes/beso.jpg")
        beso_img = pygame.transform.scale(beso_img, (80, 80))
    except pygame.error:
        beso_img = None
        print("⚠️ No se encontró la imagen de beso.")

    # Cargar sonidos
    try:
        sonido_pop = pygame.mixer.Sound("sonidos/pop.mp3")
        sonido_error = pygame.mixer.Sound("sonidos/error.mp3")
    except pygame.error:
        sonido_pop = None
        sonido_error = None
        print("⚠️ No se pudieron cargar los sonidos.")

    # Fuente de texto
    fuente = pygame.font.SysFont("Arial", 32, bold=True)

    # Crear primer círculo
    x = random.randint(radio, ANCHO - radio)
    y = random.randint(radio, ALTO - radio)

    # Bucle principal
    while True:
        # Dibujar fondo
        if fondo:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(BLANCO)

        ahora = pygame.time.get_ticks()

        # Generar nuevo círculo cada cierto tiempo
        if ahora - ultimo_cambio > tiempo_circulo:
            x = random.randint(radio, ANCHO - radio)
            y = random.randint(radio, ALTO - radio)
            ultimo_cambio = ahora
            circulo_visible = True

        # Dibujar círculo rosado
        if circulo_visible:
            pygame.draw.circle(pantalla, ROSA, (x, y), radio)

        # Dibujar besos acumulados
        if beso_img:
            for pos in besos:
                pantalla.blit(beso_img, pos)

        # Mostrar puntaje con marco decorativo
        texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        texto_rect = texto.get_rect(topleft=(10, 10))
        marco_rect = pygame.Rect(texto_rect.x - 10, texto_rect.y - 5,
                                 texto_rect.width + 20, texto_rect.height + 10)
        pygame.draw.rect(pantalla, FUCSIA, marco_rect, border_radius=10)
        pygame.draw.rect(pantalla, NEGRO, marco_rect, 3, border_radius=10)
        pantalla.blit(texto, texto_rect)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                try:
                    pos_click = pygame.mouse.get_pos()
                    distancia = ((pos_click[0] - x) ** 2 + (pos_click[1] - y) ** 2) ** 0.5

                    if distancia <= radio and circulo_visible:
                        puntaje += 1
                        circulo_visible = False
                        if sonido_pop:
                            sonido_pop.play()
                    else:
                        puntaje -= 1 if puntaje > 0 else 0
                        if sonido_error:
                            sonido_error.play()
                        if beso_img:
                            besos.append((pos_click[0] - 40, pos_click[1] - 40))
                except Exception as e:
                    print("Error al procesar el clic:", e)

        pygame.display.flip()
        clock.tick(60)

# Captura de errores generales
except pygame.error as e:
    print("Error de Pygame:", e)

except Exception as e:
    print("Ocurrió un error inesperado:", e)

finally:
    pygame.quit()
    print("Juego finalizado.")
