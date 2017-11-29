"""
 * P A C - M A N
 * Por:
 * Diego Andrés Alvarez Marín (daalvarez@unal.edu.co)
 * Ver el pacman original en:
 * http://www.thepcmanwebsite.com/media/pacman_flash/
 *
 * Los sprites se tomaron de:
 * https://www.spriters-resource.com/arcade/pacman/sheet/52631/
 *
 * Y se pueden recortar o con PAINT o con
 * https://jmsliu.com/products/sprite-sheet-decomposer/
 *
 * INSTRUCCIONES:
 * FLECHAS mueven el pac-man
 * ESPACIO pausa
 * ESCAPE  se sale del juego
"""
# %% se cargan las librerías
import time
import os
import sys
import random
import pygame

# %% se definen las constantes
COLOR_NEGRO    = (  0,   0, 0  )
COLOR_BLANCO   = (255, 255, 255)
COLOR_AMARILLO = (255, 255,  51)

# datos básicos del tablero:
ESC = 2                           # escala de multiplicacion de los sprites
XTAB, YTAB = 30, 50               # posición superior izquierda del tablero
ANCHOFIL, ANCHOCOL = 8*ESC, 8*ESC # dimensiones de una casilla (tile)
NFIL, NCOL         = 31, 28       # filas, columnas

# se definen las constantes de los movimientos
(QUIETO, DERECHA, ARRIBA, IZQUIERDA, ABAJO) = range(5)

# %% se definen algunas variables globales
marcador = 0

class Criatura():
    """definición de la clase criatura"""
    def __init__(self, pos, dir, imagen, tic, toc, tiempo_entre_mov):
        self.pos = pos
        self.dir = dir
        self.imagen = imagen
        self.tic = tic
        self.toc = toc
        self.tiempo_entre_mov = tiempo_entre_mov


class PacMan():
    """definición de la clase PacMan"""
    def __init__(self):
        Criatura.__init__(
            self,
            pos = (23, 13),  # posición actual (fila, columna)
            dir = QUIETO,  # dirección hacia la que avanza
            imagen = ('pacman0','pacman1','pacman2'),  # imágenes del pacman
            tic = time.time(),  # para el cronómetro
            toc = 0,
            tiempo_entre_mov = 1.0/10,  # muevase 10 cuadros por segundo
        )
        self.invencible = False  # se comió la vitamina
        self.boca_abierta = 1  # boca abierta 0, 1, 2, 3(1)
        self.vidas = 3


class Fantasma():
    """definición de la clase Fantasma"""
    def __init__(self):
        Criatura.__init__(
            self,
            pos = (0, 0),  # posición actual (fila, columna)
            dir = ARRIBA,  # dirección hacia la que avanza
            imagen = 0,  # imágenes del fantasma
            tic = time.time(),  # para el cronómetro
            toc = 0,
            tiempo_entre_mov = 1.0/8  # se mueve 8 cuadros/segundo
        )
        self.comido = False  # se lo comio el pacman: True/False

class Vitamina():
    """docstring for Vitamina"""
    def __init__(self):
        self.__pos = ((3,1), (3,26), (23,1), (23,26)) # posición (fila, columna)
        self.comida = [False, False, False, False]  # se comieron la vitamina
        self.tiempo_comido = [0, 0, 0, 0]  # tiempo en el que fue comida
        self.comido_una_vez = [False, False, False, False]  # fue comido
        # una vez
        self.imagen = ('pepa_peq','pepa_med','pepa_gra')  # imágenes
        self.tamano = 2  # 0=pequeña, 1=mediana, 2=grande

    def dar_pos(self, pos, indice):
        self.__pos[indice] = pos

    def obtener_pos(self):
        return self.__pos

# %% crear los fantasmas
blinky = Fantasma()
blinky.pos = (14, 11)
blinky.imagen = 'blinky'

pinky = Fantasma()
pinky.pos = (14, 13)
pinky.imagen = 'pinky'

inky = Fantasma()
inky.pos = (14, 15)
inky.imagen = 'inky'

clyde = Fantasma()
clyde.pos = (13, 13)
clyde.imagen = 'clyde'

# %% crear vitamina
vitamina = Vitamina()

# %% crear pacman
pacman = PacMan()

