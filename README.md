# Servidor MCP: Neon + GPT

Servidor MCP (FastMCP) que consulta um banco PostgreSQL no Neon e usa o GPT
para responder perguntas em português.

## Como rodar
1. Crie e ative o ambiente virtual:
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Instale as bibliotecas: `pip install -r requirements.txt`
3. Copie o `.env.example` para `.env` e preencha `NEON` e `GPT`
4. Teste:
   - `python main.py`
   - `python cliente_teste.py`
   - `fastmcp dev inspector servidor.py`

## Arquivos
- `banco.py`: classes `BancoNeon` e `BancoComLimite` (acesso ao PostgreSQL)
- `assistente.py`: classe `AssistenteGPT` (gera SQL e explica resultados)
- `servidor.py`: servidor MCP com as ferramentas
- `cliente_teste.py`: cliente para testar pelo terminal

## Ferramentas MCP
- `listar_tabelas`: lista as tabelas
- `descrever_tabela`: colunas e tipos de uma tabela
- `executar_select`: executa um SELECT
- `perguntar_ao_banco`: pergunta em português; o GPT gera o SQL e explica
- `contar_linhas`: número de linhas de uma tabela

## Segurança
- Conexão em modo somente leitura (`readonly=True`)
- Parâmetros com `%s` contra SQL Injection
- `.env` fora do Git (`.gitignore`)
