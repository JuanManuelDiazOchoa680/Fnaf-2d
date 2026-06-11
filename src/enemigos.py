import pygame
import random

class Enemigo:
    def __init__(self, nombre, camara_inicial, ruta_imagen):
        self.nombre = nombre
        self.camara_actual = camara_inicial  
        
        try:
            imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
            self.imagen = pygame.transform.scale(imagen_original, (120, 100))
            # Imagen gigante para el jumpscare de Game Over
            self.imagen_jumpscare = pygame.transform.scale(imagen_original, (1300, 700))
        except pygame.error:
            print(f"¡Error! No se pudo cargar la imagen del enemigo.")
            self.imagen = pygame.Surface((100, 100))
            self.imagen.fill((255, 0, 0))
            self.imagen_jumpscare = pygame.Surface((1300, 700))
            self.imagen_jumpscare.fill((150, 0, 0))
            
        self.cooldown_movimiento = 6000  
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.multiplicador_velocidad = 1.0  # Para castigar si cierran la ventana sin necesidad
        
        # Variables para la mecánica de la ventana (Posición 0)
        self.tiempo_llegada_ventana = 0
        self.tiempo_limite_ventana = 15000 # 15 segundos por defecto (en milisegundos)
        self.jumpscare_activado = False

        self.caminos = {
            5: [4, 3],
            4: [2, 5],
            3: [1, 5],
            2: [0],     # El pasillo/cámara 2 conecta a la Ventana (0)
            1: [0],     # El pasillo/cámara 1 conecta a la Ventana (0)
            6: [5]      # Cámara lejana de reinicio
        }

    def actualizar_ia(self, ventana_cerrada):
        """Maneja el movimiento y los tiempos de ataque en la ventana."""
        tiempo_actual = pygame.time.get_ticks()
        
        # --- LÓGICA CUANDO ESTÁ EN UNA CÁMARA NORMAL ---
        if self.camara_actual != 0:
            # Si el jugador cerró la ventana en falso, va el doble de rápido (cooldown reducido a la mitad)
            cooldown_real = self.cooldown_movimiento / self.multiplicador_velocidad
            
            if tiempo_actual - self.ultimo_movimiento > cooldown_real:
                self.ultimo_movimiento = tiempo_actual
                
                if random.random() < 0.65:
                    if self.camara_actual in self.caminos:
                        opciones = self.caminos[self.camara_actual]
                        nueva_pos = random.choice(opciones)
                        
                        # Si decide entrar a la ventana (0)
                        if nueva_pos == 0:
                            self.camara_actual = 0
                            self.tiempo_llegada_ventana = tiempo_actual
                            # Regla: Si la ventana ya estaba cerrada, se queda 30 seg. Si estaba abierta, 15 seg.
                            self.tiempo_limite_ventana = 30000 if ventana_cerrada else 15000
                            print(f"[ALERTA] {self.nombre} HA LLEGADO A LA VENTANA. Tiempo límite: {self.tiempo_limite_ventana/1000}s")
                        else:
                            self.camara_actual = nueva_pos
                        print(f"[SISTEMA IA] {self.nombre} se movió a la Cámara {self.camara_actual}")

        # --- LÓGICA CUANDO YA ESTÁ EN LA VENTANA ---
        else:
            tiempo_transcurrido = tiempo_actual - self.tiempo_llegada_ventana
            
            # Si se acaba el tiempo en la ventana -> GAME OVER
            if tiempo_transcurrido >= self.tiempo_limite_ventana:
                self.jumpscare_activado = True

    def obtener_opacidad_parpadeo(self):
        """Calcula el efecto de parpadeo progresivo a partir del segundo 10."""
        if self.camara_actual != 0:
            return 0 # Sin opacidad oscura si no está en la ventana
            
        tiempo_transcurrido = pygame.time.get_ticks() - self.tiempo_llegada_ventana
        
        # El parpadeo inicia a los 10 segundos (10000 ms) independientemente del límite total
        if tiempo_transcurrido > 10000:
            # Oscurece y aclara usando una función de onda basada en el tiempo actual
            import math
            frecuencia = (tiempo_transcurrido - 10000) / 1000  # Se vuelve más rápido con el tiempo
            oscilacion = (math.sin(pygame.time.get_ticks() * 0.01 * frecuencia) + 1) / 2
            return int(oscilacion * 200) # Retorna un valor alpha para una capa negra (0 a 200)
        return 0

    def dibujar_en_camara(self, pantalla, camara_activa_jugador, posicion_x_colgante, posicion_y_colgante):
        """Muestra al enemigo en los monitores."""
        if self.camara_actual == camara_activa_jugador and self.camara_actual != 0:
            x_enemigo = posicion_x_colgante + 225 + 65 
            y_enemigo = posicion_y_colgante + 225 + 50
            pantalla.blit(self.imagen, (x_enemigo, y_enemigo))
