
from ambiente import *



def simulacion(cant_ninos,n,m,porc_suciedad,porc_obstaculo,t):
    
    ganados = 0
    perdidos = 0
    for k in range(30):
        a = ambiente(cant_ninos,n,m,porc_suciedad,porc_obstaculo)
        a.imprimir_mundo()
        casillasLibres = n * m - 1 - cant_ninos - a.porc_obstaculo
        #input()
        val = False
        for i in range(100):
            if val:
                break

            for j in range(t):
                a.robot.mover2(a)
                

                a.imprimir_mundo()
                #input()
                a.moverNinnos()

                if a.suciedadActual * 100 / casillasLibres > 60:
                    print("Robot despedido")
                    perdidos += 1
                    val = True
                    break
                if a.suciedadActual == 0 and a.ninnosSueltos == 0:
                    print("Robot ascendido")
                    ganados += 1
                    val = True
                    break

            a.cambiarAmbiente()
        if not val:
            print("Se acabo la simulacion")
        print(f'El robot gano {ganados} , perdio {perdidos} y empato un total de {30 - ganados - perdidos} ')
        
    return ganados,perdidos



resultados = []
#resultados.append(simulacion(5,8,10,30,15,10))
#resultados.append(simulacion(5,8,10,30,15,20))
resultados.append(simulacion(2,3,5,5,10,15))
resultados.append(simulacion(2,3,5,10,10,5))
#resultados.append(simulacion(3,4,4,20,5,30))
#resultados.append(simulacion(3,4,4,20,5,20))
resultados.append(simulacion(4,5,6,5,15,25))
#resultados.append(simulacion(4,5,6,15,15,15))
#resultados.append(simulacion(7,8,10,20,10,15))
#resultados.append(simulacion(7,8,10,30,10,15))


print(resultados)


#resultados.append(simulacion(2,3,5,20,10,15))
#resultados.append(simulacion(2,3,5,20,10,5))
#resultados.append(simulacion(4,5,6,35,15,25))
#resultados.append(simulacion(4,5,6,35,15,15))