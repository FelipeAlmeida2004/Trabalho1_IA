% fatos

% ======================================================
% MÉDICOS
% ======================================================
% medico(idM, nome, [espec]) -> exemplo

medico(m1, 'Roberto', [clinico_geral]).
medico(m2, 'Marta', [pediatra, geriatra]).
% >>> gerado por integrate_pl.py
medico(m3, 'Gabriel', [cirurgiao_cardiovascular]).
medico(m4, 'Lia', [cirurgiao_craniomaxilofacial]).
medico(m5, 'Julia', [anatomopatologista]).
medico(m6, 'Olivia', [andrologista]).
medico(m7, 'Beatriz', [medico_do_trabalho]).
medico(m8, 'Lucas', [medico_do_sono]).
medico(m9, 'Renato', [endoscopista]).
medico(m10, 'Sergio', [ortopedista_de_ombro_e_cotovelo]).
% <<< fim do gerado

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
% >>> gerado por integrate_pl.py
perfil(acupunturista, baixa, idoso).
perfil(acupunturista, media, geral).
perfil(acupunturista, alta, deficiente).
perfil(adolescentologista, alta, gestante).
perfil(adolescentologista, alta, geral).
perfil(adolescentologista, baixa, idoso).
perfil(alergista, baixa, deficiente).
perfil(alergista, alta, geral).
perfil(alergista, alta, deficiente).
perfil(algologista, media, idoso).
perfil(algologista, media, deficiente).
perfil(anatomopatologista, alta, deficiente).
perfil(anatomopatologista, media, geral).
perfil(anatomopatologista, media, deficiente).
perfil(andrologista, media, crianca).
perfil(andrologista, baixa, gestante).
perfil(andrologista, alta, idoso).
perfil(anestesiologista, media, gestante).
perfil(angiologista, alta, deficiente).
perfil(angiologista, alta, crianca).
perfil(angiologista, media, gestante).
perfil(arritmologista, media, deficiente).
perfil(arritmologista, media, geral).
perfil(broncoscopista, alta, deficiente).
perfil(cardiologista, baixa, deficiente).
perfil(cardiologista, media, deficiente).
perfil(cardiologista, alta, crianca).
perfil(cardiologista_intervencionista, alta, crianca).
perfil(cardiologista_intervencionista, media, idoso).
perfil(cardiologista_pediatrico, alta, crianca).
perfil(cirurgiao_bariatrico, baixa, gestante).
perfil(cirurgiao_cardiovascular, baixa, geral).
perfil(cirurgiao_cardiovascular, alta, idoso).
perfil(cirurgiao_cardiovascular, media, geral).
perfil(cirurgiao_cardiovascular_pediatrico, baixa, deficiente).
perfil(cirurgiao_craniomaxilofacial, baixa, crianca).
perfil(cirurgiao_craniomaxilofacial, alta, crianca).
perfil(cirurgiao_craniomaxilofacial, alta, idoso).
perfil(cirurgiao_da_mao, baixa, idoso).
perfil(cirurgiao_da_mao, baixa, crianca).
perfil(cirurgiao_de_cabeca_e_pescoco, baixa, deficiente).
perfil(cirurgiao_de_cabeca_e_pescoco, media, crianca).
perfil(cirurgiao_de_coluna, alta, gestante).
perfil(cirurgiao_de_coluna, alta, geral).
perfil(cirurgiao_de_transplantes, alta, gestante).
perfil(cirurgiao_de_transplantes, alta, geral).
perfil(cirurgiao_de_transplantes, media, idoso).
perfil(cirurgiao_de_trauma, media, geral).
perfil(cirurgiao_dermatologico, baixa, idoso).
perfil(cirurgiao_do_aparelho_digestivo, media, crianca).
perfil(cirurgiao_do_aparelho_digestivo, baixa, deficiente).
perfil(cirurgiao_do_aparelho_digestivo, alta, gestante).
perfil(cirurgiao_endovascular, media, crianca).
perfil(cirurgiao_geral, baixa, gestante).
perfil(cirurgiao_hepatobiliar, alta, idoso).
perfil(cirurgiao_oculoplastico, media, deficiente).
perfil(cirurgiao_oculoplastico, alta, idoso).
perfil(cirurgiao_oncologico, baixa, geral).
perfil(cirurgiao_oncologico, baixa, idoso).
perfil(cirurgiao_pediatrico, baixa, geral).
perfil(cirurgiao_pediatrico, media, crianca).
perfil(cirurgiao_plastico, baixa, crianca).
perfil(cirurgiao_plastico, alta, idoso).
perfil(cirurgiao_plastico, alta, crianca).
perfil(cirurgiao_toracico, baixa, gestante).
perfil(cirurgiao_vascular, alta, gestante).
perfil(cirurgiao_vascular, alta, deficiente).
perfil(cirurgiao_vascular, media, gestante).
perfil(citopatologista, baixa, gestante).
perfil(clinico_geral, baixa, gestante).
perfil(coloproctologista, media, crianca).
perfil(coloproctologista, alta, idoso).
perfil(coloproctologista, media, gestante).
perfil(dermatologista, baixa, gestante).
perfil(dermatologista_pediatrico, media, gestante).
perfil(dermatopatologista, media, idoso).
perfil(dermatopatologista, alta, deficiente).
perfil(dermatopatologista, media, crianca).
perfil(ecocardiografista, alta, deficiente).
perfil(ecocardiografista, baixa, idoso).
perfil(eletrofisiologista, alta, crianca).
perfil(eletrofisiologista, media, gestante).
perfil(emergencista_pediatrico, alta, deficiente).
perfil(endocrinologista, baixa, deficiente).
perfil(endocrinologista, media, deficiente).
perfil(endocrinologista_pediatrico, media, crianca).
perfil(endoscopista, baixa, idoso).
perfil(endoscopista_digestivo, baixa, geral).
perfil(endoscopista_digestivo, alta, geral).
perfil(endoscopista_digestivo, media, crianca).
perfil(epidemiologista, baixa, idoso).
perfil(epidemiologista, baixa, deficiente).
perfil(epileptologista, media, crianca).
perfil(especialista_em_reproducao_humana, alta, crianca).
perfil(especialista_em_reproducao_humana, alta, idoso).
perfil(especialista_em_reproducao_humana, alta, deficiente).
perfil(estrabologista, media, geral).
perfil(estrabologista, alta, idoso).
perfil(estrabologista, baixa, geral).
perfil(fisiatra, baixa, gestante).
perfil(fisiatra, alta, idoso).
perfil(fisiatra, baixa, crianca).
perfil(foniatra, baixa, crianca).
perfil(gastroenterologista, alta, gestante).
perfil(gastroenterologista_pediatrico, baixa, idoso).
perfil(gastroenterologista_pediatrico, media, crianca).
perfil(geneticista, baixa, geral).
perfil(geneticista, alta, deficiente).
perfil(geneticista, baixa, idoso).
perfil(geriatra, baixa, gestante).
perfil(geriatra, baixa, crianca).
perfil(ginecologista, alta, crianca).
perfil(ginecologista, alta, deficiente).
perfil(ginecologista_oncologico, media, geral).
perfil(ginecologista_oncologico, alta, idoso).
perfil(glaucomatologista, media, geral).
perfil(hematologista, baixa, idoso).
perfil(hematologista, alta, idoso).
perfil(hematologista_pediatrico, alta, geral).
perfil(hemodinamicista, media, crianca).
perfil(hemoterapeuta, alta, gestante).
perfil(hemoterapeuta, media, deficiente).
perfil(hepatologista, media, geral).
perfil(homeopata, media, geral).
perfil(imunologista, baixa, idoso).
perfil(imunologista, baixa, deficiente).
perfil(infectologista, alta, deficiente).
perfil(infectologista, media, geral).
perfil(infectologista, baixa, deficiente).
perfil(infectologista_pediatrico, baixa, deficiente).
perfil(infectologista_pediatrico, alta, idoso).
perfil(infectologista_pediatrico, alta, geral).
perfil(intensivista, alta, crianca).
perfil(intensivista_pediatrico, baixa, gestante).
perfil(intensivista_pediatrico, baixa, geral).
perfil(intensivista_pediatrico, alta, crianca).
perfil(laringologista, media, crianca).
perfil(laringologista, baixa, geral).
perfil(laringologista, alta, gestante).
perfil(mastologista, baixa, deficiente).
perfil(mastologista, alta, crianca).
perfil(medico_aeroespacial, media, crianca).
perfil(medico_de_familia, media, idoso).
perfil(medico_de_familia, media, deficiente).
perfil(medico_de_familia, baixa, geral).
perfil(medico_de_trafego, baixa, geral).
perfil(medico_de_trafego, alta, geral).
perfil(medico_do_esporte, baixa, crianca).
perfil(medico_do_sono, media, crianca).
perfil(medico_do_trabalho, media, crianca).
perfil(medico_do_trabalho, media, geral).
perfil(medico_fetal, media, gestante).
perfil(medico_fetal, baixa, deficiente).
perfil(medico_fetal, baixa, idoso).
perfil(medico_hiperbarico, alta, idoso).
perfil(medico_hiperbarico, baixa, idoso).
perfil(medico_legista, alta, crianca).
perfil(medico_nuclear, baixa, geral).
perfil(medico_perito, media, idoso).
perfil(medico_perito, alta, gestante).
perfil(medico_perito, media, crianca).
perfil(nefrologista, media, crianca).
perfil(nefrologista_pediatrico, baixa, idoso).
perfil(neonatologista, baixa, crianca).
perfil(neonatologista, baixa, geral).
perfil(neurocirurgiao, alta, gestante).
perfil(neurocirurgiao, baixa, deficiente).
perfil(neurocirurgiao, baixa, geral).
perfil(neurocirurgiao_funcional, alta, gestante).
perfil(neurocirurgiao_funcional, baixa, deficiente).
perfil(neurocirurgiao_pediatrico, alta, deficiente).
perfil(neurocirurgiao_pediatrico, media, deficiente).
perfil(neurofisiologista_clinico, media, crianca).
perfil(neurologista, alta, deficiente).
perfil(neurologista_pediatrico, media, deficiente).
perfil(neurologista_pediatrico, alta, idoso).
perfil(neurologista_pediatrico, media, idoso).
perfil(neurologista_vascular, media, crianca).
perfil(neurologista_vascular, baixa, gestante).
perfil(neurooftalmologista, media, crianca).
perfil(neurooftalmologista, baixa, idoso).
perfil(neurorradiologista, baixa, deficiente).
perfil(neurorradiologista, alta, gestante).
perfil(nutrologo, alta, crianca).
perfil(nutrologo, baixa, crianca).
perfil(obstetra, alta, crianca).
perfil(oftalmologista, alta, geral).
perfil(oftalmologista, baixa, crianca).
perfil(oftalmologista_pediatrico, alta, crianca).
perfil(oftalmologista_pediatrico, alta, geral).
perfil(oftalmologista_pediatrico, baixa, crianca).
perfil(oncologista_clinico, alta, deficiente).
perfil(oncologista_pediatrico, baixa, crianca).
perfil(oncologista_pediatrico, baixa, geral).
perfil(ortopedista, baixa, idoso).
perfil(ortopedista_de_joelho, alta, idoso).
perfil(ortopedista_de_ombro_e_cotovelo, media, idoso).
perfil(ortopedista_de_ombro_e_cotovelo, alta, deficiente).
perfil(ortopedista_de_ombro_e_cotovelo, baixa, crianca).
perfil(ortopedista_de_pe_e_tornozelo, alta, gestante).
perfil(ortopedista_de_pe_e_tornozelo, media, crianca).
perfil(ortopedista_de_pe_e_tornozelo, baixa, crianca).
perfil(ortopedista_de_quadril, baixa, geral).
perfil(ortopedista_oncologico, baixa, idoso).
perfil(ortopedista_oncologico, alta, crianca).
perfil(ortopedista_pediatrico, alta, geral).
perfil(otologista, alta, idoso).
perfil(otorrinolaringologista, alta, idoso).
perfil(otorrinolaringologista, media, idoso).
perfil(otorrinolaringologista, baixa, deficiente).
perfil(otorrinolaringologista_pediatrico, alta, gestante).
perfil(otorrinolaringologista_pediatrico, media, crianca).
perfil(paliativista, media, deficiente).
perfil(patologista, baixa, deficiente).
perfil(patologista_clinico, baixa, crianca).
perfil(pediatra, baixa, crianca).
perfil(pediatra, media, gestante).
perfil(pneumologista, media, deficiente).
perfil(pneumologista, media, idoso).
perfil(pneumologista, alta, deficiente).
perfil(pneumologista_pediatrico, media, deficiente).
perfil(pneumologista_pediatrico, baixa, deficiente).
perfil(pneumologista_pediatrico, media, gestante).
perfil(psicogeriatra, baixa, crianca).
perfil(psiquiatra, baixa, idoso).
perfil(psiquiatra, media, deficiente).
perfil(psiquiatra, baixa, gestante).
perfil(psiquiatra_da_infancia_e_adolescencia, alta, crianca).
perfil(psiquiatra_da_infancia_e_adolescencia, media, crianca).
perfil(psiquiatra_da_infancia_e_adolescencia, media, idoso).
perfil(psiquiatra_forense, baixa, deficiente).
perfil(psiquiatra_forense, media, crianca).
perfil(radiologista, media, gestante).
perfil(radiologista_intervencionista, baixa, crianca).
perfil(radiologista_intervencionista, alta, deficiente).
perfil(radiologista_pediatrico, media, deficiente).
perfil(radiologista_pediatrico, baixa, gestante).
perfil(radiologista_pediatrico, alta, deficiente).
perfil(radioterapeuta, baixa, deficiente).
perfil(radioterapeuta, media, idoso).
perfil(retinologista, media, deficiente).
perfil(retinologista, media, crianca).
perfil(reumatologista, media, crianca).
perfil(reumatologista, alta, geral).
perfil(reumatologista_pediatrico, baixa, crianca).
perfil(reumatologista_pediatrico, alta, crianca).
perfil(rinologista, alta, idoso).
perfil(sanitarista, alta, deficiente).
perfil(toxicologista, baixa, deficiente).
perfil(toxicologista, baixa, geral).
perfil(ultrassonografista, baixa, gestante).
perfil(ultrassonografista, baixa, geral).
perfil(uroginecologista, media, gestante).
perfil(urologista, media, geral).
perfil(urologista, media, deficiente).
perfil(urologista_oncologico, alta, gestante).
perfil(urologista_oncologico, alta, idoso).
perfil(urologista_pediatrico, baixa, gestante).
perfil(urologista_pediatrico, baixa, crianca).
perfil(urologista_pediatrico, media, deficiente).
% <<< fim do gerado

% ======================================================
% PACIENTES
% ======================================================
% 'geral' é o grupo de quem não tem condição especial e nunca aparece junto
% de outro grupo na lista.
% paciente(idP, nome, taxa_critica, [grupo_critico]) -> exemplo

paciente(p1, 'Ana', baixa, [crianca]).
paciente(p2, 'Carlos', media, [idoso]).
% >>> gerado por integrate_pl.py
paciente(p3, 'Renato', alta, [geral]).
paciente(p4, 'Nicolas', alta, [geral]).
paciente(p5, 'Vanessa', baixa, [crianca]).
paciente(p6, 'Eduardo', baixa, [deficiente]).
paciente(p7, 'Beatriz', baixa, [idoso]).
paciente(p8, 'Igor', alta, [geral]).
paciente(p9, 'Pedro', alta, [gestante]).
paciente(p10, 'Julia', alta, [idoso]).
% <<< fim do gerado

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
