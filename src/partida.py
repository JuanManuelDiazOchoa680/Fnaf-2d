import pygame
import sys
# Importamos la clase Enemigo desde tu archivo enemigos.py
from enemigos import Enemigo

def ejecutar_partida(pantalla, reloj, superficie_negra):
    ANCHO_VENTANA = pantalla.get_width()
    ALTO_VENTANA = pantalla.get_height()
    
    pygame.display.set_caption("Modo Partida")

    # --- 1. CONFIGURACIÓN DEL FONDO ---
    ANCHO_FONDO_JUEGO = 1300
    ALTO_FONDO_JUEGO = 700
    try:
        imagen_partida_original = pygame.image.load("assets/images/salon_principal.png")
    except pygame.error:
        print("Error: No se encuentra salon_principal.png")
        pygame.quit(); sys.exit()
        
    fondo_juego = pygame.transform.scale(imagen_partida_original, (ANCHO_FONDO_JUEGO, ALTO_FONDO_JUEGO))
    pos_x_fondo = (ANCHO_VENTANA - ANCHO_FONDO_JUEGO) // 2
    pos_y_fondo = (ALTO_VENTANA - ALTO_FONDO_JUEGO) // 2

    # --- 2. CONFIGURACIÓN DE ELEMENTOS ---
    ANCHO_MESA, ALTO_MESA = 500, 400
    MESA_X, MESA_Y = 400, 200
    ANCHO_MONITOR, ALTO_MONITOR = 500, 270
    MONITOR_X, MONITOR_Y = 350, 175
    ANCHO_COLGANTE, ALTO_COLGANTE = 700, 600
    COLGANTE_X = 700 
    
    # --- UBICACIÓN DE LA VENTANA ---
    VENTANA_X = COLGANTE_X + 225
    VENTANA_Y = 150  
    VENTANA_ANCHO, VENTANA_ALTO = 250, 200
    rect_ventana = pygame.Rect(VENTANA_X, VENTANA_Y, VENTANA_ANCHO, VENTANA_ALTO)
    
    # Botón de la ventana
    rect_btn_ventana = pygame.Rect(VENTANA_X + 85, VENTANA_Y - 40, 80, 30)
    
    ventana_cerrada = False
    tiempo_ventana_cerrada_con_enemigo = 0  
    
    # Variables de estado del monitor colgante
    Y_ARRIBA = -500
    Y_ABAJO = -50
    colgante_y_actual = Y_ARRIBA 
    monitor_arriba = True 
    esta_moviendose = False
    velocidad_animacion = 150 
    
    # Carga de imágenes de la oficina
    mesa_img = pygame.transform.scale(pygame.image.load("assets/images/mesa_juego_.png"), (ANCHO_MESA, ALTO_MESA))
    monitor_img = pygame.transform.scale(pygame.image.load("assets/images/pantalla_1.png"), (ANCHO_MONITOR, ALTO_MONITOR))
    colgante_img = pygame.transform.scale(pygame.image.load("assets/images/pantalla_3.png"), (ANCHO_COLGANTE, ALTO_COLGANTE))

    # --- 3. BOTONES NUMÉRICOS (EN PANTALLA 1) ---
    fuente = pygame.font.SysFont("Arial", 30)
    botones_rects = []
    for i in range(6):
        col = i % 3
        fila = i // 3
        btn_x = MONITOR_X + 135 + (col * 80)
        btn_y = MONITOR_Y + 60 + (fila * 80)
        botones_rects.append(pygame.Rect(btn_x, btn_y, 70, 60))

    # Carga de imágenes para el monitor colgante
    imgs_colgantes = []
    for i in range(1, 7):
        try:
            img = pygame.image.load(f"assets/images/img{i}.png")
            imgs_colgantes.append(pygame.transform.scale(img, (250, 200)))
        except:
            imgs_colgantes.append(None)
    
    imagen_actual = None
    camara_mirando = 0  

    # --- SISTEMA DE TIEMPO (12 PM A 6 PM) ---
    cronologia_horas = [12, 1, 2, 3, 4, 5, 6]
    tiempo_inicio = pygame.time.get_ticks()
    duracion_hora_ms = 60000  # 1 minuto real por hora
    fuente_reloj = pygame.font.SysFont("Arial", 40, bold=True)
    hora_actual = 12

    # --- SISTEMA DE BATERÍA / ENERGÍA ---
    bateria = 100.0  # Flotante para restar con precisión decimal
    ultimo_consumo_pasivo = tiempo_inicio
    ultimo_consumo_activo = tiempo_inicio
    sin_energia = False
    tiempo_fallo_energia = 0  # Guardará el momento exacto en que la batería llegó a 0
    
    fuente_bateria = pygame.font.SysFont("Arial", 28, bold=True)

    # --- CREACIÓN DEL ENEMIGO ---
    jocker_enemigo = Enemigo(nombre="Jocker", camara_inicial=5, ruta_imagen="assets/images/cara 1 white black.png")

    # --- 4. BOTÓN DE MOVIMIENTO (ROJO) ---
    ANCHO_CONTORNO = ANCHO_VENTANA // 2  
    ALTO_CONTORNO = 50
    X_CONTORNO = ANCHO_VENTANA // 2      
    Y_CONTORNO = ALTO_VENTANA - ALTO_CONTORNO  
    rect_contorno = pygame.Rect(X_CONTORNO, Y_CONTORNO, ANCHO_CONTORNO, ALTO_CONTORNO)

    # Superficies de capas oscuras
    capa_parpadeo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    capa_parpadeo.fill((0, 0, 0))
    
    capa_apagon_total = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    capa_apagon_total.fill((0, 0, 0))
    capa_apagon_total.set_alpha(235)  # Oscuridad casi absoluta, dejando ver siluetas sutiles

    # --- BUCLE PRINCIPAL ---
    alfa_capa = 255
    jugando = True
    while jugando:
        reloj.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        tiempo_actual = pygame.time.get_ticks()
        
        # --- CONTROL DEL RELOJ ---
        tiempo_transcurrido_partida = tiempo_actual - tiempo_inicio
        indice_hora = tiempo_transcurrido_partida // duracion_hora_ms
        if indice_hora >= len(cronologia_horas):
            indice_hora = len(cronologia_horas) - 1
        hora_actual = cronologia_horas[indice_hora]

        # PANTALLA DE VICTORIA (Solo si hay energía o si lograste llegar justo a tiempo)
        if hora_actual == 6 and not jocker_enemigo.jumpscare_activado:
            pantalla.fill((0, 0, 0))
            fuente_win = pygame.font.SysFont("Arial", 90, bold=True)
            texto_5pm = fuente_win.render("5 PM -> 6 PM", True, (255, 255, 255))
            texto_win = fuente_win.render("¡VICTORIA!", True, (0, 255, 0))
            pantalla.blit(texto_5pm, (ANCHO_VENTANA // 2 - 250, ALTO_VENTANA // 2 - 80))
            pantalla.blit(texto_win, (ANCHO_VENTANA // 2 - 200, ALTO_VENTANA // 2 + 30))
            pygame.display.flip()
            pygame.time.wait(5000)
            jugando = False
            break

        # --- GESTIÓN DE CONSUMO DE BATERÍA ---
        if not sin_energia:
            # 1. Consumo Pasivo: -1% cada 15 segundos (15000 ms)
            if tiempo_actual - ultimo_consumo_pasivo >= 15000:
                bateria -= 1.0
                ultimo_consumo_pasivo = tiempo_actual
            
            # 2. Consumo Activo: -2% cada 3 segundos (3000 ms) de uso de ventana O cámara abajo
            # Comprobamos si la ventana está cerrada o el monitor colgante está desplegado (no arriba)
            if ventana_cerrada or (not monitor_arriba):
                if tiempo_actual - ultimo_consumo_activa >= 3000:
                    bateria -= 2.0
                    ultimo_consumo_activa = tiempo_actual
            else:
                # Reseteamos el temporizador activo para que empiece a contar limpio al activarse de nuevo
                ultimo_consumo_activa = tiempo_actual

            # Control de quiebre de energía (Llegada a 0%)
            if bateria <= 0:
                bateria = 0.0
                sin_energia = True
                tiempo_fallo_energia = tiempo_actual  # Guardamos cuándo empezó el apagón
                ventana_cerrada = False  # La ventana se abre obligatoriamente por falta de luz
                monitor_arriba = True    # El monitor se guarda automáticamente
                camara_mirando = 0
                print("[SISTEMA] ¡BATERÍA AGOTADA! Iniciando conteo de muerte de 10 segundos...")

        # --- DETONACIÓN DE JUMPSCARE POR FALTA DE ENERGÍA (Pasados 10 segundos) ---
        if sin_energia and (tiempo_actual - tiempo_fallo_energia >= 10000):
            jocker_enemigo.jumpscare_activado = True

        # --- ACTUALIZAR INTELIGENCIA ARTIFICIAL ---
        jocker_enemigo.actualizar_ia(ventana_cerrada)
        
        # PANTALLA DE GAME OVER
        if jocker_enemigo.jumpscare_activado:
            pantalla.fill((0, 0, 0))
            pantalla.blit(jocker_enemigo.imagen_jumpscare, (0, 0))
            fuente_go = pygame.font.SysFont("Arial", 80, bold=True)
            texto_go = fuente_go.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(texto_go, (ANCHO_VENTANA // 2 - 200, ALTO_VENTANA // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit(); sys.exit()

        # --- COMPROBACIÓN DE LOS 5 SEGUNDOS DE SEGURIDAD EN LA VENTANA ---
        if jocker_enemigo.camara_actual == 0 and ventana_cerrada:
            if tiempo_ventana_cerrada_con_enemigo == 0:
                tiempo_ventana_cerrada_con_enemigo = tiempo_actual
            elif tiempo_actual - tiempo_ventana_cerrada_con_enemigo >= 5000:
                jocker_enemigo.camara_actual = 6
                jocker_enemigo.ultimo_movimiento = tiempo_actual
                tiempo_ventana_cerrada_con_enemigo = 0
        else:
            tiempo_ventana_cerrada_con_enemigo = 0

        # Lógica de movimiento del monitor colgante (BLOQUEADO SI NO HAY ENERGÍA)
        if not sin_energia:
            if rect_contorno.collidepoint(mouse_pos) and not esta_moviendose:
                esta_moviendose = True
                monitor_arriba = not monitor_arriba
            if not rect_contorno.collidepoint(mouse_pos):
                esta_moviendose = False

        # Animación del monitor
        pos_objetivo = Y_ABAJO if not monitor_arriba else Y_ARRIBA
        if colgante_y_actual < pos_objetivo:
            colgante_y_actual += velocidad_animacion
            if colgante_y_actual > pos_objetivo: colgante_y_actual = pos_objetivo
        elif colgante_y_actual > pos_objetivo:
            colgante_y_actual -= velocidad_animacion
            if colgante_y_actual < pos_objetivo: colgante_y_actual = pos_objetivo
            
        if monitor_arriba:
            camara_mirando = 0
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False; pygame.quit(); sys.exit()
                
            # INTERACCIONES MOUSE (BLOQUEADAS SI NO HAY ENERGÍA)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not sin_energia:
                for idx, rect in enumerate(botones_rects):
                    if rect.collidepoint(evento.pos):
                        imagen_actual = imgs_colgantes[idx]
                        camara_mirando = idx + 1 

                if rect_btn_ventana.collidepoint(evento.pos):
                    ventana_cerrada = not ventana_cerrada
                    if ventana_cerrada:
                        if jocker_enemigo.camara_actual != 0:
                            jocker_enemigo.multiplicador_velocidad = 2.0
                    else:
                        jocker_enemigo.multiplicador_velocidad = 1.0
                        if jocker_enemigo.camara_actual == 0:
                            jocker_enemigo.jumpscare_activado = True

        # --- C. ORDEN DE CAPAS ---
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo_juego, (pos_x_fondo, pos_y_fondo))
        
        # La Ventana y el Enemigo
        if ventana_cerrada:
            pygame.draw.rect(pantalla, (35, 35, 35), rect_ventana)
            pygame.draw.line(pantalla, (15, 15, 15), (VENTANA_X, VENTANA_Y + 100), (VENTANA_X + VENTANA_ANCHO, VENTANA_Y + 100), 6)
        else:
            pygame.draw.rect(pantalla, (10, 15, 25), rect_ventana)
            if jocker_enemigo.camara_actual == 0:
                pantalla.blit(jocker_enemigo.imagen, (VENTANA_X + 65, VENTANA_Y + 50))

        # Botón de la ventana
        color_boton = (0, 160, 255) if ventana_cerrada else (0, 255, 120)
        pygame.draw.rect(pantalla, color_boton, rect_btn_ventana)
        texto_btn = pygame.font.SysFont("Arial", 16, bold=True).render("VENT", True, (0, 0, 0))
        pantalla.blit(texto_btn, (rect_btn_ventana.x + 18, rect_btn_ventana.y + 5))

        # Mesa y Monitor estático
        pantalla.blit(mesa_img, (MESA_X, MESA_Y))
        pantalla.blit(monitor_img, (MONITOR_X, MONITOR_Y))
        
        # Pantalla colgante
        pantalla.blit(colgante_img, (COLGANTE_X, colgante_y_actual))
        
        # Transmisión de cámaras
        if imagen_actual:
            pantalla.blit(imagen_actual, (COLGANTE_X + 225, colgante_y_actual + 225))
            if not monitor_arriba:
                jocker_enemigo.dibujar_en_camara(pantalla, camara_mirando, COLGANTE_X, colgante_y_actual)
        
        # Botones numéricos de cámaras
        for i, rect in enumerate(botones_rects):
            pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
            texto = fuente.render(str(i+1), True, (255, 255, 255))
            pantalla.blit(texto, (rect.x + 25, rect.y + 15))
        
        # Sensor inferior
        pygame.draw.rect(pantalla, (255, 0, 0), rect_contorno, 3)
        
        # --- RENDEREZADO DE LA INTERFAZ DE TIEMPO Y BATERÍA ---
        # 1. Reloj (Arriba Izquierda)
        texto_hora = f"{hora_actual} PM"
        render_reloj = fuente_reloj.render(texto_hora, True, (0, 0, 0))
        pantalla.blit(render_reloj, (30, 30))
        
        # 2. Batería (Izquierda Central)
        # Cambia a color rojo si queda menos de 20%
        color_bateria = (0, 255, 0) if bateria > 20 else (255, 50, 50)
        texto_bat = f"BATERÍA: {int(bateria)}%"
        render_bateria = fuente_bateria.render(texto_bat, True, color_bateria)
        # Posición central izquierda (x=30, y=mitad de la pantalla)
        pantalla.blit(render_bateria, (30, ALTO_VENTANA // 2))

        # --- D. CAPAS DE OSCURIDAD ---
        # Si se acabó la batería, aplicamos el apagón total
        if sin_energia:
            pantalla.blit(capa_apagon_total, (0, 0))
        else:
            # Si hay energía, aplica el parpadeo normal del enemigo (segundo 10)
            alpha_parpadeo = jocker_enemigo.obtener_opacidad_parpadeo()
            if alpha_parpadeo > 0:
                capa_parpadeo.set_alpha(alpha_parpadeo)
                pantalla.blit(capa_parpadeo, (0, 0))
        
        # Fade inicial
        if alfa_capa > 0:
            alfa_capa -= 5
            superficie_negra.set_alpha(alfa_capa)
            pantalla.blit(superficie_negra, (0, 0))

        pygame.display.flip()