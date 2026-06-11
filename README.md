# Cursed School
# (Python & Pygame)

Este proyecto es un videojuego de terror y supervivencia en 2D/3D desarrollado desde cero en **Python** utilizando la biblioteca **Pygame**. Inspirado en las mecánicas clásicas de gestión de recursos y tensión, el objetivo principal es sobrevivir a una jornada crítica en una oficina vigilada mientras eres acechado por una Inteligencia Artificial implacable.

---

## 🎮 Mecánicas Principales del Juego

El juego sumerge al jugador en una cabina de control u oficina principal. La partida tiene una duración fija de **6 minutos reales**, donde cada minuto equivale a una hora dentro del universo del juego. La supervivencia se basa en la gestión de tres elementos dinámicos:

### 1. Sistema Cronológico (El Reloj)
* **Horario de la Partida:** La jornada laboral inicia estrictamente a las **12 PM** y el objetivo de victoria absoluta es alcanzar las **6 PM**.
* **Escala de Tiempo:** 1 hora del juego = 60 segundos (1 minuto) en la vida real.
* El reloj se encuentra visible en la **esquina superior izquierda**, renderizado en color negro para contraste directo con la iluminación de la oficina.

### 2. Gestión de Energía (Batería Limitada)
La oficina cuenta con una planta eléctrica limitada que drena recursos constantemente. El indicador se encuentra en la **zona central izquierda** con un color verde brillante, el cual cambia a un rojo de alerta si cae por debajo del 20%.

* **Consumo Pasivo:** El juego consume automáticamente **1% de batería cada 15 segundos** por el simple hecho de mantener las luces encendidas.
* **Consumo Activo (Uso de Sistemas):** Mantener la ventana cerrada o tener el monitor de cámaras desplegado genera una carga masiva en los circuitos, drenando un **2% extra cada 3 segundos**.
* **Apagón Total (0% Batería):** Si la energía se agota por completo, el juego entra en modo crítico:
  1. Se aplica una capa negra pesada con alta opacidad sobre toda la oficina (Apagón).
  2. Los sistemas mecánicos fallan: la ventana se abre a la fuerza y la pantalla colgante se bloquea arriba.
  3. Tras **10 segundos exactos en la oscuridad**, el enemigo atacará directamente al jugador provocando un Game Over instantáneo.

### 3. La Pantalla Colgante y Sistema de Cámaras
* **Animación e Interacción:** En la parte inferior de la interfaz existe un sensor de movimiento (recuadro rojo). Al pasar el cursor por esta zona, una gran pantalla colgante se desliza verticalmente desde el techo con una transición fluida.
* **Jerarquía de Capas (Superposición):** Cuando la pantalla se despliega, se posiciona en la capa superior de renderizado, cubriendo físicamente la ventana y cualquier elemento que se encuentre detrás de ella.
* **Monitoreo:** El monitor principal de la mesa cuenta con 6 botones interactivos para alternar entre las cámaras de seguridad (`img1.png` a `img6.png`), permitiendo rastrear la posición en tiempo real del enemigo.

### 4. Defensa de la Ventana y Comportamiento de la IA
* El enemigo principal (**Jocker**) avanza de forma aleatoria a través del mapa de cámaras guiado por un temporizador interno (`cooldown_movimiento`).
* **La Ventana:** Está alineada horizontalmente detrás de la pantalla colgante. Si el enemigo llega a la **Cámara 0**, significa que está físicamente asomado en tu ventana listo para atacar.
* **Mecánica de Cierre:** El jugador debe presionar el botón `VENT` para sellar la ventana. 
  * Si el enemigo está en la ventana y esta se cierra, el jugador debe resistir **5 segundos continuos** para ahuyentarlo con éxito (lo que lo obligará a huir a la Cámara 6).
  * **Castigo por Pánico:** Si el jugador cierra la ventana cuando el enemigo NO está ahí, la IA se percata del sabotaje y **duplica su velocidad de movimiento**, penalizando fuertemente el gasto innecesario de energía.
  * Si el enemigo pasa demasiado tiempo en la ventana abierta o se apaga la luz, se ejecutará una animación de `Jumpscare` a pantalla completa resultando en **GAME OVER**.

---

## 📂 Arquitectura del Código

El proyecto está modularizado para mantener un entorno de desarrollo limpio y escalable:

* **`menu.py`**: El punto de entrada del juego. Gestiona la interfaz del menú principal, la carga de recursos estáticos, la estética del título y una transición de pantalla negra suave mediante canales alfa al presionar "Jugar".
* **`partida.py`**: El núcleo de la lógica del juego. Controla el bucle principal (`While`), el orden de dibujado por capas en la superficie de Pygame, el procesamiento de eventos del mouse, el renderizado de las fuentes (reloj y batería), y las colisiones de botones.
* **`enemigos.py`**: Contiene la clase estructurada `Enemigo`. Define las propiedades de la IA, el cálculo matemático de parpadeo de pantalla (onda sinusoidal a partir del segundo 10 en ventana) y los métodos para dibujar al personaje en los cuadrantes de las cámaras.

muestra de juego por ahora:
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/60858ffe-0936-4e6b-983f-8ae35e2e1c2c" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/60e37c82-97d7-4f84-be29-1f0969d88676" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/be08f622-1da6-4c31-898b-e54652b4af4b" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/2afc0292-b693-4fb0-be29-50d901239029" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/587abc4c-5522-4c43-a458-739f550bcf86" />





