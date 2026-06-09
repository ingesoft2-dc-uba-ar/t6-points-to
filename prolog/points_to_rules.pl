%% Reglas de Points-To Analysis
%% ============================
%%
%% Relaciones:
%%   points_to(X, O)       - la variable X apunta al objeto O
%%   heap_field(O1, F, O2) - el campo F del objeto O1 apunta al objeto O2
%%
%% Hechos (provistos por el análisis):
%%   new(X, O)             - X = new Obj()
%%   assign(X, Y)          - X = Y
%%   store(X, F, Y)        - X.F = Y
%%   load(X, Y, F)         - X = Y.F

:- table points_to/2.
:- table heap_field/3.

% Regla 1: si X = new O, entonces X apunta a O (dado)
points_to(X, O) :- new(X, O).

% Regla 3: si X.F = Y (store), y X apunta a O1, e Y apunta a O2,
%           entonces el campo F de O1 apunta a O2
heap_field(O1, F, O2) :- store(X, F, Y). % COMPLETAR (incompleto!)

% Regla 2: COMPLETAR
% Pista: si X = Y (assign), y Y apunta a O, entonces X apunta a O.

% Regla 4: COMPLETAR
% Pista: si X = Y.F (load), y Y apunta a O1, y el campo F de O1 apunta a O,
%         entonces X apunta a O.
