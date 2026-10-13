# Trabalho1_IA

Trabalho 1 da disciplina de Inteligência Artificial. O projeto é escrito em Python e usa o [Janus](https://www.swi-prolog.org/pldoc/man?section=janus) (`janus-swi`) para chamar o SWI-Prolog a partir do Python.

## Recursos necessários

| Recurso | Versão | Para que serve |
| --- | --- | --- |
| [Python](https://www.python.org/downloads/) | 3.12 ou superior | Executar o projeto |
| [SWI-Prolog](https://www.swi-prolog.org/download/stable) | 9.1.12 ou superior | Motor Prolog usado pelo `janus-swi` |
| [Poetry](https://python-poetry.org/docs/#installation) | 2.0 ou superior | Gerenciar o ambiente virtual e as dependências |
| Compilador C | — | Só é necessário quando não existe wheel pronto do `janus-swi` para a sua versão do Python (veja [Problemas comuns](#problemas-comuns)) |

## Instalação

### 1. Python

Baixe e instale o Python 3.12+ em <https://www.python.org/downloads/>. No Windows, marque a opção **"Add python.exe to PATH"** no instalador.

Confira a instalação:

```bash
python --version
```

### 2. SWI-Prolog

O SWI-Prolog precisa estar instalado **antes** das dependências do projeto, pois o `janus-swi` o localiza pelo comando `swipl`.

- **Windows:** baixe o instalador em <https://www.swi-prolog.org/download/stable> e, durante a instalação, escolha **"Add swipl to the system PATH"**. Outra opção é `winget install SWI-Prolog.SWI-Prolog`.
- **Linux (Debian/Ubuntu):** `sudo apt install swi-prolog`
- **macOS:** `brew install swi-prolog`

Abra um novo terminal e confira:

```bash
swipl --version
```

### 3. Poetry

Instale com o `pipx` (recomendado) ou com o `pip`:

```bash
pipx install poetry
```

```bash
pip install poetry
```

Confira a instalação:

```bash
poetry --version
```

### 4. Clonar o repositório

```bash
git clone git@github.com:FelipeAlmeida2004/Trabalho1_IA.git
```

```bash
cd Trabalho1_IA
```

### 5. Instalar as dependências

Na raiz do projeto (onde está o `pyproject.toml`):

```bash
poetry install
```

O Poetry cria um ambiente virtual e instala as dependências travadas no `poetry.lock`.

## Acessando o ambiente virtual

As dependências (como o `janus-swi`) ficam instaladas no ambiente virtual criado pelo Poetry, e **não** no Python do sistema. Por isso é necessário acessar esse ambiente antes de executar o projeto; do contrário, o import falha com `ModuleNotFoundError`.

1. Exiba o comando de ativação:

```bash
poetry env activate
```

2. Copie e execute a linha que o comando imprimir. No PowerShell, ela tem a forma `& "C:\...\Scripts\activate.ps1"`.

3. Com o ambiente ativo, o terminal mostra o nome dele no início da linha e `python` passa a usar as dependências do projeto. Para sair, use `deactivate`.

Se preferir não ativar o ambiente, coloque `poetry run` antes de cada comando (veja abaixo).

**VS Code:** selecione o interpretador do ambiente com `Ctrl+Shift+P` → `Python: Select Interpreter` → `trabalho1-ia-...-py3.12`. Sem isso, o editor usa o Python do sistema e sublinha o import como não reconhecido.

## Execução

Com o ambiente virtual ativo:

```bash
python main.py
```

Ou, sem ativar, usando o Poetry:

```bash
poetry run python main.py
```

## Verificando a instalação

Com o ambiente virtual ativo (ou usando `poetry run`), o comando abaixo deve imprimir `True` se o Python conseguir conversar com o SWI-Prolog:

```bash
poetry run python -c "import janus_swi as janus; print(janus.query_once('X = 1')['truth'])"
```

## Problemas comuns

**`swipl` não é reconhecido como comando**
O SWI-Prolog não está no `PATH`. Reinstale marcando a opção de adicionar ao `PATH` ou adicione manualmente a pasta `bin` da instalação (no Windows, normalmente `C:\Program Files\swipl\bin`) e abra um novo terminal.

**Erro de compilação ao instalar o `janus-swi`**
O `janus-swi` só publica wheels prontos para algumas combinações de sistema e versão do Python. Nas demais, o `pip`/Poetry compila o pacote a partir do código-fonte, o que exige um compilador C e o `swipl` no `PATH`:

- **Windows:** instale o [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) com a carga de trabalho "Desenvolvimento para desktop com C++".
- **Linux (Debian/Ubuntu):** `sudo apt install build-essential python3-dev swi-prolog`
- **macOS:** `xcode-select --install`

**`ModuleNotFoundError: No module named 'janus'`**
O pacote instalado se chama `janus-swi` e o módulo é importado como `janus_swi`. Use `import janus_swi as janus`.

**O Poetry usa a versão errada do Python**
Aponte o Poetry para um Python 3.12+ e reinstale:

```bash
poetry env use 3.12
```

```bash
poetry install
```
