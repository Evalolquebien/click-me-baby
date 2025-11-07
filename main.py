import pygame
import random
import sys



try:

    pygame.init()

    
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Haz clic en los círculos rosados")

    
    ROSA = (255, 105, 180)
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    
    clock = pygame.time.Clock()

    
    radio = 40
    puntaje = 0
    tiempo_circulo = 1000  # milisegundos que dura cada círculo
    ultimo_cambio = pygame.time.get_ticks()

    
    x = random.randint(radio, ANCHO - radio)
    y = random.randint(radio, ALTO - radio)
    circulo_visible = True

    
    fuente = pygame.font.SysFont("Arial", 30)

    
    while True:
        pantalla.fill(BLANCO)
        ahora = pygame.time.get_ticks()

       
        if ahora - ultimo_cambio > tiempo_circulo:
            x = random.randint(radio, ANCHO - radio)
            y = random.randint(radio, ALTO - radio)
            ultimo_cambio = ahora
            circulo_visible = True

        
        if circulo_visible:
            pygame.draw.circle(pantalla, ROSA, (x, y), radio)

        
        texto = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
        pantalla.blit(texto, (10, 10))

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and circulo_visible:
                try:
                    pos_click = pygame.mouse.get_pos()
                    distancia = ((pos_click[0] - x) ** 2 + (pos_click[1] - y) ** 2) ** 0.5
                    if distancia <= radio:
                        puntaje += 1
                        circulo_visible = False
                    else:
                        puntaje -= 1 if puntaje > 0 else 0
                except Exception as e:
                    print("Error al procesar el clic:", e)

        pygame.display.flip()
        clock.tick(60)


except pygame.error as e:
    print("Error de Pygame:", e)

except Exception as e:
    print("Ocurrió un error inesperado:", e)

finally:
    
    pygame.quit()
    print("Juego finalizado.")

