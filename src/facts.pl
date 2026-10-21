% fatos

% ======================================================
% MÉDICOS
% ======================================================
% medico(idM, nome, [espec]) -> exemplo

medico(m1, 'Roberto', [clinico_geral]).
medico(m2, 'Marta', [pediatra, geriatra]).

% Especialidade de atendimento geral: só atende pacientes que não têm
% especialista cadastrado, ou cujos especialistas já estão no limite.
% generalista(espec) -> exemplo

generalista(clinico_geral).

% ======================================================
% PERFIL
% ======================================================
% Quais combinações de risco e grupo cada especialidade atende.
% perfil(especialidade, criticidade, grupo) -> exemplo

perfil(traumatologista, alta, geral).
perfil(emergencista, alta, geral).
perfil(cardiologista, alta, idoso).
perfil(intensivista, alta, geral).
perfil(pediatra, baixa, crianca).
perfil(geriatra, media, idoso).
perfil(obstetra, media, gestante).
perfil(clinico_geral, baixa, geral).
perfil(gastroenterologista, baixa, idoso).
perfil(fisiatra, media, deficiente).

% ======================================================
% PACIENTES
% ======================================================
% 'geral' é o grupo de quem não tem condição especial e nunca aparece junto
% de outro grupo na lista.
% paciente(idP, nome, taxa_critica, [grupo_critico]) -> exemplo

paciente(p1, 'Ana', baixa, [crianca]).
paciente(p2, 'Carlos', media, [idoso]).
paciente(p3, 'Felipe', baixa, [geral]).
paciente(p4, 'Bruno', baixa, [crianca]).
paciente(p5, 'Julia', media, [gestante]).
paciente(p6, 'Dona Rita', media, [idoso]).
paciente(p7, 'Pedro', baixa, [crianca]).
paciente(p8, 'Lia', baixa, [crianca]).

% ======================================================
% PESOS
% ======================================================
% A prioridade de um paciente é o peso do risco somado ao MAIOR peso entre
% os seus grupos.

% Proporção dada por uma escala de 1 a 3 indo na ordem crescente, onde o 3 tem maior prioridade
% taxa_critica(criticidade, valor) -> exemplo

taxa_critica(baixa, 1).
taxa_critica(media, 2).
taxa_critica(alta, 3).

% Proporção dada por uma escala de 1 a 5 indo na ordem crescente, onde o 5 tem maior prioridade
% grupo_critico(criticidade, valor). -> exemplo

grupo_critico(geral, 1).
grupo_critico(deficiente, 2).
grupo_critico(idoso, 3).
grupo_critico(crianca, 4).
grupo_critico(gestante, 5).

% ======================================================
% LIMITE DE ATENDIMENTOS
% ======================================================
% Cada médico atende um paciente por vez e no máximo L pacientes, com
%   L = max(limite_minimo, ceil(numero_de_pacientes / numero_de_medicos)).
% limite_minimo(valor) -> exemplo

limite_minimo(5).
