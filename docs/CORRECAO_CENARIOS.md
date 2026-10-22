# Por que tantos cenários não tinham solução

O gerador anterior sorteava as especialidades dos médicos, os riscos e os grupos
dos pacientes de forma independente. As regras Prolog exigem que uma
especialidade tenha um `perfil(Especialidade, Risco, Grupo)` compatível com o
risco e com ao menos um dos grupos do paciente.

Quando nenhum especialista pode atender um paciente, ele depende do generalista.
Mas esse médico tem o mesmo limite de atendimentos que os demais. A fórmula
`L = max(5, ceil(pacientes / medicos))` garante capacidade total suficiente;
ela não garante capacidade suficiente em cada perfil de atendimento.

## O que acontecia na configuração padrão

Com a antiga semente 7, a interface criava um generalista e um médico com
`cardiologista` e `obstetra`. Esses perfis atendem, respectivamente, risco alto
com grupo idoso e risco médio com grupo gestante. Nenhum dos oito pacientes
sorteados correspondia a eles.

| Recurso | Capacidade utilizável para esses oito pacientes |
|---|---:|
| Generalista | 5 |
| Cardiologista/obstetra | 0 |
| Pacientes que precisavam ser atribuídos | 8 |

Nesse caso, atribuir todos é impossível: três pacientes ficam sem capacidade
compatível. A prioridade apenas ordena as filas; ela não cria capacidade nem
altera a compatibilidade dos médicos.

Foram executadas 200 sementes de 0 a 199 com 2 médicos e 8 pacientes no código
anterior. O SWI-Prolog confirmou ausência de solução em 182 casos, ou 91% dessa
amostra. Além disso, a semente fixa fazia a mesma configuração repetir o cenário
ao reiniciar.

## Correção implementada

1. As especialidades vêm do catálogo real de `perfil/3` em `facts.pl`.
2. Calcula-se o limite final a partir das quantidades escolhidas.
3. Para cada novo paciente, o gerador enumera riscos e grupos conhecidos e usa
   `pode_atender/3` para identificar escolhas que algum médico com vaga pode
   receber na ocupação de construção.
4. Sorteia-se uma dessas escolhas e atualiza-se essa ocupação temporária.
5. Ao concluir a construção, a ocupação é descartada. A interface exibe todos
   os pacientes na espera e os médicos sem pacientes.
6. Ao clicar em RESOLVER, a busca em largura calcula a sequência de atribuições
   independentemente da construção. A animação usa os estados devolvidos pelo
   Prolog.

O uso de `snapshot/1` mantém intactos os fatos de referência. A semente é nova a
cada cenário; `build_scenario(..., seed=7)` permite reprodução determinística.

Essa é uma geração aleatória condicionada à viabilidade: a distribuição dos
perfis passa a depender dos médicos e das vagas disponíveis. As regras de
compatibilidade, o limite por médico, a prioridade e a busca em largura mantêm
seus significados.

## Por que a construção tem solução

Cada inclusão tem uma atribuição legal sob as mesmas regras da busca. A cada
passo, a ocupação continua respeitando o limite. Um especialista cadastrado possui
ao menos um perfil válido; enquanto ele tiver vaga, existe um paciente candidato
compatível. Se somente o generalista tiver vaga, nenhum especialista disponível
impede esse atendimento.

Como `numero_medicos * L >= numero_pacientes`, a capacidade não se esgota antes
de concluir a construção. Assim, a sequência temporária é uma testemunha de
que pelo menos uma solução existe para a ordem gerada. Essa testemunha não é
guardada nem fornecida à busca.

## Verificação

Os 12 testes de regressão incluem:

- As 300 combinações selecionáveis na interface, usando a semente 7.
- As mesmas 200 sementes da comparação anterior, com 2 médicos e 8 pacientes.
- Mais 60 cenários de 30 pacientes, com 3, 5 e 10 médicos e 20 sementes por tamanho.
- Verificação de cada ação quanto à compatibilidade, capacidade, regra do
  generalista, ordem de retirada da espera e prioridade das filas.
- Verificação de completude e ausência de duplicações.
- Reprodução por semente, leitura do catálogo real e preservação dos fatos.
- Controle negativo com dados manualmente inviáveis, que continuam rejeitados.

Os 560 cenários dos três primeiros grupos tiveram solução. Nos 200 casos
comparáveis, a ausência de solução passou de 182 para zero.

Para executar:

```bash
poetry run python -m unittest discover -s tests -v
```

A garantia de existência se aplica aos cenários gerados. Dados inseridos
manualmente podem violar a cobertura. O limite de 15 segundos da busca continua
existindo: uma busca interrompida por tempo excedido não prova ausência de
solução, e a interface mantém essas situações distintas.
