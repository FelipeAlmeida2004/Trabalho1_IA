:- encoding(utf8).
:- ensure_loaded('facts.pl').
:- use_module(library(lists), [member/2, memberchk/2, max_list/2, reverse/2]).
:- use_module(library(apply), [maplist/3]).

% Regras baseadas em docs/PEAS.md e nos fatos paciente/4 e medico/3.
%
% Formato do estado:
%   estado(Fila_Espera, Listas_Medicos)
%   Listas_Medicos = [fila(m1, [p5, p8, p3]), fila(m2, [...])]
%
% As consultas que recebem um estado pressupõem um estado concreto criado
% por estado_inicial/1 e pelas transições. Não se alteram os fatos na busca.

% ======================================================
% PRIORIDADE E LIMITE DE ATENDIMENTOS
% ======================================================

% Soma o peso do risco ao MAIOR peso entre os grupos do paciente.
% Exemplo: prioridade(p5, Prioridade). -> Prioridade = 7.
prioridade(Id_Paciente, Prioridade) :-
    paciente(Id_Paciente, _, Risco, Grupos),
    taxa_critica(Risco, Peso_Risco),
    maplist(grupo_critico, Grupos, Pesos_Grupos),
    max_list(Pesos_Grupos, Maior_Peso_Grupo),
    Prioridade is Peso_Risco + Maior_Peso_Grupo.

% L = max(limite_minimo, ceil(numero_pacientes / numero_medicos)).
% A conta inteira arredonda para cima sem usar ponto flutuante.
% Sem médicos, falha antes de tentar dividir por zero.
limite_atendimentos(Limite) :-
    findall(Id_Medico, medico(Id_Medico, _, _), Medicos),
    findall(Id_Paciente, paciente(Id_Paciente, _, _, _), Pacientes),
    length(Medicos, Numero_Medicos),
    length(Pacientes, Numero_Pacientes),
    Numero_Medicos > 0,
    limite_minimo(Minimo),
    Media_Arredondada is
        (Numero_Pacientes + Numero_Medicos - 1) // Numero_Medicos,
    Limite is max(Minimo, Media_Arredondada).

% ======================================================
% COMPATIBILIDADE
% ======================================================

% O médico tem uma especialidade NÃO generalista cujo perfil corresponde
% ao risco e a pelo menos um grupo do paciente. 'geral' não é um coringa.
% once/1 evita repetir o mesmo par se mais de um perfil for compatível.
especialista(Id_Paciente, Id_Medico) :-
    paciente(Id_Paciente, _, Risco, Grupos),
    medico(Id_Medico, _, EspecialidadesMedico),
    once((
        member(Especialidade, EspecialidadesMedico),
        \+ generalista(Especialidade),
        perfil(Especialidade, Risco, Grupo),
        memberchk(Grupo, Grupos)
    )).

medico_generalista(Id_Medico) :-
    medico(Id_Medico, _, EspecialidadesMedico),
    once((
        member(Especialidade, EspecialidadesMedico),
        generalista(Especialidade)
    )).

tem_vaga(Id_Medico, Listas_Medicos) :-
    member(fila(Id_Medico, Pacientes), Listas_Medicos),
    length(Pacientes, Quantidade),
    limite_atendimentos(Limite),
    Quantidade < Limite.

% Versão com duas entradas: consulta a compatibilidade no estado INICIAL.
% Para considerar especialistas que já ficaram cheios, use a versão /3.
compatibilidade(Id_Paciente, Id_Medico) :-
    estado_inicial(estado(_, Listas_Medicos)),
    compatibilidade(Id_Paciente, Id_Medico, Listas_Medicos).

% A compatibilidade depende da ocupação NO MOMENTO da atribuição.
% O médico atende como especialista; ou, se for generalista, atende apenas
% quando não existir especialista cadastrado com vaga para esse paciente.
% O perfil de clinico_geral não restringe esse atendimento de retaguarda.
compatibilidade(Id_Paciente, Id_Medico, Listas_Medicos) :-
    paciente(Id_Paciente, _, _, _),
    medico(Id_Medico, _, _),
    (   especialista(Id_Paciente, Id_Medico)
    ->  true
    ;   medico_generalista(Id_Medico),
        \+ (
            especialista(Id_Paciente, Id_Especialista),
            tem_vaga(Id_Especialista, Listas_Medicos)
        )
    ).

% Além da compatibilidade, o próprio médico precisa ter vaga.
pode_atender(Id_Paciente, Id_Medico, Listas_Medicos) :-
    compatibilidade(Id_Paciente, Id_Medico, Listas_Medicos),
    tem_vaga(Id_Medico, Listas_Medicos).

% ======================================================
% LISTAS ORDENADAS POR PRIORIDADE
% ======================================================

% Insere em ordem decrescente. Em empates, preserva a ordem de chegada.
inserir_por_prioridade(Id_Paciente, Lista, Nova_Lista) :-
    prioridade(Id_Paciente, Prioridade),
    inserir_com_prioridade(Id_Paciente, Prioridade, Lista, Nova_Lista).

