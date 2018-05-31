# -*- coding: utf-8 -*-
"""
Created on Sun May 27 14:35:16 2018

Jose Alejandro Aristizabal
Daniel Fandiño Ocampo
Alejandro Jaramillo Hidalgo
Ismael Restrepo

"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
MetX = np.arange(0, 30, 1)
MetodoUsado = ctrl.Antecedent(MetX, 'MetodoUsado')

edad = ctrl.Antecedent(np.arange(12, 55, 1), 'edad')
hijos = ctrl.Antecedent(np.arange(0, 16, 1), 'hijos')

EfectX = np.arange(0, 26, 1)
efectividad = ctrl.Consequent(EfectX, 'efectividad')

# Auto-membership function population is possible with .automf(3, 5, or 7)
#MetodoUsado.automf(3)
#edad.automf(3)
#TerceraVariableDeEntrada.automf(3)


MetodoUsado['CortoPlazo'] = fuzz.trapmf(MetodoUsado.universe, [0, 0, 3, 5])
MetodoUsado['LargoPlazo'] = fuzz.trapmf(MetodoUsado.universe, [3, 5, 30, 30])

#Grafica 1
#MetodoUsado.view()

fuzz.centroid

edad['Joven'] = fuzz.trapmf(edad.universe, [12, 12, 20, 25])
edad['Madura'] = fuzz.trapmf(edad.universe, [20, 25, 35, 40])
edad['Veterana'] = fuzz.trapmf(edad.universe, [35, 40, 55, 55])

#Grafica 2
#edad.view()

hijos['pocos'] = fuzz.trapmf(hijos.universe, [0, 0, 2, 3])
hijos['moderado'] = fuzz.trapmf(hijos.universe, [2, 3, 5, 6])
hijos['muchos'] = fuzz.trapmf(hijos.universe, [5, 6, 15, 15])

#Grafica 3
#hijos.view()

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
efectividad['baja'] = fuzz.trapmf(efectividad.universe, [0, 0, 5, 10])
efectividad['media'] = fuzz.trapmf(efectividad.universe, [5, 10, 15, 20])
efectividad['alta'] = fuzz.trapmf(efectividad.universe, [15, 20, 25, 25])

#quality['average'].view()

#Reglas del sistema
rule1 = ctrl.Rule(MetodoUsado['LargoPlazo'] and edad['Joven'] and hijos['muchos'], efectividad['baja'])
rule2 = ctrl.Rule(MetodoUsado['LargoPlazo'] and edad['Madura'] and hijos['moderado'], efectividad['media'])
rule3 = ctrl.Rule(MetodoUsado['LargoPlazo'] and edad['Veterana'] and hijos['pocos'], efectividad['alta'])
rule4 = ctrl.Rule(MetodoUsado['CortoPlazo'] and edad['Joven'] and hijos['muchos'], efectividad['baja'])
rule5 = ctrl.Rule(MetodoUsado['CortoPlazo'] and edad['Madura'] and hijos['moderado'], efectividad['media'])
rule6 = ctrl.Rule(MetodoUsado['CortoPlazo'] | edad['Veterana'] | hijos['pocos'], efectividad['alta'])

#MetodoUsado.view()
#edad.view()
#hijos.view()
#efectividad.view()

#rule1.view()

effectiveness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
effectiveness = ctrl.ControlSystemSimulation(effectiveness_ctrl)



# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)

#Valores de entrada para el fuzzy

a = input("Ingrese el valor del Metodo Anticonceptivo Usado: ")
b = input("Ingrese la edad: ")
c = input("Ingrese el numero de hijos: ") 


effectiveness.input['MetodoUsado'] = a
effectiveness.input['edad'] = b
effectiveness.input['hijos'] = c

# Crunch the numbers
effectiveness.compute()

#print("Efectividad del anticonceptivo: ")
#print (effectiveness.output['efectividad'])
#Grafica 4
#efectividad.view(sim=effectiveness)

#z = effectiveness.output['efectividad']

#d = effectiveness.['efectividad']

#print(d)


# Definición categorias para usar en la defusificación
def metodo_Categoria(metodo_in):
    Metodo_CortoPlazo = fuzz.interp_membership(MetX,fuzz.trapmf(MetodoUsado.universe, [0, 0, 3, 5]),metodo_in) # Depends from Step 1
    Metodo_LargoPlazo = fuzz.interp_membership(MetX,fuzz.trapmf(MetodoUsado.universe, [3, 5, 30, 30]),metodo_in) # Depends form Step 1
    return dict(corto = Metodo_CortoPlazo,largo = Metodo_LargoPlazo)

def efectividad_categoria(efectividad_in):
    efectividad_baja = fuzz.interp_membership(EfectX,fuzz.trapmf(efectividad.universe, [0, 0, 5, 10]), efectividad_in) # Depends from Step 1
    efectividad_media = fuzz.interp_membership(EfectX,fuzz.trapmf(efectividad.universe, [5, 10, 15, 20]), efectividad_in)
    efectividad_alta = fuzz.interp_membership(EfectX, fuzz.trapmf(efectividad.universe, [15, 20, 25, 25]), efectividad_in)
    return dict(baja = efectividad_baja, media = efectividad_media, alta = efectividad_alta)

#Exaple input variables 
meotodo_in = metodo_Categoria(a)
efectividad_in = efectividad_categoria(effectiveness.output['efectividad'])
print "Para el metodo ", meotodo_in
print "Para efectividad ",efectividad_in 


# Reglas usadas para la defusificación
rul1 = np.fmax(efectividad_in['baja'],meotodo_in['corto'])
rul2 = efectividad_in['media']
rul3 = np.fmax(meotodo_in['largo'],efectividad_in['alta'])

imp1= np.fmin(rul1,fuzz.trapmf(efectividad.universe, [0, 0, 5, 10]))
imp2 = np.fmin(rul2,fuzz.trapmf(efectividad.universe, [5, 10, 15, 20]))
imp3 = np.fmin(rul3,fuzz.trapmf(efectividad.universe, [15, 20, 25, 25]))

# Defusificación
aggregate_membership = np.fmax(imp1, np.fmax(imp2,imp3))
resultado = fuzz.defuzz(EfectX, aggregate_membership , 'centroid')
print resultado

# Categoria a la que pertenece el método anticonceptivo usado
print(efectividad_categoria(resultado))
categoria = max(efectividad_categoria(resultado), key=efectividad_categoria(resultado).get)

print "La efectividad del metodo es:", categoria

if categoria == 'baja': 
    print("Experto habla de la calidad baja del metodo")
    
elif categoria == 'media': 
    print("Experto habla de la calidad media del metodo")
    
elif categoria == 'alta':
    print("Experto habla de la calidad alta del metodo")
