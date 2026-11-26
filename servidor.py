import os

from dotenv import load_dotenv
from fastmcp import FastMCP

from assistente import AssistenteGPT
from banco import BancoNeon

# 1) Lê as variáveis do arquivo .env (NEON e GPT)
load_dotenv()

# 2) Cria os objetos que fazem o trabalho de verdade
banco = BancoNeon(os.getenv("NEON"))
gpt = AssistenteGPT(os.getenv("GPT"))

# 3) Cria o servidor MCP
mcp = FastMCP("Servidor Neon + GPT")


# 4) Cada função com @mcp.tool vira uma ferramenta disponível para a IA.
#    A docstring é a descrição que a IA lê para saber quando usar a ferramenta.

@mcp.tool
def listar_tabelas() -> list[str]:
    """Lista as tabelas existentes no banco de dados."""
    return banco.listar_tabelas()


@mcp.tool
def descrever_tabela(tabela: str) -> list[dict]:
    """Mostra as colunas e os tipos de uma tabela."""
    return banco.descrever_tabela(tabela)


@mcp.tool
def executar_select(sql: str) -> list[dict]:
    """Executa um comando SELECT no banco e devolve as linhas."""
    return banco.consultar(sql)


@mcp.tool
def perguntar_ao_banco(pergunta: str) -> dict:
    """Responde uma pergunta em português: o GPT gera o SQL, o banco executa e o GPT explica."""
    sql = gpt.gerar_sql(pergunta, banco.esquema_completo())
    dados = banco.consultar(sql)
    resposta = gpt.explicar_resultado(pergunta, dados)
    return {"sql": sql, "dados": dados, "resposta": resposta}


if __name__ == "__main__":
    mcp.run()  # padrão: transporte stdio