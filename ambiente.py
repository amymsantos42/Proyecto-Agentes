
import random 
from robot import *

class casilla():
    def __init__(self):
        self.casilla = []
    def es_vacia(self):
        return len(self.casilla) == 0
    def annadir(self,name):
        self.casilla.append(name)
    def remover(self,name):
        self.casilla.remove(name)
    def contiene(self,name):
        return name in self.casilla

    def __str__(self):
        if self.es_vacia() :
            return "_  "
        elif len(self.casilla) == 1:
            return self.casilla[0] + "  "
        elif len(self.casilla) == 2:
            return self.casilla[0] +"/" + self.casilla[1] + " "
        return self.casilla[0] +"/" + self.casilla[1] + "/" + self.casilla[2] + " "


        

class ambiente():
    def __init__(self,cant_ninos,n,m,porc_suciedad,porc_obstaculo):
        self.cant_ninos = cant_ninos
        self.ninnosSueltos = cant_ninos
        self.habitacion = []
        self.corral = []
        self.ninnos = []
        self.n = n
        self.m = m
        self.porc_suciedad = porc_suciedad
        self.suciedadActual = int(self.n * self.m * self.porc_suciedad / 100) 
        self.porc_obstaculo = porc_obstaculo
        self.desplazamiento_x = [-1 ,0,1,0]
        self.desplazamiento_y = [0,1,0,-1]
        self.generarAmbiente()

    def generarSuciedad(self):
        #cant_suciedad = int(self.n * self.m * self.porc_suciedad / 100) 
        #self.suciedadActual = cant_suciedad
        cant_suciedad = self.suciedadActual
        for i in range(cant_suciedad):
            x = 0
            y = 0
            while True:
                x = random.randint(0,self.n - 1)
                y = random.randint(0,self.m- 1)

                if self.habitacion[x][y].es_vacia():
                    break
            self.habitacion[x][y].annadir("S") 

    def en_rango(self,x,y):
        return x >= 0 and x < self.n and y >= 0 and  y < self.m

    def construirCorral(self,x,y,cant_ninos):
        
        if cant_ninos > 0:
            
            for k in range(0,len(self.desplazamiento_x)):
                n_x = x + self.desplazamiento_x[k]
                n_y = y + self.desplazamiento_y[k]

                if self.en_rango(n_x,n_y) and self.habitacion[n_x][n_y].es_vacia():
                    self.habitacion[n_x][n_y].annadir("C")
                    self.corral.append((n_x,n_y))
                    espacios_creados = 1
                    cantitad  = self.construirCorral(n_x,n_y,cant_ninos - 1)
                    espacios_creados += cantitad
                    if cant_ninos - espacios_creados == 0:
                        break
                    else:
                        cant_ninos -= espacios_creados
            
            return espacios_creados
        return 0

    def generarCorral(self):
        
        x = random.randint(0,self.n - 1)
        y = random.randint(0,self.m - 1)

        self.habitacion[x][y].annadir("C")
        self.corral.append((x,y))
        self.construirCorral(x,y,self.cant_ninos - 1)

    def verificar_conexidad(self,pos_x,pos_y,x,y,marca):
        marca[pos_x][pos_y] = 1
        visitados = 1
        for k in range(0,len(self.desplazamiento_x)):
                n_x = pos_x + self.desplazamiento_x[k]
                n_y = pos_y + self.desplazamiento_y[k]
                if n_x == x and n_y == y:
                    continue
                #if self.en_rango(n_x,n_y) and not self.habitacion[n_x][n_y].contiene("O") and not (self.habitacion[n_x][n_y].contiene("C") and self.habitacion[n_x][n_y].contiene("N")) and marca[n_x][n_y] == 0  :
                if self.en_rango(n_x,n_y) and not self.habitacion[n_x][n_y].contiene("O") and marca[n_x][n_y] == 0  :
                    visitados += self.verificar_conexidad(n_x,n_y,x,y,marca)
        return visitados


    def conexo(self,x,y,cant_obstaculos):
        init_x = -1
        init_y = -1
        for i in range(self.n):
            if init_x != -1:
                break
            for j in range(self.m):
                if i == x and j == y :
                    continue
                if self.habitacion[i][j].es_vacia():
                    init_x = i
                    init_y = j
                    break

        lista_auxliar = []
        for i in range(self.n):
            lista_auxliar.append([0] * self.m)

        ninnosCorral = self.cant_ninos - self.ninnosSueltos
        #return (self.n * self.m - cant_obstaculos - ninnosCorral) == (self.verificar_conexidad(init_x,init_y,x,y,lista_auxliar) + 1 )
        return (self.n * self.m - cant_obstaculos ) == (self.verificar_conexidad(init_x,init_y,x,y,lista_auxliar) + 1 )
        

    def ubicar_obstaculo(self,x,y,cant_obstaculos):
        if not self.habitacion[x][y].es_vacia():
            return False
        else:
            if self.conexo(x,y,cant_obstaculos):
                return True
            return False
    
    def generarObstaculos(self):
        cant_obstaculos = int(self.n * self.m * self.porc_obstaculo / 100) 
        
        for i in range(0,cant_obstaculos):
            while True:
                x = random.randint(0,self.n - 1)
                y = random.randint(0,self.m - 1)
                if self.ubicar_obstaculo(x,y,i):
                    break
            
            self.habitacion[x][y].annadir("O")
    
    def ubicarNinos(self):
        for i in range(self.cant_ninos):
            x = 0
            y = 0
            while True:
                x = random.randint(0,self.n- 1)
                y = random.randint(0,self.m-1 )

                if self.habitacion[x][y].es_vacia():
                    break
            self.habitacion[x][y].annadir("N")
            self.ninnos.append((x,y)) 
    
    def ubicarRobot(self):
        while True:
                x = random.randint(0,self.n - 1)
                y = random.randint(0,self.m - 1)

                if self.habitacion[x][y].es_vacia():
                    self.robot = robot(x,y)
                    self.habitacion[x][y].annadir("R")
                    break
    
    def generarAmbiente(self):
        for i in range(self.n):
            self.habitacion.append([]) 
            for j in range(self.m):
                self.habitacion[i].append(casilla())
            
        
        self.generarCorral()
        self.generarObstaculos()
        self.generarSuciedad()
        self.ubicarNinos()
        self.ubicarRobot()


    def generarSuciedadNinno(self,x,y):
        casillaLibres = []
        ninnos = 1
        desplazamiento_x = [-1,-1 ,0,1,1,1,0,-1]
        desplazamiento_y = [0,1,1,1,0,-1,-1,-1]
        nuevaSuciedad = 0


        for k in range(0,len(desplazamiento_x)):
            n_x = x + desplazamiento_x[k]
            n_y = y + desplazamiento_y[k]

            if self.en_rango(n_x,n_y):
                if self.habitacion[n_x][n_y].es_vacia():
                    casillaLibres.append((n_x,n_y))
                elif self.habitacion[n_x][n_y].contiene("N"):
                    ninnos += 1

        if ninnos == 1:
            nuevaSuciedad = random.randint(0,1)
        elif ninnos == 2:
            nuevaSuciedad = random.randint(0,3)
        else:
            nuevaSuciedad = random.randint(0,6)
        
        print(f'el nino en {x},{y} genero {nuevaSuciedad} nuevas basuras')

        casillaLibres = random.sample(casillaLibres,min(len(casillaLibres),nuevaSuciedad))
        for i,j in casillaLibres:
            self.habitacion[i][j].annadir("S")
            self.suciedadActual += 1

    def movimientoInvalido(self,x,y):    
        Tcorral = self.habitacion[x][y].contiene("C")
        Trobot = self.habitacion[x][y].contiene("R")
        Tninno = self.habitacion[x][y].contiene("N")
        Tsuciedad = self.habitacion[x][y].contiene("S")
        return Tcorral or Tninno or Trobot or Tsuciedad  

    def moverNinno(self,x,y):
        if random.randint(0,1):#Si decide moverse
            movimiento = random.randint(0,3)
            n_x = x + self.desplazamiento_x[movimiento]
            n_y = y + self.desplazamiento_y[movimiento]
            
            if self.en_rango(n_x,n_y) and not self.movimientoInvalido(n_x,n_y):
                if self.habitacion[n_x][n_y].es_vacia():
                    self.habitacion[n_x][n_y].annadir("N")
                    self.habitacion[x][y].remover("N")
                    print(f'El ninno en {x},{y} decidio moverse en la dir {movimiento} y se pudo mover')
                    self.generarSuciedadNinno(n_x,n_y)
                    return (n_x,n_y)
                else:
                    aux_x = n_x + self.desplazamiento_x[movimiento]
                    aux_y = n_y + self.desplazamiento_y[movimiento]
                    while self.en_rango(aux_x,aux_y) :
                        
                        if self.habitacion[aux_x][aux_y].es_vacia():
                            while True:
                                aux1_x = aux_x - self.desplazamiento_x[movimiento]
                                aux1_y = aux_y - self.desplazamiento_y[movimiento]
                                self.habitacion[aux_x][aux_y].annadir("O")
                                self.habitacion[aux1_x][aux1_y].remover("O")
                                aux_x = aux1_x
                                aux_y = aux1_y
                                if aux_x == n_x and aux_y == n_y:
                                    break
                            self.habitacion[n_x][n_y].annadir("N")
                            self.habitacion[x][y].remover("N")
                            print(f'El ninno en {x},{y} decidio moverse en la dir {movimiento} y se pudo mover')
                            self.generarSuciedadNinno(n_x,n_y)
                            return (n_x,n_y)

                        elif self.habitacion[aux_x][aux_y].contiene("O"):
                            aux_x = aux_x + self.desplazamiento_x[movimiento]
                            aux_y = aux_y + self.desplazamiento_y[movimiento] 
                        else:
                            print(f'El ninno en {x},{y} decidio moverse en la dir {movimiento} pero no se pudo mover')
                            return (x,y)
                    
                    print(f'El ninno en {x},{y} decidio moverse en la dir {movimiento} pero no se pudo mover')
                    return (x,y)
                    

            else:
                print(f'El ninno en {x},{y} decidio moverse en la dir {movimiento} pero no se pudo mover')  
                return (x,y)  
        else:
            print(f'El ninno en {x},{y} decidio no moverse')
            return (x,y)

    def moverNinnos(self):
        nuevasPosiciones = []
        for x,y in self.ninnos:
            if (x,y) not in self.corral:
                nuevasPosiciones.append(self.moverNinno(x,y))
                self.imprimir_mundo()
                #input()
            else:
                nuevasPosiciones.append((x,y))


        self.ninnos = nuevasPosiciones

    def cambiarAmbiente(self):
        corral = list(self.corral)
        self.habitacion = []
        
        self.corral = []
        for i in range(self.n):
            self.habitacion.append([]) 
            for j in range(self.m):
                self.habitacion[i].append(casilla())
        
        self.generarCorral()

        ninnos = []
        for i in range(len(self.ninnos)):
            x,y = self.ninnos[i]
            if (x,y) in corral:
                pos_x ,pos_y = self.corral[i]
                self.habitacion[pos_x][pos_y].annadir("N")
                ninnos.append((pos_x,pos_y))

        self.generarObstaculos()
        self.generarSuciedad()#mantener actualizada la suciedad

        #reubicar ninnos 
        #ninnos = []
        for i in range(len(self.ninnos)):
            x,y = self.ninnos[i]
            if (x,y) in corral:
                continue
        #        pos_x ,pos_y = self.corral[i]
        #        self.habitacion[pos_x][pos_y].annadir("N")
        #        ninnos.append((pos_x,pos_y))
            #este caso hay q manejarlo en el movimiento(si estas dentro de un robot no estas en el mapa)
            #elif self.robot.pos_x == x and self.robot.pos_y == y and self.robot.nino:
            #    continue
            else:
                while True:
                    x = random.randint(0,self.n- 1)
                    y = random.randint(0,self.m-1 )

                    if self.habitacion[x][y].es_vacia():
                        break
                self.habitacion[x][y].annadir("N")
                ninnos.append((x,y))
        self.ninnos = list(ninnos)

        #reubicar robot
        while True:
            x = random.randint(0,self.n- 1)
            y = random.randint(0,self.m-1 )

            if self.habitacion[x][y].es_vacia():
                self.habitacion[x][y].annadir("R")
                self.robot.pos_x = x
                self.robot.pos_y = y
                break

    def imprimir_mundo(self):
        for i in range(self.n):
            imprimir = ""
            for j in range(self.m):
                imprimir += str(self.habitacion[i][j])
            print(imprimir)

    