# %% se define el tablero de juego
mapa = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o#  #.#   #.##.#   #.#  #o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###MM### ##.#     ",
    "######.## #      # ##.######",
    "#     .   #      #   .     #", # En *ESTA* línea mucho cuidado con el # al
    "######.## #      # ##.######", # principio y al final. Toca ponerlos para
    "     #.## ######## ##.#     ", # cerrar el túnel
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##.......  .......##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# %%
def cargar_archivo_de_sonido(archivo):
    # Se crea la ruta del nombre del archivo a cargar. La función
    # os.path.join() concatena o produce el nombre del archivo de modo que se
    # pueda correr bajo cualquier sistema operativo.
    nombre_archivo = os.path.join('sonidos', archivo + '.wav')
    try:
        return pygame.mixer.Sound(nombre_archivo)
    except pygame.error:
        texto_error = 'No se pudo cargar el sonido {0}.\n{1}'.\
            format(nombre_archivo, pygame.get_error())
        pygame.quit()
        raise SystemExit(texto_error)

# %%
def cargar_archivo_de_imagen(archivo):
    # Se crea la ruta del nombre del archivo a cargar. La función
    # os.path.join() concatena o produce el nombre del archivo de modo que se
    # pueda correr bajo cualquier sistema operativo.
    nombre_archivo = os.path.join('imagenes', archivo + '.png')
    try:
        return pygame.image.load(nombre_archivo).convert()
    except pygame.error:
        texto_error = 'No se pudo cargar la imagen {0}.\n{1}'.\
            format(nombre_archivo, pygame.get_error())
        pygame.quit()
        raise SystemExit(texto_error)

# %%
def vitaminas_animar():
    # se selecciona el gráfico de la vitamina a utilizar
    vitamina.tamano += 1
    if vitamina.tamano == 4:
        vitamina.tamano = 0

    if   vitamina.tamano == 0: num_imagen_vitamina = 0
    elif vitamina.tamano == 1: num_imagen_vitamina = 1
    elif vitamina.tamano == 2: num_imagen_vitamina = 2
    elif vitamina.tamano == 3: num_imagen_vitamina = 1

    imagen_vitamina = vitamina.imagen[num_imagen_vitamina]

    # graficamos c/u de las vitaminas siempre y cuando no hayan sido comidas
    for i in range(4):
        if not vitamina.comida[i]:
            ventana.blit(imagen_ficha[imagen_vitamina],
                           (XTAB + vitamina.obtener_pos()[i][1]*ANCHOCOL,
                            YTAB + vitamina.obtener_pos()[i][0]*ANCHOFIL))

# %%
def fantasma_animar(F, pos_anterior):
    fil, col = pos_anterior

    # se pone la loseta vacía en la nueva posición; ese "-3*ESC" es porque el
    # fantasma tiene un tamaño de 14x14 y la loseta uno de 8x8
    ventana.blit(vacio_fantasma, (XTAB + col*ANCHOCOL - 3*ESC,
                                  YTAB + fil*ANCHOFIL - 3*ESC))

    # ya con el espacio en blanco, se pone el punto .o o el muro M
    if mapa[fil][col] == 'M':
        ventana.blit(imagen_ficha['muro_fan'], (XTAB + col*ANCHOCOL,
                                                YTAB + fil*ANCHOFIL))
    elif mapa[fil][col] == '.':
        ventana.blit(imagen_ficha['pepa_peq'], (XTAB + col*ANCHOCOL,
                                                YTAB + fil*ANCHOFIL))
    elif mapa[fil][col] == 'o':
        ventana.blit(imagen_ficha['pepa_gra'], (XTAB + col*ANCHOCOL,
                                                YTAB + fil*ANCHOFIL))
    elif mapa[fil][col] == ' ':
        ventana.blit(imagen_ficha['vacio'],    (XTAB + col*ANCHOCOL,
                                                YTAB + fil*ANCHOFIL))

    # se pone el fantasma en la nueva posición; ese "-3*ESC" es porque el
    # fantasma tiene un tamaño de 14x14 y la loseta uno de 8x8
    fil_sgte, col_sgte = F.pos
    ventana.blit(imagen_ficha[F.imagen], (XTAB + col_sgte*ANCHOCOL - 3*ESC,
                                             YTAB + fil_sgte*ANCHOFIL - 3*ESC))

