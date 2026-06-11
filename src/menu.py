import pygame
import sys

# 1. Inicializar Pygame
pygame.init()

# --- CONFIGURACIÓN DE LA VENTANA ---
ANCHO_VENTANA = 1300
ALTO_VENTANA = 700
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Menú Principal")

reloj = pygame.time.Clock()

# --- CONFIGURACIÓN DE LA IMAGEN DE FONDO ---
ANCHO_FONDO = 1450
ALTO_FONDO = 900

try:
    imagen_original = pygame.image.load("assets/images/fondo_menu.png")
except pygame.error:
    print("¡Error! No se pudo encontrar la imagen 'fondo_menu.png'.")
    pygame.quit()
    sys.exit()

fondo_ajustado = pygame.transform.scale(imagen_original, (ANCHO_FONDO, ALTO_FONDO))
pos_x = (ANCHO_VENTANA - ANCHO_FONDO) // 2
pos_y = (ALTO_VENTANA - ALTO_FONDO) // 2


# --- CAPA NEGRA DE OPACIDAD (EFECTO GRISÁCEO) ---
capa_grisacea = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
capa_grisacea.fill((0, 0, 0))
capa_grisacea.set_alpha(140) 


# --- CONFIGURACIÓN DEL TÍTULO ---
try:
    titulo_original = pygame.image.load("assets/images/titulo_menu.png")
except pygame.error:
    print("¡Error! No se pudo encontrar la imagen 'titulo_menu.png'.")
    pygame.quit()
    sys.exit()

# Ajusta el tamaño del título aquí (por ejemplo: 600 de ancho y 150 de alto)
ANCHO_TITULO, ALTO_TITULO = 700, 300
titulo_img = pygame.transform.scale(titulo_original, (ANCHO_TITULO, ALTO_TITULO))

# Posicionamos el título centrado horizontalmente y en la parte superior (Y = 100)
titulo_rect = titulo_img.get_rect()
titulo_rect.center = (ANCHO_VENTANA // 2, 150)


# --- CONFIGURACIÓN DEL BOTÓN JUGAR ---
try:
    boton_original = pygame.image.load("assets/images/boton_jugar.png") 
except pygame.error:
    print("¡Error! No se pudo encontrar la imagen 'boton_jugar.png'.")
    pygame.quit()
    sys.exit()

ANCHO_BOTON, ALTO_BOTON = 350, 150
boton_img = pygame.transform.scale(boton_original, (ANCHO_BOTON, ALTO_BOTON))

# El botón queda centrado, un poco más abajo del centro de la pantalla
boton_rect = boton_img.get_rect()
boton_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 120)


# --- CONFIGURACIÓN DEL EFECTO DE TRANSICIÓN (FADE OUT) ---
superficie_negra = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
superficie_negra.fill((0, 0, 0))
alfa_capa = 0                    
superficie_negra.set_alpha(alfa_capa)

transicionando = False
velocidad_transicion = 5  

# Bucle principal
ejecutando = True
while ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN and not transicionando:
            if evento.button == 1: 
                if boton_rect.collidepoint(evento.pos): 
                    transicionando = True
            
    if transicionando:
        alfa_capa += velocidad_transicion
        if alfa_capa >= 255:
            alfa_capa = 255
            ejecutando = False 

    # --- ORDEN DE DIBUJADO (CAPAS DE ATRÁS HACIA ADELANTE) ---
    pantalla.fill((30, 30, 30)) 
    
    # 1. El fondo de la ventana
    pantalla.blit(fondo_ajustado, (pos_x, pos_y))
    
    # 2. La capa oscura que vuelve el fondo grisáceo
    pantalla.blit(capa_grisacea, (0, 0))
    
    # 3. El título (por encima del fondo oscuro para conservar sus colores reales)
    pantalla.blit(titulo_img, titulo_rect.topleft)
    
    # 4. El botón de jugar 
    pantalla.blit(boton_img, boton_rect.topleft)
    
    # 5. Capa de fundido a negro (solo visible durante la transición al hacer click)
    if alfa_capa > 0:
        superficie_negra.set_alpha(alfa_capa)
        pantalla.blit(superficie_negra, (0, 0))
    
    pygame.display.flip()

# --- CAMBIO DE ARCHIVO ---
import partida
partida.ejecutar_partida(pantalla, reloj, superficie_negra)