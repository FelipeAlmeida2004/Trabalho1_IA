:- encoding(utf8).
:- dynamic medico/3, paciente/4, limite_minimo/1.
:- ensure_loaded('rules.pl').
:- use_module(library(apply), [maplist/2]).
:- use_module(library(time), [call_with_time_limit/2]).
:- ensure_loaded('scenario_generation.pl').

% Entrada do Janus: listas Python são listas Prolog, e strings viram átomos.
% Medicos = [[Id, [Especialidades]], ...]
% Pacientes = [[Id, Risco, [Grupos]], ...]
% Cada quadro devolvido contém o estado exato após uma atribuição.
resolver_interface(Medicos, Pacientes, Limite, Quadros, Gerados, Expandidos) :-
    snapshot((
        retractall(medico(_, _, _)),
        retractall(paciente(_, _, _, _)),
        retractall(limite_minimo(_)),
        assertz(limite_minimo(Limite)),
        maplist(cadastrar_medico_interface, Medicos),
        maplist(cadastrar_paciente_interface, Pacientes),
        limite_atendimentos(Limite),
        resolver(_, Acoes, estatisticas(Gerados, Expandidos)),
        estado_inicial(Inicial),
        quadros_da_solucao(Acoes, Inicial, Quadros)
    )).

% snapshot/1 descarta as alterações ao terminar, inclusive se houver falha
% ou exceção. Os fatos de referência no disco e na memória são preservados.
cadastrar_medico_interface([Id, Especialidades]) :-
    assertz(medico(Id, Id, Especialidades)).

cadastrar_paciente_interface([Id, Risco, Grupos]) :-
    assertz(paciente(Id, Id, Risco, Grupos)).

quadros_da_solucao([], _, []).
quadros_da_solucao([Acao | Acoes], Estado, [Quadro | Quadros]) :-
    once(transicao(Estado, Acao, Proximo)),
    Acao = atribuir(Id_Paciente, Id_Medico),
    Proximo = estado(Espera, Filas),
    findall([Id, Pacientes], member(fila(Id, Pacientes), Filas), Listas),
    Quadro = _{
        paciente: Id_Paciente,
        medico: Id_Medico,
        espera: Espera,
        filas: Listas
    },
    quadros_da_solucao(Acoes, Proximo, Quadros).