#a = ambiente(2,3,5,20,10)

#a.imprimir_mundo()
    
# #a.cambiarAmbiente()

#print("*"*100)

# # a.imprimir_mundo()



#t = 1
#for i in range(20):
    #a.moverNinnos()
    #a.robot.mover1(a)
#    a.robot.mover2(a)
#    a.imprimir_mundo()
#    input()
#    a.moverNinnos()
#    if t % 9 == 0:
#        a.cambiarAmbiente()
#        a.imprimir_mundo()
#        input()

#    t += 1

# S  O  O  N  _  O  C/N C/N C/N C  
# S  O  S  S  S  R  C/N _  _  _  
# S  S  S  _  _  S  _  O  S  _  
# S  _  S  _  _  S  _  _  S  O  
# S  S  S  _  _  _  _  _  O  _  
# S  S  S  _  S  _  _  S  S  _  
# _  S  S  _  _  O  S  _  S  _  
# O  S  _  _  S  O  O  O  S  S 

# a = ambiente(5,8,10,10,15)



# a.habitacion = []
# a.ninnos = [(0,3) , (0,6),(1,6),(0,7),(0,8)]
# for i in range(a.n):
#     a.habitacion.append([]) 
#     for j in range(a.m):
#         a.habitacion[i].append(casilla())

