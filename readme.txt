
Para simular el proceso correr el main.py:

    python main.py


El main.py brinda un metodo simulacion que recibe los siguientes parametros:
    -cantidad de ninos
    -cantidad de filas del mundo
    -cantidad de columnas del mundo
    -porciento de suciedad inicial con respecto al total de casillas
    -porciento de obstaculos iniciales con respecto al total de casillas
    -el metodo retorna para ese determinado escenario una tupla de ganados y perdidos,

Modelo de Agente ejecutado:
    Por defecto se esta corriedo el metodo mover2 , el cual esta asociado al modelo 2 .Si se quieren probar los otros agentes cambiar la siguiente linea en el metodo simulacion del main.py:
        a.robot.mover2(a)
        posible cambios:
        a.robot.mover(a) ,corresponde al modelo 3 explicado en el infome
        a.robot.mover2P(a) ,corresponde al modelo 4 explicado en el informe
        a.robot.mover3(a) , corresponde al modelo 1 explicado en el informe