# %%
def fantama_generar_dir_aleatoria(F):
    # se encuentran las posibles direcc. en las que el fantasma se puede mover
    pos_dir = []
    if puede_moverse_fantasma(F, DERECHA):   pos_dir.append(DERECHA)
    if puede_moverse_fantasma(F, ARRIBA):    pos_dir.append(ARRIBA)
    if puede_moverse_fantasma(F, IZQUIERDA): pos_dir.append(IZQUIERDA)
    if puede_moverse_fantasma(F, ABAJO):     pos_dir.append(ABAJO)

    if len(pos_dir) == 1: # si solo hay una posible dirección de movimiento
        return pos_dir[0]
    else:
        # si el fantasma se puede mover en varias direcciones, se encuentra la
        # dirección contraria al movimiento actual y se descarta
        if   F.dir == DERECHA:   dir_contraria = IZQUIERDA
        elif F.dir == ARRIBA:    dir_contraria = ABAJO
        elif F.dir == IZQUIERDA: dir_contraria = DERECHA
        elif F.dir == ABAJO:     dir_contraria = ARRIBA

        # remueva la dirección contraria porque no se puede devolver
        if puede_moverse_fantasma(F, dir_contraria):
            pos_dir.remove(dir_contraria)

        # se selecciona la dirección aleatoria y se retorna
        return pos_dir[int(len(pos_dir)*random.random())]

# %%
def fantasma_mover(F):
    # se guardan las posiciones anteriores
    fil_anterior, col_anterior = fil_sgte, col_sgte = F.pos

    F.toc = time.time()
    tiempo = F.toc - F.tic
    if tiempo > F.tiempo_entre_mov:
        # se genera la dirección de movimiento del fantasma
        F.dir = fantama_generar_dir_aleatoria(F)

        # actualizar las posiciones siguientes
        if   (F.dir == DERECHA)   and (col_anterior < NCOL-1): col_sgte += 1
        elif (F.dir == ARRIBA)    and (fil_anterior > 0):      fil_sgte -= 1
        elif (F.dir == IZQUIERDA) and (col_anterior > 0):      col_sgte -= 1
        elif (F.dir == ABAJO)     and (fil_anterior < NFIL-1): fil_sgte += 1

        # se actualiza la posición del fantasma
        F.pos = (fil_sgte, col_sgte)

        # se actualiza el reloj interno del fantasma
        F.tic = time.time()

    # se mueve el fantasma de la posicion anterior a la actual
    fantasma_animar(F, (fil_anterior, col_anterior))

# %%
def pacman_animar(pos_anterior):
    # se pone la loseta vacía en la nueva posición; ese "-3*ESC" es porque el
    # pacman tiene un tamaño de 14x14 y la loseta uno de 8x8
    fil, col = pos_anterior
    ventana.blit(vacio_pacman, (XTAB + col*ANCHOCOL - 3*ESC,
                                YTAB + fil*ANCHOFIL - 3*ESC))

    # se encuentra la figura a graficar
    pacman.boca_abierta += 1
    if pacman.boca_abierta == 4:
        pacman.boca_abierta = 0

    if   pacman.boca_abierta == 0: num_imagen_pacman = 0
    elif pacman.boca_abierta == 1: num_imagen_pacman = 1
    elif pacman.boca_abierta == 2: num_imagen_pacman = 2
    elif pacman.boca_abierta == 3: num_imagen_pacman = 1

    imagen_pacman = pacman.imagen[num_imagen_pacman]

    # se grafica el pacman en la nueva posición; ese "-3*ESC" es porque el
    # pacman tiene un tamaño de 14x14 y la loseta uno de 8x8
    fil_sgte, col_sgte = pacman.pos
    ventana.blit(imagen_ficha[imagen_pacman], (XTAB + col_sgte*ANCHOCOL - 3*ESC,
                                               YTAB + fil_sgte*ANCHOFIL - 3*ESC))

