# PEAS — Escalonamento de pacientes em um hospital

## Agente

Agente de triagem e distribuição hospitalar, baseado em objetivo. O problema se comporta como um cubo mágico: parte-se de um estado inicial **inválido** (todos os pacientes na fila de espera e a lista de cada médico vazia) e o estado é modificado, passo a passo e por busca cega, até se chegar a um estado **válido**, com a lista ordenada de pacientes de cada médico.

## P — Medida de desempenho

Uma solução é boa quando é **válida**. Todas as condições abaixo devem valer:

1. **Completude:** todos os pacientes foram atribuídos (a fila de espera termina vazia).
2. **Capacidade:** nenhum médico tem mais pacientes que o limite de atendimentos.
3. **Compatibilidade:** cada paciente está com um médico adequado:
   - **especialista:** o médico tem uma especialidade com perfil para o risco e para algum grupo do paciente;
   - **generalista:** só atende o paciente se nenhum médico cadastrado é especialista dele, ou se todos os especialistas dele já estão no limite.
4. **Prioridade:** em cada lista, nenhum paciente aparece depois de outro de prioridade menor. Pacientes de prioridade igual podem aparecer em qualquer ordem.

Critérios secundários:

- **Escalabilidade:** o mesmo conjunto de regras funciona para N médicos e M pacientes, apenas cadastrando novos fatos.
- **Eficiência da busca:** número de estados gerados e expandidos até encontrar a primeira solução.

## E — Ambiente

Um hospital com:

- **Médicos** (inicialmente 2, mas em quantidade arbitrária), cada um com uma ou mais especialidades. Uma especialidade pode ser marcada como de atendimento geral.
- **Pacientes**, cada um com um nível de risco (`baixa`, `media`, `alta`) e uma lista de grupos de prioridade (`idoso`, `crianca`, `gestante`, `deficiente`, ou `geral` quando não há condição especial; `geral` nunca aparece junto de outro grupo).
- **Fila de espera inicial** com todos os pacientes, na ordem em que foram cadastrados, e médicos com as listas vazias.
- **Regra de atendimento:** cada médico atende um paciente por vez, na ordem da sua lista, e no máximo `L` pacientes.

Propriedades do ambiente:

| Propriedade | Classificação | Justificativa |
|---|---|---|
| Observabilidade | Totalmente observável | Todo o estado (fila de espera e listas) é conhecido |
| Determinismo | Determinístico | Cada ação tem um único resultado |
| Dinamismo | Estático | Não chegam pacientes durante a busca e o tempo não é modelado |
| Discretização | Discreto | Conjuntos finitos de estados e ações |
| Agentes | Agente único | Não há competição ou cooperação com outros agentes |
| Episódios | Sequencial | Uma atribuição altera a capacidade disponível para as seguintes |

## A — Atuadores

- **Atribuir** o primeiro paciente da fila de espera a um médico compatível com vaga, inserindo-o na posição que mantém a lista em ordem de prioridade.
- **Exibir** a lista ordenada de cada médico quando o estado válido é alcançado (tela 2D em Arcade: fila de espera à esquerda e uma linha de vagas por médico).

## S — Sensores

O agente lê a base de fatos (`src/facts.pl`) e o estado corrente:

| Fato | Conteúdo |
|---|---|
| `medico(idM, nome, [espec])` | Médicos e suas especialidades |
| `generalista(espec)` | Especialidades de atendimento geral |
| `perfil(espec, risco, grupo)` | Combinações de risco e grupo que cada especialidade atende |
| `paciente(idP, nome, risco, [grupos])` | Pacientes, na ordem da fila de espera |
| `taxa_critica(risco, peso)` | Peso de cada risco |
| `grupo_critico(grupo, peso)` | Peso de cada grupo |
| `limite_minimo(valor)` | Valor mínimo do limite de atendimentos |

E também o estado atual: a fila de espera e a lista de cada médico.

## Formulação do problema de busca

| Elemento | Definição |
|---|---|
| **Estado** | A fila de espera e, para cada médico, a lista ordenada dos pacientes atribuídos a ele. A ordem de cada lista faz parte do estado: os mesmos pacientes em ordens diferentes são estados diferentes |
| **Estado inicial** | Fila de espera com todos os pacientes; a lista de cada médico vazia (estado inválido) |
| **Ações** | Atribuir o primeiro paciente da fila de espera a um médico que (a) seja compatível e (b) tenha menos pacientes que o limite |
| **Modelo de transição** | O paciente sai da fila de espera e entra na lista do médico, na posição que preserva a ordem de prioridade |
| **Teste de objetivo** | A fila de espera está vazia |
| **Custo de passo** | 1 por atribuição (busca cega: nenhum custo ou heurística guia a busca) |
| **Estratégia de busca** | Busca em largura: expande todos os estados de um nível antes de passar ao seguinte. Como cada ação atribui um paciente, toda solução está no nível igual ao número de pacientes |
| **Solução** | A sequência de atribuições, que resulta na lista de cada médico |

A compatibilidade e o limite são verificados **na ação**: uma atribuição inválida nunca gera um estado, então todo estado alcançado já respeita as regras e o teste de objetivo só precisa conferir que a fila de espera esvaziou.

