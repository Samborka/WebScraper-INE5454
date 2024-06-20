# Web Scraper de Resultados de Torneios de Jogadores Chineses de League of Legends

Este projeto coleta os resultados de torneios de jogadores chineses de League of Legends de uma página específica do wiki usando Selenium e BeautifulSoup.

## Requisitos

- Python 3.6+
- Google Chrome
- ChromeDriver

## Instruções de Configuração

### 1. Clonar o Repositório

```sh
git clone <url_do_repositorio>
cd <nome_do_repositorio>
```

### 2. Criar e ativar um Ambiente Virtual

```sh
python -m venv myenv
source myenv/bin/activate
```

### 3. Instalar as Dependências

```sh
pip install -r requirements.txt
```

### 4. ChromeDriver

É necessário baixar o chrome driver em `https://googlechromelabs.github.io/chrome-for-testing/`.

Outros sistemas operacionais podem precisar de outras alterações.

### 5. Executar o Script

```sh
python extractor.py
```

## Notas

- O script usa execução concorrente para acelerar o processo de scraping.
- Certifique-se de que o caminho do ChromeDriver no script corresponda ao local onde você colocou o ChromeDriver.

## Exemplo de saída

```json
[
    {
        "name": "Player1",
        "url": "http://exemplo.com/Player1_Tournament_Results",
        "results": [
            {
                "date": "2021-01-01",
                "place": "1º",
                "tournament": "Torneio Exemplo",
                "last_result": "Vitória",
                "team": "Equipe Exemplo",
                "roster": "Player1, Player2"
            },
            ...
        ]
    },
    ...
]
```
