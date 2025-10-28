from pyDatalog import pyDatalog

pyDatalog.create_terms('Abuelo, Padre, X, Y, Z') # para indicar que son terminos de nuestros predicados/reglas

Abuelo(X, Z) <= Padre(X, Y) & Padre(Y, Z)

+Padre("Carlos", "Juan")
+Padre("Juan", "Esteban")

for a, b in Abuelo(X, Z).data:
    print(f"{a} es abuelo de {b}")

# no llamo a clear() -> siguen valiendo las reglas y hechos anteriores

pyDatalog.create_terms('Bisabuelo')

Bisabuelo(X, Y) <= Padre(X, Z) & Abuelo(Z, Y)

+Padre("Esteban", "Alberto")
+Padre("Esteban", "Blas")
+Padre("Alberto", "Oscar")

print()
for a, b in Bisabuelo(X, Y).data:
    print(f"{a} es bisabuelo de {b}")

pyDatalog.create_terms('Familiar')

Familiar(X, Y) <= Padre(X, Y)
Familiar(X, Y) <= Padre(Y, X)
Familiar(X, Y) <= Familiar(X, Z) & Familiar(Z, Y)

print()
for a, b in Familiar(X, Y).data:
    print(f"{a} es familiar de {b}")

pyDatalog.create_terms('Antepasado')

Antepasado(X, Y) <= Padre(X, Y)
Antepasado(X, Y) <= Antepasado(X, Z) & Antepasado(Z, Y)

print()
for a, b in Antepasado(X, Y).data:
    print(f"{a} es antepasado de {b}")


