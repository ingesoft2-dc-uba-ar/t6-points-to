from pyDatalog import pyDatalog

pyDatalog.create_terms('Abuelo, Padre, X, Y, Z') # para indicar que son terminos de nuestros predicados/reglas

Abuelo(X, Z) <= Padre(X, Y) & Padre(Y, Z)

+Padre("Carlos", "Juan")
+Padre("Juan", "Esteban")

for a, b in Abuelo(X, Z).data:
    print(f"{a} es abuelo de {b}")

# no llamo a clear() -> siguen valiendo las reglas y hechos anteriores

