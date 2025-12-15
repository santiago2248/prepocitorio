import pygame
import random
import sys
import math


# Inicializar Pygame
pygame.init()


# --- 1. CONFIGURACIÓN DE LA VENTANA ---
ANCHO = 500
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Homero Atrapando Donas")


# --- 2. CONFIGURACIÓN DEL JUGADOR ---
player_x = ANCHO // 2 - 20
player_y = ALTO - 80
player_size = 80
player_vel = 12


# --- 3. CONFIGURACIÓN DE OBJETOS (DONAS) ---
obstaculos = []
BASE_SPAWN_RATE = 0.02
BASE_DONUT_VEL = 4


# --- 4. CONFIGURACIÓN GENERAL ---
clock = pygame.time.Clock()
running = True
score = 0      
donas_perdidas = 0   # ← contador de donas perdidas
font_sm = pygame.font.Font(None, 36)


# Colores
COLOR_FONDO = (30, 30, 30)
COLOR_HOMERO = (255, 204, 0)
COLOR_DONA = (255, 105, 180)
COLOR_TEXTO = (255, 255, 255)


# Función para dibujar la puntuación
def draw_score():
    score_text = font_sm.render(f"Donas comidas: {score}", True, COLOR_TEXTO)
    pantalla.blit(score_text, (10, 10))


# 🔥 NUEVO: texto de donas perdidas arriba derecha
def draw_lost():
    lost_text = font_sm.render(f"Donas perdidas: {donas_perdidas}", True, COLOR_TEXTO)
    pantalla.blit(lost_text, (ANCHO - lost_text.get_width() - 10, 10))


# Función para dificultad
def calculate_difficulty(current_score):
    difficulty_level = 1 + math.log10(current_score / 10 + 1)
    current_spawn_rate = min(BASE_SPAWN_RATE * difficulty_level, 0.15)
    min_vel = BASE_DONUT_VEL
    max_vel = min_vel + int(difficulty_level * 1.5)
    return current_spawn_rate, min_vel, max_vel




# BUCLE PRINCIPAL DEL JUEGO
while running:
    clock.tick(60)


    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False


    spawn_rate, min_vel, max_vel = calculate_difficulty(score)


    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if teclas[pygame.K_RIGHT] and player_x < ANCHO - player_size:
        player_x += player_vel


    # Crear donas nuevas
    if random.random() < spawn_rate:
        obstaculos.append([
            random.randint(0, ANCHO - 30),
            -30,
            30,
            random.randint(min_vel, max_vel)
        ])


    nuevos_obstaculos = []
    jugador_rect = pygame.Rect(player_x, player_y, player_size, player_size)


    for obs in obstaculos:
        obs[1] += obs[3]
        obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[2])


        # Si toca al jugador → suma puntos
        if jugador_rect.colliderect(obs_rect):
            score += 1
            continue


        # Si la dona sale por abajo
        if obs[1] > ALTO:
            donas_perdidas += 1


            # Si pierde 3 → fin del juego
            if donas_perdidas >= 5:
                print("Perdiste! Se escaparon 5 donas.")
                running = False
            continue


        nuevos_obstaculos.append(obs)


    obstaculos = nuevos_obstaculos


    # DIBUJAR
    pantalla.fill(COLOR_FONDO)


    center_player_x = player_x + player_size // 2
    center_player_y = player_y + player_size // 2
    pygame.draw.circle(pantalla, COLOR_HOMERO, (center_player_x, center_player_y), player_size // 2)


    for o in obstaculos:
        cx = o[0] + o[2] // 2
        cy = o[1] + o[2] // 2
        pygame.draw.circle(pantalla, COLOR_DONA, (cx, cy), o[2] // 2)
        pygame.draw.circle(pantalla, COLOR_FONDO, (cx, cy), o[2] // 4)


    draw_score()
    draw_lost()   # ← DIBUJAR TEXTO NUEVO


    pygame.display.flip()


pygame.quit()
sys.exit()
