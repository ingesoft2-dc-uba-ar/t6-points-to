from src.prolog import PrologRunner

runner = PrologRunner()
output = runner.run_program(r"""
:- table abuelo/2.

padre('Carlos', 'Juan').
padre('Juan', 'Esteban').

abuelo(X, Z) :- padre(X, Y), padre(Y, Z).

:- forall(abuelo(X, Z),
    format('~w es abuelo de ~w~n', [X, Z])).

% Agregar mas hechos y definir las relaciones bisabuelo, familiar y antepasado.
% COMPLETAR

:- halt.
""")

print(output)
