import re
import numpy.polynomial.polynomial as poly
import numpy as np
from scipy import optimize


def getcoef(): # recuerda que si no hay termino independiente se le quita el espacio al final de la funcion
    read_coef = open("C:\\Archivos\\coeficientes.txt", "r", encoding="utf-8")
    get_coef = read_coef.read()
    read_coef.close()

    temp = re.findall(r'(-?\d*)x', get_coef) + re.findall(r'(-?\d*) ', get_coef)  # toma los coeficientes
    pot = ("".join(re.findall(r'(\^\d*)', get_coef))).split("^")  # toma las potencias

    # arreglamos temp con espacio
    for i in range(len(temp)):
        if temp[i] == '' or temp[i] == '-':
            temp[i] = 1

    potx = re.findall(r'(x\^)', get_coef)
    pot1 = re.findall(r'(x\d*)', get_coef)

    del pot[0]  # borra un lugar de la lista ocupado por un espacio en blanco
    potencias = list(map(int, pot))  # convierte la lista de strings de potencias en lista de ints
    coeficientes = list(map(int, temp))  # convierte la lista de strings de coeficientes en lista de ints

    bandera = False
    if len(pot1) != len(potx):  # agarrar la potencia 1 dek valro x      pot1 numero de x, potx numero de x con un ^
        potencias.append(1)
    # si el numero de x y de x^ es igual y el numero de coef es mayor al de potencias
    elif len(pot1) == len(potx) and len(coeficientes) > len(potx) > 1:
        potencias.append(0)
    elif len(pot1) == len(potx) and len(potx) == 1:
        print("es una unica x ")
        bandera = True  # if True es ua sola x y puede (o no) contener algun otro termino

    # def Dic
    # armamos el dicionario que relaciona coef y potencias
    if len(potencias) == len(coeficientes):
        DicCoefPow = dict(zip(potencias, coeficientes))
    else:
        potencias.append(0)  # agrego un 0 para len(potencias) == len(coeficientes) y que sea posible armar el
        # diccionario
        DicCoefPow = dict(zip(potencias, coeficientes))
        potencias.remove(0)  # quito el cero que agregue arriba para que la variable potencias solo tengapotencias
        # necesaria

    global grado
    potencias.sort()
    potencias.reverse()
    grado = potencias[0]

    # def FixPotencias
    # Arregla las potencias ////////////////////////////////(fixpow)
    fixpow = []
    for cont in range(grado + 1):
        fixpow.append(cont)
    fixpow.reverse()

    # def fixcoef
    # Arregla los coeficientes /////////////////////////////(fixcoef)
    fixcoef = []
    for i in range(grado + 1):
        if DicCoefPow.get(i) in coeficientes:
            fixcoef.append(DicCoefPow.get(i))
        else:
            fixcoef.append(0)
    fixcoef.reverse()

    return fixcoef



def bisection(a, b):   # funcion de biseccion descargada de internet
    if p(a) * p(b) >= 0:    #si el polinomio evaluado en a*b es mayor o igual a 0
        print("You have not assumed right a and b\n")   # intervalo invalido
        return
    c = a   #copiamos a en una nueva variable

    while (b - a) >= 0.01:  # mientras b-a esten en un rango aceptable

        # Find middle point
        c = (a + b) / 2

        # Check if middle point is root
        if p(c) == 0.0:
            break

        # Decide the side to repeat the steps
        if p(c) * p(a) < 0:
            b = c
        else:
            a = c

    print("El valor de la raiz es : ", "%.4f" % c)
    return c #retornamos el valor de la raiz


# pol= polinimio para div sintetica
# ao = divisor de la div sintetica
# newcoef= aqui se guardan los resultados de la div sintetica (lista)
# residuo= si es 0 es porque se encontro una raiz
raices =  []  # lista con las raices
def syntheticdiv(dividend, divisor): # esta funcion hace divison sintetica                                          p
    pol = list(dividend) # hago el polinomio                                                                        u
    a0 = divisor    # asigno el divisonr                                                                            t
    newcoef = []    # creo el arreglo donde se van a guardar los resultados de la division                          o
    for i in range(len(pol)):   # para cada elemento se hace la divison                                             E
        if i == 0:  # siempre se baja el primer coeficiente en la division por default                              L
            newcoef.append(pol[i])  # aqui se guarda nada mas                                                       I
        elif i < len(pol):  # mientras que no se nos acabe el polinomio                                             U
            newcoef.append((a0 * newcoef[i - 1]) + pol[i])  # se realizan las operacines correspondientes
    residuo = newcoef[-1]   # el residuo es la ultima posicion siempre
    # impresion de resultados
    print(f"Dividendo = {dividend}")
    print(f"Divisor = {divisor}")   # pol original
    print(f'Resultado = {newcoef}')     # pol resultante
    print(f'Residuo = {residuo}\n')

    for count in newcoef:   # por cada elemento en el resultado de la div sintetica
        if count < 0:   # verificamos si es positivo
            n = bisection(a0, a0+1) # si no, mandamos ese divisior y el siguiennte a biseccion
            raices.append(n)    # agregamos a la lista de raices
            break   # nos salimos del ciclo porque ya encontramos la raiz en ese intervalo

    if residuo == 0:    # si encontramos una raiz
        raices.append(a0)   # la agregamos
        print(f'{a0} es una raiz real')

    Fixraices = []  # lista de las raices con los decimales deseados
    for i in raices:    # este ciclo remueve los None de la lista de raices
        if i == None:
            raices.remove(i)
        else:
            Fixraices.append(i)

        sorted(set(Fixraices))     #elimina los elementos repetidos

    print(f"Las Raices son = {Fixraices}")
    return newcoef


def newtonraphson(x): # funcion de newton-Raphson descargada de internet
    P = p.deriv(1)  #primera derivada del polinomio p guardada en MAYUS p
    h = p(x) / P(x)
    while abs(h) >= 0.0001:
        h = p(x) / P(x)

        # x(i+1) = x(i) - f(x`) / f'(x)
        x = x - h

    print("El valor de la raiz es : %.4f" % x)


if __name__ == '__main__':  # función main
    p = np.poly1d(getcoef())    # p es nuestro polinomio, lo obtenemos de los coeficientes de la funcion getcoef()
    print("El polinomio original es:")
    print(f"{p}\n")
    a0 = p[-1]
    # Pminus = polinomio volteado
    Pminus = []
    Pminus = getcoef()

    for i in range(100):    # asigno el numero de iteraciones de la buscqueda de raices
        print(syntheticdiv(p, i))    # mando el polinomio y la iteracion a synteticdiv()
    print("------------------------------------------------------------------------------------------------------------")
    #for i in range(100):
    #   print(syntheticdiv(p, i*-1))

    for cont in range(grado): # refleja el polinomio en el eje dde las y
        Pminus[cont] = Pminus[cont]*-1

    #for i in range(100):
    #    print(syntheticdiv(Pminus, i*-1))