# a.robot.pos_x = 1 
# a.robot.pos_y = 5
# a.robot.nino = False
# a.habitacion[0][4].annadir("S")
# a.habitacion[1][0].annadir("O")
# a.habitacion[0][1].annadir("C")
# a.habitacion[0][2].annadir("C")
# a.habitacion[0][2].annadir("N")
# a.habitacion[0][2].annadir("R")
# a.habitacion[0][4].annadir("S")
# a.habitacion[2][1].annadir("S")
# #a.habitacion[1][3].annadir("S")
# a.habitacion[0][0].annadir("N")
# a.ninnos = [(0,0),(0,3)]
#a.corral = [(0,6),(1,6),(0,7),(0,8),(0,9)]

#a.ninnosSueltos = 1
# a.porc_obstaculo = 10
#a.suciedadActual = 30
#a.cambiarAmbiente()
#a.imprimir_mundo()

# a.robot.mover(a)
# a.imprimir_mundo()
# input()
# a.robot.mover(a)
# a.imprimir_mundo()
# input()

# a.habitacion[1][1].annadir("O")
# a.habitacion[2][1].annadir("N")
# a.ninnos.append((2,1))
# a.imprimir_mundo()
# a.moverNinnos()
# a.moverNinnos()
# a.moverNinnos()
# a.moverNinnos()
# a.moverNinnos()
# a.moverNinnos()