# %%
def pacman_mover(dir):
    global marcador

    # se guardan las posiciones anteriores
    fil_anterior, col_anterior = fil_sgte, col_sgte = pacman.pos

    pacman.toc = time.time()
    tiempo = pacman.toc - pacman.tic
    if tiempo > pacman.tiempo_entre_mov:
        # actualizar las posiciones siguientes
        if   (dir == DERECHA)   and (col_anterior < NCOL-1): col_sgte += 1
        elif (dir == ARRIBA)    and (fil_anterior > 0):      fil_sgte -= 1
        elif (dir == IZQUIERDA) and (col_anterior > 0):      col_sgte -= 1
        elif (dir == ABAJO)     and (fil_anterior < NFIL-1): fil_sgte += 1

        if mapa[fil_sgte][col_sgte] in ' .o': # vacío, punto, vitamina
            if mapa[fil_sgte][col_sgte] == '.':   # se comió un puntico
                marcador += 10
                mapa[fil_sgte][col_sgte] = ' '
                # Si ya está sonando un efecto de sonido, no mandar otro porque
                # se sobrepone y suena mal:
                if not Canal_Efectos_Sonido.get_busy():
                    Canal_Efectos_Sonido.play(sonido['eating_short'])
            elif mapa[fil_sgte][col_sgte] == 'o': # se comió la vitamina
                marcador += 50
                mapa[fil_sgte][col_sgte] = ' '
                for i in range(4):
                    if vitamina.obtener_pos()[i] == (fil_sgte,col_sgte):
                        vitamina.comida[i] = True
                        vitamina.comido_una_vez[i] = True
                        vitamina.tiempo_comido[i] = time.time()

            # se actualiza la posición y dirección del fantasma
            pacman.pos = (fil_sgte, col_sgte)
            pacman.dir = dir

            # se actualiza el reloj interno del pacman
            pacman.tic = time.time()

    # se mueve el pacman de la posicion anterior a la actual
    pacman_animar((fil_anterior, col_anterior))

    # se actualiza el puntaje
    # Texto, AliasedText=True/False, ForegroundColor, BackgroundColor
    ventana.blit(fuente['whimsy'].render('Score:', True,
                                       COLOR_BLANCO, COLOR_NEGRO), (10, 10))
    ventana.blit(fuente['whimsy'].render(str(marcador) + '  ', True,
                                       COLOR_AMARILLO, COLOR_NEGRO), (100, 10))

# %%
def puede_moverse_pacman(dir):
    fil, col = pacman.pos
    # actualizar las posiciones
    if   (dir == DERECHA)   and (col < NCOL-1): col += 1
    elif (dir == ARRIBA)    and (fil > 0):      fil -= 1
    elif (dir == IZQUIERDA) and (col > 0):      col -= 1
    elif (dir == ABAJO)     and (fil < NFIL-1): fil += 1

    return mapa[fil][col] in ' .o' # vacío, punto, vitamina

# %%
def puede_moverse_fantasma(F, dir):
    fil, col = F.pos
    # actualizar las posiciones
    if   (dir == DERECHA)   and (col < NCOL-1): col += 1
    elif (dir == ARRIBA)    and (fil > 0):      fil -= 1
    elif (dir == IZQUIERDA) and (col > 0):      col -= 1
    elif (dir == ABAJO)     and (fil < NFIL-1): fil += 1

    return mapa[fil][col] in 'M .o' # muro fantasma, vacío, punto, vitamina

# %%
def vitamina_comida():
    for i, x in enumerate(vitamina.comido_una_vez):
        if x and time.time() - vitamina.tiempo_comido[i] >= 5:
            print("Ya pasaron 5 segundos")
            vitamina.comido_una_vez[i] = False

# %%###### ########## ######## PROGRAMA PRINCIPAL ######## ########## #########
# %% Se convierte el laberinto a una lista
for i in range(NFIL):
    mapa[i] = list(mapa[i])

# lista de fantasmas
fant = [ blinky, pinky, inky, clyde ]

# %% Se inicializa el modo PYGAME
pygame.init()
reloj = pygame.time.Clock()                   # reloj
ventana = pygame.display.set_mode((600, 600)) # ventana de juego
pygame.display.set_caption('P A C - M A N')   # titulo a la ventana

# se crean dos canales de sonido para tocar dos pistas de audio simultaneamente
Canal_Musica_Fondo   = pygame.mixer.Channel(0)
Canal_Efectos_Sonido = pygame.mixer.Channel(1)

# %% Se configura la fuente
fuente = {}
fuente['whimsy'] = pygame.font.Font(os.path.join('fuentes','whimsytt.ttf'), 25)

# %% Se leen los sonidos
archivos = [
    'opening_song',
    'eating_short',
    'siren'
    ]

sonido = {}     # diccionario vacío
for archivo in archivos:
    sonido[archivo] = cargar_archivo_de_sonido(archivo)

# %% Se leen las imágenes del disco y se almacenan en un diccionario
# Nombres de los archivos que contienen las fichas (.png)
archivos = [
    'laberinto',
    'blinky',
    'pinky',
    'inky',
    'clyde',
    'muro_fan',   # muro de la cueva de los fantasmas
    'pepa_peq',   # pasillo con el pepa pequeña
    'pepa_med',   # pasillo con el pepa pequeña
    'pepa_gra',   # pasillo con la pepa grande (vitamina)
    'vacio',      # pasillo sin el puntico
    'pacman0', 'pacman1', 'pacman2'
]