inserir_com_prioridade(Id_Paciente, _, [], [Id_Paciente]).
inserir_com_prioridade(Id_Paciente, Prioridade, [Atual | Resto], Nova_Lista) :-
    prioridade(Atual, Prioridade_Atual),
    (   Prioridade > Prioridade_Atual
    ->  Nova_Lista = [Id_Paciente, Atual | Resto]
    ;   Nova_Lista = [Atual | Nova_Cauda],
        inserir_com_prioridade(Id_Paciente, Prioridade, Resto, Nova_Cauda)
    ).

% Atualiza somente a fila do médico escolhido, mantendo a ordem dos médicos.
atualizar_fila(Id_Paciente, Id_Medico,
               [fila(Id_Atual, Lista) | Resto], Novas_Listas) :-
    (   Id_Medico == Id_Atual
    ->  inserir_por_prioridade(Id_Paciente, Lista, Nova_Lista),
        Novas_Listas = [fila(Id_Atual, Nova_Lista) | Resto]
    ;   Novas_Listas = [fila(Id_Atual, Lista) | Nova_Cauda],
        atualizar_fila(Id_Paciente, Id_Medico, Resto, Nova_Cauda)
    ).

% ======================================================
% ESTADOS E TRANSIÇÕES
% ======================================================

% A fila de espera segue a ordem dos fatos paciente/4.
estado_inicial(estado(Fila_Espera, Listas_Medicos)) :-
    findall(Id_Paciente, paciente(Id_Paciente, _, _, _), Fila_Espera),
    findall(fila(Id_Medico, []), medico(Id_Medico, _, _), Listas_Medicos).

% Estados produzidos pelas transições já respeitam compatibilidade,
% capacidade e prioridade. O objetivo exige apenas esvaziar a espera.
estado_objetivo(estado([], _)).

% Cada ação atribui SOMENTE o primeiro paciente da espera.
% No backtracking, são tentados os outros médicos que podem recebê-lo.
transicao(estado([Id_Paciente | Espera], Listas_Medicos),
          atribuir(Id_Paciente, Id_Medico),
          estado(Espera, Novas_Listas)) :-
    pode_atender(Id_Paciente, Id_Medico, Listas_Medicos),
    atualizar_fila(Id_Paciente, Id_Medico, Listas_Medicos, Novas_Listas).

% ======================================================
% BUSCA EM LARGURA
% ======================================================

% Consultas principais:
%   resolver(Listas).
%   resolver(Listas, Acoes).
%   resolver(Listas, Acoes, estatisticas(Gerados, Expandidos)).
%
% Retorna a primeira solução encontrada, ou false se não houver solução.
% As ações ficam em ordem de execução; cada atribuição tem custo 1.
resolver(Listas_Medicos) :-
    resolver(Listas_Medicos, _, _).

resolver(Listas_Medicos, Acoes) :-
    resolver(Listas_Medicos, Acoes, _).

resolver(Listas_Medicos, Acoes, Estatisticas) :-
    estado_inicial(Inicial),
    once(busca_em_largura(
        [no(Inicial, [])], [], 1, 0,
        Final, Acoes_Invertidas, Estatisticas
    )),
    Final = estado([], Listas_Medicos),
    reverse(Acoes_Invertidas, Acoes).

% A fronteira é uma fila FIFO representada por duas listas:
% Frente: próximos nós a visitar; Tras: novos nós na ordem inversa.
% Isso evita percorrer toda a fronteira a cada inserção.
%
% Gerados inclui o estado inicial. Expandidos conta os nós cujos
% sucessores foram calculados; o objetivo encontrado não é expandido.
busca_em_largura([no(Estado, Caminho) | Frente], Tras,
                 Gerados, Expandidos, Final, Acoes, Estatisticas) :-
    (   estado_objetivo(Estado)
    ->  Final = Estado,
        Acoes = Caminho,
        Estatisticas = estatisticas(Gerados, Expandidos)
    ;   findall(
            no(Proximo, [Acao | Caminho]),
            transicao(Estado, Acao, Proximo),
            Sucessores
        ),
        enfileirar(Sucessores, Tras, Nova_Tras),
        length(Sucessores, Quantidade),
        Novos_Gerados is Gerados + Quantidade,
        Novos_Expandidos is Expandidos + 1,
        busca_em_largura(
            Frente, Nova_Tras, Novos_Gerados, Novos_Expandidos,
            Final, Acoes, Estatisticas
        )
    ).

busca_em_largura([], [No | Resto], Gerados, Expandidos,
                 Final, Acoes, Estatisticas) :-
    reverse([No | Resto], Frente),
    busca_em_largura(
        Frente, [], Gerados, Expandidos, Final, Acoes, Estatisticas
    ).

% Sem nós na frente e atrás, a busca falha: não existe solução.
% Não é preciso tratar ciclos: cada ação reduz a espera em um paciente.
enfileirar([], Tras, Tras).
enfileirar([No | Resto], Tras, Nova_Tras) :-
    enfileirar(Resto, [No | Tras], Nova_Tras).