## Analogia com o cubo mágico

| Cubo mágico | Hospital |
|---|---|
| Cubo embaralhado | Fila de espera cheia e médicos sem pacientes |
| Giro de uma face | Atribuição de um paciente a um médico |
| Desfazer um giro | Retrocesso (backtracking) para tentar outro médico |
| Cubo resolvido | Fila vazia e listas válidas e ordenadas |
| Busca cega | Nenhuma heurística ou custo guia a escolha das ações (busca em largura) |

Diferença em relação ao cubo: lá existe um único estado final, aqui existem vários estados válidos (por exemplo, pacientes de mesma prioridade podem trocar de posição). A busca para no primeiro que encontrar.

## Definições auxiliares

**Prioridade de um paciente**

```
prioridade(paciente) = peso_risco(risco) + max(peso_grupo(g) para g em grupos)
```

| Risco | Peso | Grupo | Peso |
|---|---|---|---|
| `baixa` | 1 | `geral` | 1 |
| `media` | 2 | `deficiente` | 2 |
| `alta` | 3 | `idoso` | 3 |
| | | `crianca` | 4 |
| | | `gestante` | 5 |

**Compatibilidade médico–paciente.** Um médico pode receber um paciente se:

- ele é **especialista** do paciente; ou
- ele é **generalista** e (não existe médico especialista do paciente no cenário, ou todos os especialistas do paciente estão com `L` pacientes).

**Limite de atendimentos `L`.** Parâmetro do cenário, com mínimo de 5 e crescimento conforme o tamanho do problema:

```
L = max(limite_minimo, ceil(numero_de_pacientes / numero_de_medicos))
```

## Cenário de referência

### Geração dos cenários da interface

O cenário de referência abaixo continua definido nos fatos. A interface gera
outros cenários, com as quantidades escolhidas pelo usuário, garantindo que cada
um tenha pelo menos uma sequência válida de atribuições.

As especialidades são sorteadas entre as cadastradas em `perfil/3`. Durante a
construção, cada novo paciente é sorteado apenas entre os perfis que algum médico
pode receber com a ocupação temporária atual. Essa ocupação é atualizada para a
próxima escolha, respeitando a regra do generalista e o limite final `L`.

Ao terminar, a ocupação de construção é descartada: todos os pacientes aparecem
na espera e as filas dos médicos começam vazias. A busca em largura continua
responsável pela solução; ela não recebe a sequência usada na construção.

O sorteio padrão usa uma nova semente a cada cenário. Uma semente explícita
permite reproduzir o mesmo caso para testes. A garantia vale para a geração;
dados externos podem continuar sendo inviáveis, e tempo excedido de busca é
tratado separadamente de ausência de solução.

### Dados de referência

2 médicos (`m1` generalista com `clinico_geral`; `m2` com `pediatra` e `geriatra`) e 8 pacientes, `L = 5`.

| Paciente | Risco | Grupos | Prioridade | Quem atende |
|---|---|---|---|---|
| p1 | `baixa` | `[crianca]` | 5 | m2 |
| p2 | `media` | `[idoso]` | 5 | m2 |
| p3 | `baixa` | `[geral]` | 2 | m1 |
| p4 | `baixa` | `[crianca]` | 5 | m2 |
| p5 | `media` | `[gestante]` | 7 | m1 (nenhum obstetra cadastrado) |
| p6 | `media` | `[idoso]` | 5 | m2 |
| p7 | `baixa` | `[crianca]` | 5 | m2 |
| p8 | `baixa` | `[crianca]` | 5 | m2 cheio, vai para m1 |

Resultado esperado, com os pacientes saindo da fila de espera na ordem p1 a p8:

- `m1`: `[p5, p8, p3]`
- `m2`: `p1, p2, p4, p6, p7`, em qualquer ordem (todos com prioridade 5)

Com `L = 6`, m2 comportaria p8 e m1 ficaria só com `[p5, p3]`. Com `L = 4`, p7 e p8 transbordam para m1.

## Premissas e decisões

Decididas:

- O tempo de atendimento, a hora de entrada e o tempo máximo de espera não são modelados neste trabalho.
- O generalista é verificado no momento da ação, e não no teste de objetivo.
- Pacientes de prioridade igual podem ficar em qualquer ordem.
- O grupo `geral` é exclusivo e não funciona como coringa nos perfis.
- A estratégia de busca é a busca em largura.
- A ordem dos pacientes na lista de cada médico importa: ela é exigida pela prioridade e faz parte do estado.
- A ordem inicial da fila de espera não importa: ela segue a ordem dos fatos `paciente/4` e qualquer ordem é aceita. Como a regra do generalista depende de quem já foi atribuído, essa ordem pode mudar quem transborda para o generalista, mas toda distribuição válida é uma resposta correta.

Em aberto:

- A fórmula do limite `L` é a proposta atual e pode ser substituída por um valor fixo.
- Se não há distribuição válida (por exemplo, mais pacientes do que a soma das capacidades), a busca esgota os estados e termina sem solução.
