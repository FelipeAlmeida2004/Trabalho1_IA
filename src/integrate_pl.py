import itertools
import json
import random
import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
INFO = PASTA / 'info.json'
FACTS = PASTA / 'facts.pl'

MARCA_INICIO = '% >>> gerado por integrate_pl.py'
MARCA_FIM = '% <<< fim do gerado'

USO = ('uso: python src/integrate_pl.py MEDICOS PACIENTES [SEMENTE]\n'
       '     python src/integrate_pl.py limpar')

GRUPO_GERAL = 'geral'
ESPECIALIDADE_GERAL = 'clinico_geral'

NOMES = (
    'Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gabriel',
    'Helena', 'Igor', 'Julia', 'Lucas', 'Marta', 'Nicolas', 'Olivia', 'Pedro',
    'Rafaela', 'Sergio', 'Tatiana', 'Vitor', 'Yasmin', 'Roberto', 'Lia',
    'Felipe', 'Beatriz', 'Caio', 'Larissa', 'Mateus', 'Paula', 'Renato',
    'Sofia', 'Thiago', 'Vanessa', 'Dona Rita', 'Seu Antonio',
)

dados = json.loads(INFO.read_text(encoding='utf-8'))
ESPECIALIDADES = dados['especialidades']
GRUPOS = [nome for item in dados['grupos'] for nome in item]
RISCOS = [nome for item in dados['cricidade'] for nome in item]


def sortear_nomes(rng, quantidade):
    if quantidade <= len(NOMES):
        return rng.sample(NOMES, quantidade)
    return rng.choices(NOMES, k=quantidade)


def criar_medicos(quantidade, max_especialidades=1, semente=None):
    rng = random.Random(semente)
    medicos = []

    for numero, nome in enumerate(sortear_nomes(rng, quantidade), start=1):
        total = rng.randint(1, min(max_especialidades, len(ESPECIALIDADES)))
        medicos.append({'id': f'm{numero}', 'nome': nome,
                        'especialidades': rng.sample(ESPECIALIDADES, total)})

    return medicos


def especialidades_gerais(caminho=FACTS):
    """Especialidades declaradas como generalista(...) no facts.pl."""
    linhas, _ = _ler_facts(caminho)
    return [m.group(1) for l in linhas
            if (m := re.match(r'generalista\((\w+)\)', l))]


def definir_generalistas(medicos, quantidade, gerais=None, semente=None):
    """Devolve os médicos com exatamente `quantidade` generalistas.

    É generalista quem tem alguma das especialidades em `gerais` (por padrão,
    as declaradas como generalista(...) no facts.pl, como clinico_geral).
    Sorteia entre os que ainda não são e troca a primeira especialidade de
    cada um por uma das gerais. Quem já era conta na quantidade, e a lista
    recebida não é alterada.
    """
    rng = random.Random(semente)
    if gerais is None:
        gerais = especialidades_gerais()

    ja_sao = [i for i, m in enumerate(medicos)
              if any(e in gerais for e in m['especialidades'])]
    candidatos = [i for i in range(len(medicos)) if i not in ja_sao]
    faltam = min(max(0, quantidade - len(ja_sao)), len(candidatos))
    if faltam and not gerais:
        raise ValueError('nenhuma especialidade declarada como generalista')
    escolhidos = rng.sample(candidatos, faltam)

    resultado = []
    for posicao, medico in enumerate(medicos):
        especialidades = list(medico['especialidades'])
        if posicao in escolhidos:
            especialidades[:1] = [rng.choice(gerais)]
        resultado.append(dict(medico, especialidades=especialidades))

    return resultado


def criar_pacientes(quantidade, prob_geral=0.4, max_grupos=2, semente=None):
    rng = random.Random(semente)
    especiais = [g for g in GRUPOS if g != GRUPO_GERAL]
    pacientes = []

    for numero, nome in enumerate(sortear_nomes(rng, quantidade), start=1):
        if rng.random() < prob_geral or not especiais:
            grupos = [GRUPO_GERAL]
        else:
            total = rng.randint(1, min(max_grupos, len(especiais)))
            grupos = rng.sample(especiais, total)
        pacientes.append({'id': f'p{numero}', 'nome': nome,
                          'risco': rng.choice(RISCOS), 'grupos': grupos})

    return pacientes


