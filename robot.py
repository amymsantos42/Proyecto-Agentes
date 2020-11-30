import random

class robot():
    def __init__(self,x,y):
        self.pos_x = x
        self.pos_y = y
        self.nino = False
        self.objetivo = []
        self.objetivoNombre = ""

    def buscarObjetivo(self,x,y,objetivo,camino,distancia,ambiente,dic):

        if (x,y) in dic.keys():
            if dic[(x,y)] < distancia :
                return False , camino ,distancia
            else:
                dic[(x,y)] = distancia
        else:
            dic[(x,y)] = distancia

        if ambiente.habitacion[x][y].contiene(objetivo) and (self.pos_x ,self.pos_y) != (x, y):
            return True , camino , distancia

        posiblesMovimientos = self.puedeMoverse(ambiente,x,y)
        if len(posiblesMovimientos) > 0:
            minimo = 10**9
            caminoMinimo = []
            camino.append((-1,-1))
            for n_x,n_y in posiblesMovimientos:
                camino[len(camino)-1] = (n_x,n_y)
                Aobjetivo , nuevoCamino , distanciaAux = self.buscarObjetivo(n_x,n_y,objetivo,list(camino),distancia + 1,ambiente,dic) 
                if Aobjetivo :
                    if distanciaAux < minimo:
                        minimo = distanciaAux
                        caminoMinimo = nuevoCamino
            
            if minimo == 10**9:
                return False ,camino ,distancia
            return True , caminoMinimo , minimo

        return False , camino ,distancia



    def mover2P(self,ambiente):
        recalcular = False
        if len(self.objetivo) > 0:
            n_x , n_y = self.objetivo.pop(0)
            if self.movimientoInvalido(ambiente,n_x,n_y):
                recalcular = True
                
            else :
                if self.objetivoNombre == "N":
                    if ambiente.habitacion[n_x][n_y].contiene("N"):
                        self.cargar_nino(ambiente,n_x,n_y)
                    else:
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")

                elif self.objetivoNombre == "C":
                    if ambiente.habitacion[n_x][n_y].contiene("C"):
                        self.soltar_nino(ambiente,n_x,n_y)
                    else:
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")

                else:
                    ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                    self.pos_x = n_x
                    self.pos_y = n_y
                    ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                
                    
                
        if len(self.objetivo) == 0 or recalcular:
            #fijar objetivo 
            if self.nino :
                if ambiente.ninnosSueltos > 1:
                    Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"C",[],0,ambiente,{})
                    if Aobjetivo:
                        self.objetivo = camino
                        self.objetivoNombre = "C"
                        self.mover2P(ambiente) 
                    else:
                        print(f'No veo el objetivo')
                else :
                    if ambiente.suciedadActual > 0 : 
                        if ambiente.habitacion[self.pos_x][self.pos_y].contiene("S"):
                            self.limpiar(ambiente)
                        else:
                            Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"S",[],0,ambiente,{})
                            if Aobjetivo:
                                self.objetivo = camino
                                self.objetivoNombre = "S"
                                self.mover2P(ambiente)
                            else:
                                print(f'No veo el objetivo')   
                    else:
                        Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"C",[],0,ambiente,{})
                        if Aobjetivo:
                            self.objetivo = camino
                            self.objetivoNombre = "C"
                            self.mover2P(ambiente) 
                        else:
                            print(f'No veo el objetivo')
            else:
                if ambiente.ninnosSueltos == 0:
                    print("Termine")
                else:
                    Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"N",[],0,ambiente,{})

                    if Aobjetivo:
                        self.objetivo = camino
                        self.objetivoNombre = "N"
                        self.mover2P(ambiente) 
                    else:
                        print(f'No veo el objetivo')  

    def mover2(self,ambiente):
        if self.nino :
            if ambiente.ninnosSueltos > 1:
                Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"C",[],0,ambiente,{})
                if Aobjetivo:
                    if len(camino) >= 2 :
                        n_x , n_y = camino.pop(1)
                    else:
                        n_x , n_y = camino.pop(0)

                    if ambiente.habitacion[n_x][n_y].contiene("C"):
                        self.soltar_nino(ambiente,n_x,n_y)
                    else:
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                else:
                    print(f'No veo el objetivo')  
            else:
                if ambiente.suciedadActual > 0 :
                    if ambiente.habitacion[self.pos_x][self.pos_y].contiene("S"):
                        self.limpiar(ambiente)
                    else:
                        Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"S",[],0,ambiente,{})
                        if Aobjetivo:
                            if len(camino) >= 2 :
                                n_x , n_y = camino.pop(1)
                            else:
                                n_x , n_y = camino.pop(0)
                            ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                            self.pos_x = n_x
                            self.pos_y = n_y
                            ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                        else:
                            print(f'No veo el objetivo')  
                else:
                    Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"C",[],0,ambiente,{})
                    if Aobjetivo:
                        if len(camino) >= 2 :
                            n_x , n_y = camino.pop(1)
                        else:
                            n_x , n_y = camino.pop(0)
                            
                        if ambiente.habitacion[n_x][n_y].contiene("C"):
                            self.soltar_nino(ambiente,n_x,n_y)
                        else:

                            ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                            self.pos_x = n_x
                            self.pos_y = n_y
                            ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                    else:
                        print(f'No veo el objetivo') 

        else:
            if ambiente.ninnosSueltos == 0:
                print("Termine")
            else:
                Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"N",[],0,ambiente,{})

                if Aobjetivo:
                    n_x , n_y = camino.pop(0)
                    if ambiente.habitacion[n_x][n_y].contiene("N"):
                        self.cargar_nino(ambiente,n_x,n_y)
                    else:
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                else:
                    print(f'No veo el objetivo')  
    
    def objetivoUnPaso(self,objetivo,ambiente):

        posiblesMovimientos = self.puedeMoverse(ambiente,self.pos_x,self.pos_y)
        for n_x,n_y in posiblesMovimientos:
            if ambiente.habitacion[n_x][n_y].contiene(objetivo):
                return True , (n_x,n_y)
        return False , None

    def mover3(self,ambiente):
        if ambiente.suciedadActual > 0 :

            if ambiente.habitacion[self.pos_x][self.pos_y].contiene("S"):
                self.limpiar(ambiente)
            else:
                val , proximaPos = self.objetivoUnPaso("N",ambiente)
                val1 , proximaPos1 = self.objetivoUnPaso("C",ambiente)
                if self.nino == False and val:
                    self.cargar_nino(ambiente,proximaPos[0],proximaPos[1])
                elif self.nino == True and val1:
                    self.soltar_nino(ambiente,proximaPos1[0],proximaPos1[1])
                else:
                    Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"S",[],0,ambiente,{})
                    if Aobjetivo:
                        n_x , n_y = camino.pop(0)
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                    else:
                        print(f'No veo el objetivo')  
        else:
            if self.nino :
                Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"C",[],0,ambiente,{})
                if Aobjetivo:
                    n_x , n_y = camino.pop(0)
                    if ambiente.habitacion[n_x][n_y].contiene("C"):
                        self.soltar_nino(ambiente,n_x,n_y)
                    else:

                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                else:
                    print(f'No veo el objetivo')
            else :
                Aobjetivo , camino , _ = self.buscarObjetivo(self.pos_x,self.pos_y,"N",[],0,ambiente,{})
                if Aobjetivo:
                    n_x , n_y = camino.pop(0)
                    if ambiente.habitacion[n_x][n_y].contiene("N"):
                        self.cargar_nino(ambiente,n_x,n_y)
                    else:
                        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                        self.pos_x = n_x
                        self.pos_y = n_y
                        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                else:
                    print(f'No veo el objetivo')
            

    
    def movimientoInvalido(self,ambiente,x,y):
        TObstaculo = ambiente.habitacion[x][y].contiene("O")
        TCorral_Ninno = ambiente.habitacion[x][y].contiene("C") and ambiente.habitacion[x][y].contiene("N")
        TNinno_lleno = ambiente.habitacion[x][y].contiene("N") and self.nino
        return TObstaculo or TNinno_lleno or TCorral_Ninno

    def puedeMoverse(self,ambiente,x,y):
        posiblesMovimientos = []
        for k in range(len(ambiente.desplazamiento_x)):
            n_x = x + ambiente.desplazamiento_x[k]
            n_y = y + ambiente.desplazamiento_y[k]

            if ambiente.en_rango(n_x,n_y) and not self.movimientoInvalido(ambiente,n_x,n_y):
                posiblesMovimientos.append((n_x,n_y ))
        return posiblesMovimientos

    def mover(self,ambiente):
        if ambiente.habitacion[self.pos_x][self.pos_y].contiene("S"):
            self.limpiar(ambiente)
        else:
            posiblesMovimientos = self.puedeMoverse(ambiente,self.pos_x,self.pos_y)
            if len(posiblesMovimientos) > 0:
                n_x , n_y = posiblesMovimientos[ random.randint(0,len(posiblesMovimientos)-1) ]
                print(f'El robot se movio a la posicion {n_x},{n_y}')
                if ambiente.habitacion[n_x][n_y].contiene("C") and self.nino:
                    self.soltar_nino(ambiente,n_x,n_y)
                elif ambiente.habitacion[n_x][n_y].es_vacia() or ambiente.habitacion[n_x][n_y].contiene("C") or ambiente.habitacion[n_x][n_y].contiene("S"):
                    ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
                    self.pos_x = n_x
                    self.pos_y = n_y
                    ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
                    
                elif ambiente.habitacion[n_x][n_y].contiene("N"):
                    self.cargar_nino(ambiente,n_x,n_y)
                    
                
            else:
                print("El robot no tiene movimientos validos")
                    
    def cargar_nino(self,ambiente,x,y):
        self.nino = True
        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
        self.pos_x = x
        self.pos_y = y 
        ambiente.habitacion[self.pos_x][self.pos_y].remover("N")
        ambiente.habitacion[self.pos_x][self.pos_y].annadir("R")
        ambiente.ninnos.remove((x,y))
        print(f'el robot cargo el ninno de la posicion {self.pos_x},{self.pos_y}')
    
    def limpiar(self,ambiente):
        ambiente.habitacion[self.pos_x][self.pos_y].remover("S")
        ambiente.suciedadActual -= 1
        print(f'el robot limpio la posicion {self.pos_x},{self.pos_y}')
    
    def soltar_nino(self,ambiente,x,y):
        ambiente.habitacion[x][y].annadir("R")
        ambiente.habitacion[x][y].annadir("N")
        ambiente.habitacion[self.pos_x][self.pos_y].remover("R")
        self.pos_x = x
        self.pos_y = y
        self.nino = False
        ambiente.ninnos.append((x,y))
        ambiente.ninnosSueltos -= 1
        print(f'el robot solto al ninno en la posicion {self.pos_x},{self.pos_y}')
        
    
    
    
    