imagen_ficha = {}      # diccionario vacío
for archivo in archivos:
    imagen_ficha[archivo] = cargar_archivo_de_imagen(archivo)
    imagen_ficha[archivo] = pygame.transform.scale2x(imagen_ficha[archivo])

vacio_fantasma = imagen_ficha['blinky'].copy();  vacio_fantasma.fill(COLOR_NEGRO)
vacio_pacman   = imagen_ficha['pacman0'].copy(); vacio_pacman.fill(COLOR_NEGRO)
imagen_ficha['pepa_gra'].set_colorkey(COLOR_NEGRO)
imagen_ficha['blinky'].set_colorkey(COLOR_NEGRO)
imagen_ficha['pinky'].set_colorkey(COLOR_NEGRO)
imagen_ficha['inky'].set_colorkey(COLOR_NEGRO)
imagen_ficha['clyde'].set_colorkey(COLOR_NEGRO)

# %% Se le coloca el ícono a la ventana
icono = imagen_ficha['pacman1'].copy()
icono.set_colorkey(COLOR_NEGRO)      # Asuma que el color negro es transparente
pygame.display.set_icon(icono)

# %% Se borra la pantalla y se pinta toda de color negro
ventana.fill(COLOR_NEGRO)

# %% se imprime la imagen del laberinto
ventana.blit(imagen_ficha['laberinto'], (XTAB, YTAB))

salirse_del_juego = False  # ¿salirse del juego?
proxima_dir = QUIETO       # quédese quieto al principio del juego

# %% se hace la introducción
# se toca la canción de inicio
haciendo_la_introduccion = True
duracion_intro = sonido['opening_song'].get_length()
inicio_intro_tic = time.time()
Canal_Musica_Fondo.play(sonido['opening_song'])
# Bloqueamos el muro "M" de la cueva de los fantasmas
mapa[12][13] = mapa[12][14] = '#'

# %% bucle principal
while (pacman.vidas > 0) and (not salirse_del_juego):
    # cambiar imagenes dependiendo de si vitamina es comida o no
    vitamina_comida()

    # se está ejecutando la introducción?
    if haciendo_la_introduccion:
        if (time.time() - inicio_intro_tic) > duracion_intro:
            # se restaura el muro de la cueva de los fantasmas
            mapa[12][13] = mapa[12][14] = 'M'

            # se toca la sirena como música de fondo indefinidamente (-1)
            Canal_Musica_Fondo.play(sonido['siren'], -1)
            haciendo_la_introduccion = False

    # mover el pacman: si se puede mover en la proxima dirección hágalo, de lo
    # contrario siga la inercia
    if(puede_moverse_pacman(proxima_dir)):
        pacman_mover(proxima_dir)
    else:
        pacman_mover(pacman.dir)

    # mover los fantasmas
    for i in range(4):
        fantasma_mover(fant[i])

    # se hacen titilar las vitaminas:
    vitaminas_animar()

    # leer el teclado
    for event in pygame.event.get():
        # si se presiona con el mouse la X de la ventana:
        if event.type == pygame.QUIT:
            salirse_del_juego = True

        # si se presiona una tecla:
        if (event.type == pygame.KEYDOWN) and (not haciendo_la_introduccion):
            if event.key == pygame.K_ESCAPE:  # ESCAPE: se sale del juego
                salirse_del_juego = True
            if event.key == pygame.K_UP:      # FLECHA_ARRIBA
                proxima_dir = ARRIBA
            if event.key == pygame.K_DOWN:    # FLECHA_ABAJO
                proxima_dir = ABAJO
            if event.key == pygame.K_LEFT:    # FLECHA_IZQUIERDA
                proxima_dir = IZQUIERDA
            if event.key == pygame.K_RIGHT:   # FLECHA_DERECHA
                proxima_dir = DERECHA

            if event.key == pygame.K_SPACE:   # HACER UNA PAUSA
                pass

    # Actualizar la pantalla
    pygame.display.update()

    # número de cuadros/segundo en la animación
    tiempo_entre_ciclos = reloj.tick_busy_loop(16)

# %% BYE, BYE!
pygame.quit()    # finalice el modo PYGAME
sys.exit()
