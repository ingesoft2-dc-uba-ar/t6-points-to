from src.prolog import PrologRunner

runner = PrologRunner()
output = runner.run_program(r"""
:- table amigo/2.
:- table conocido/2.

% Facts
amigo(alicia, beto).
amigo(beto, camila).
amigo(ximena, yamila).
conocido(ximena, zoilo).

% Reglas

% R1: si X es amigo de Y => X es conocido de Y
conocido(X, Y) :- amigo(X, Y).

% R2: la relacion amigo es simetrica (podriamos hacer que no lo sea)
amigo(X, Y) :- amigo(Y, X).

% R3: si X es amigo de Z y Z es conocido de Y => X es conocido de Y. Pero alguien no es conocido de si mismo
conocido(X, Y) :- amigo(X, Z), conocido(Z, Y), X \= Y.

% R4: si X es conocido de Z y Z es conocido de Y => X es conocido de Y. Pero alguien no es conocido de si mismo
conocido(X, Y) :- conocido(X, Z), conocido(Z, Y), X \= Y.

:- forall(conocido(X, Y),
    format('~w es conocido de ~w~n', [X, Y])).
:- halt.
""")

print(output)