def criar_perfis(especialidades=None, max_por_especialidade=3, semente=None):
    rng = random.Random(semente)
    if especialidades is None:
        especialidades = ESPECIALIDADES
    combinacoes = list(itertools.product(RISCOS, GRUPOS))
    perfis = []

    for especialidade in especialidades:
        total = rng.randint(1, min(max_por_especialidade, len(combinacoes)))
        for risco, grupo in rng.sample(combinacoes, total):
            perfis.append((especialidade, risco, grupo))

    return perfis


def _atomo(texto):
    return "'" + texto.replace("'", "''") + "'"


def fato_medico(medico):
    especialidades = ', '.join(medico['especialidades'])
    return f"medico({medico['id']}, {_atomo(medico['nome'])}, [{especialidades}])."


def fato_paciente(paciente):
    grupos = ', '.join(paciente['grupos'])
    return (f"paciente({paciente['id']}, {_atomo(paciente['nome'])}, "
            f"{paciente['risco']}, [{grupos}]).")


def fato_perfil(especialidade, risco, grupo):
    return f'perfil({especialidade}, {risco}, {grupo}).'


def gerar_fatos_prolog(medicos, pacientes, perfis):
    linhas = [fato_medico(m) for m in medicos]
    linhas += [fato_paciente(p) for p in pacientes]
    linhas += [fato_perfil(*p) for p in perfis]
    return '\n'.join(linhas) + '\n'


def _sem_gerado(linhas):
    resultado = []
    dentro = False
    for linha in linhas:
        if linha.startswith(MARCA_INICIO):
            dentro = True
        elif linha.startswith(MARCA_FIM):
            dentro = False
        elif not dentro:
            resultado.append(linha)
    return resultado


def _ler_facts(caminho):
    texto = Path(caminho).read_bytes().decode('utf-8')
    quebra = '\r\n' if '\r\n' in texto else '\n'
    return _sem_gerado(texto.split(quebra)), quebra


def _gravar_facts(caminho, linhas, quebra):
    Path(caminho).write_bytes(quebra.join(linhas).encode('utf-8'))


def _renumerar(itens, linhas, predicado, prefixo):
    padrao = re.compile(rf'{predicado}\({prefixo}(\d+),')
    usados = [int(m.group(1)) for l in linhas if (m := padrao.match(l))]
    inicio = max(usados, default=0) + 1
    return [dict(item, id=f'{prefixo}{inicio + n}')
            for n, item in enumerate(itens)]


def adicionar_ao_facts(medicos, pacientes, perfis, caminho=FACTS):
    linhas, quebra = _ler_facts(caminho)

    medicos = _renumerar(medicos, linhas, 'medico', 'm')
    pacientes = _renumerar(pacientes, linhas, 'paciente', 'p')
    com_perfil = {m.group(1) for l in linhas
                  if (m := re.match(r'perfil\((\w+),', l))}
    perfis = [p for p in perfis if p[0] not in com_perfil]

    blocos = {
        'medico(': [fato_medico(m) for m in medicos],
        'paciente(': [fato_paciente(p) for p in pacientes],
        'perfil(': [fato_perfil(*p) for p in perfis],
    }
    for inicio, fatos in blocos.items():
        posicoes = [i for i, linha in enumerate(linhas)
                    if linha.startswith(inicio)]
        if not posicoes:
            raise ValueError(f'{caminho} não tem nenhum fato {inicio}...')
        if fatos:
            ultimo = posicoes[-1] + 1
            linhas[ultimo:ultimo] = [MARCA_INICIO, *fatos, MARCA_FIM]

    _gravar_facts(caminho, linhas, quebra)
    return len(medicos), len(pacientes), len(perfis)


def limpar_gerado(caminho=FACTS):
    linhas, quebra = _ler_facts(caminho)
    _gravar_facts(caminho, linhas, quebra)


def gerar_e_adicionar(num_medicos, num_pacientes, semente=None,
                      num_generalistas=0, caminho=FACTS):
    medicos = criar_medicos(num_medicos, semente=semente)
    return adicionar_ao_facts(
        definir_generalistas(medicos, num_generalistas,
                             especialidades_gerais(caminho), semente),
        criar_pacientes(num_pacientes, semente=semente),
        criar_perfis(semente=semente),
        caminho,
    )


def main(argumentos):
    if argumentos == ['limpar']:
        limpar_gerado()
        print('facts.pl sem os fatos gerados')
    elif len(argumentos) in (2, 3):
        medicos, pacientes, *semente = map(int, argumentos)
        total = gerar_e_adicionar(medicos, pacientes, *semente)
        print('adicionados ao facts.pl: %d medicos, %d pacientes, %d perfis'
              % total)
    else:
        sys.exit(USO)


if __name__ == '__main__':
    main(sys.argv[1:])
