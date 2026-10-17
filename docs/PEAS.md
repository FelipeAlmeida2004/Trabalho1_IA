# PEAS — Escalonamento de pacientes em um hospital

## Agente

Agente de triagem e distribuição hospitalar, baseado em objetivo. Parte de uma fila de espera com todos os pacientes e médicos sem pacientes atribuídos, e modifica esse estado por busca cega até obter uma distribuição válida, com a lista ordenada de pacientes de cada médico.

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
- **Pacientes**, cada um com um nível de risco (`baixa`, `media`, `alta`) e uma lista de grupos de prioridade (`idoso`, `crianca`, `gestante`, `deficiente`, ou `geral` quando não há condição especial).
- **Fila de espera inicial** com todos os pacientes e médicos com as listas vazias.
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
- **Exibir** a lista ordenada de cada médico quando o estado válido é alcançado.

## S — Sensores

O agente lê a base de fatos e o estado corrente:

- Médicos, suas especialidades e a marcação de quem é generalista.
- Perfis das especialidades (risco e grupo atendidos).
- Pacientes, com risco e grupos.
- Tabelas de peso de risco e de grupo.
- O limite de atendimentos.
- O estado atual: fila de espera e lista de cada médico.

## Formulação do problema de busca

| Elemento | Definição |
|---|---|
| **Estado** | A fila de espera e, para cada médico, a lista ordenada dos pacientes atribuídos a ele |
| **Estado inicial** | Fila de espera com todos os pacientes; a lista de cada médico vazia |
| **Ações** | Atribuir o primeiro paciente da fila de espera a um médico que (a) seja compatível e (b) tenha menos pacientes que o limite |
| **Modelo de transição** | O paciente sai da fila de espera e entra na lista do médico, na posição que preserva a ordem de prioridade |
| **Teste de objetivo** | A fila de espera está vazia |
| **Custo de passo** | 1 por atribuição (busca cega: nenhum custo ou heurística guia a busca) |
| **Solução** | A sequência de atribuições, que resulta na lista de cada médico |

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
L = max(5, ceil(numero_de_pacientes / numero_de_medicos))
```

## Premissas e decisões em aberto

- O tempo de atendimento, a hora de entrada e o tempo máximo de espera não são modelados neste trabalho.
- A estratégia de busca (em largura ou em profundidade) ainda precisa ser escolhida.
- A fórmula do limite `L` é a proposta atual e pode ser substituída por um valor fixo.
- Se não há distribuição válida (por exemplo, mais pacientes do que a soma das capacidades), a busca esgota os estados e termina sem solução.
