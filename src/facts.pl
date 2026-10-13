% fatos

% ======================================================
% MÉDICOS
% ======================================================
% medico(idM, nome, [espec]) -> exemplo

medico(m1, 'Roberto', [traumatologista]).

% ======================================================
% PERFIL
% ======================================================
% perfil(especialidade, criticidade, grupo, fatores) -> exemplo

perfil(traumatologista, alta, geral, 0.60).
perfil(emergencista, alta, geral, 0.60).
perfil(cardiologista, alta, idoso, 0.50).
perfil(intensivista, alta, geral, 0.30).
perfil(pediatra, baixa, crianca, 0.50).
perfil(geriatra, media, idoso, 0.70).
perfil(obstetra, media, gestante, 0.90).
perfil(clinico_geral, baixa, geral, 0.30).
perfil(gastroenterologista, baixa, idoso, 0.40).
perfil(fisiatra, media, deficiente, 0.80).

% tempo_base(criticidade, valor) -> exemplo
tempo_base(baixa, 30).
tempo_base(media, 60).
tempo_base(alta, 120).

% ======================================================
% PACIENTES
% ======================================================
% paciente(idP, nome, taxa_critica, [grupo_critico], horaEnt)-> exemplo

paciente(p1, 'Felipe', baixa, [geral] , 0).

% ======================================================
% PESOS
% ======================================================
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

% Proporção dada por uma escala de 60 min(1h) a 360 min(6h) indo na ordem crescente, onde o 360 min tem menor prioridade
% tempo_max_espera(criticidade, valor). -> exemplo

tempo_max_espera(alta, 60).
tempo_max_espera(media, 180).
tempo_max_espera(baixa, 360).