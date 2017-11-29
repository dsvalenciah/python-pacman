import time

class criatura():
    """docstring for criatura"""
    def __init__(self, pos, dir, imagen, tic, toc, tiempo_entre_mov):
        self.pos = None
        self.dir = None
        self.imagen = None
        self.tic = None
        self.toc = None
        self.tiempo_entre_mov = None


class pac_man():
    """docstring for pac_man"""
    def __init__(self):
        criatura.__init__(
            self,
            pos = (23, 13),  # posición actual (fila, columna)
            dir = 1,  # dirección hacia la que avanza
            imagen = ('pacman0','pacman1','pacman2'),  # imágenes del pacman
            tic = time.time(),  # para el cronómetro
            toc = 0,
            tiempo_entre_mov = 1.0/10,  # muevase 10 cuadros por segundo
        )
        self.invencible = False  # se comió la vitamina
        self.boca_abierta = 1  # boca abierta 0, 1, 2, 3(1)
        self.vidas = 3


class fantasma():
    """docstring for fantasma"""
    def __init__(self):
        criatura.__init__(
            self,
            pos = (0, 0),  # posición actual (fila, columna)
            dir = 1,  # dirección hacia la que avanza
            imagen = 0,  # imágenes del fantasma
            tic = time.time(),  # para el cronómetro
            toc = 0,
            tiempo_entre_mov = 1.0/8  # se mueve 8 cuadros/segundo
        )
        self.__comido = False  # se lo comio el pacman: True/False

    def dar_comido(self, comido):
        self.__comido = comido

    def obtener_comido(self):
        return self.__comido

if __name__ == '__main__':
    pacman = pac_man()
    print(pacman.pos)

    fant = fantasma()
    print(fant.obtener_comido())