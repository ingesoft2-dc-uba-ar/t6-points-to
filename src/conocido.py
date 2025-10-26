from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('Amigo, Conocido, X, Y, Z')

# Facts
+Amigo('alicia', 'beto')
+Amigo('beto', 'camila')
+Amigo('ximena', 'yamila')
+Conocido('ximena', 'zoilo')

# Reglas

# R1.a: si X es amigo de Y => X es conocido de Y
Conocido(X, Y) <= Amigo(X, Y) 

# R2: la relacion Amigo() es simetrica (podriamos hacer que no lo sea)
Amigo(X, Y) <= Amigo(Y, X)

# R3: si X es amigo de Z y Z es conocido de Y => X es conocido de Y. Pero alguien no es conocido de si mismo
Conocido(X, Y) <= Amigo(X, Z) & Conocido(Z, Y) & (X != Y)

# R4: si X es conocido de Z y Z es conocido de Y => X es conocido de Y. Pero alguien  no es conocido de si mismo
Conocido(X, Y) <= Conocido(X, Z) & Conocido(Z, Y) & (X != Y)

print(Conocido(X, Y))
