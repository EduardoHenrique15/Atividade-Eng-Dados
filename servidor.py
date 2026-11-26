import os

from dotenv import load_dotenv
from fastmcp import FastMCP

from assistente import AssistenteGPT
from banco import BancoComLimite

load_dotenv()

banco = BancoComLimite(os.getenv("NEON"))
gpt = AssistenteGPT(os.getenv("GPT"), os.getenv("MODELO", "gpt-6-luna"))

mcp = FastMCP("Servidor Neon + GPT")


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


@mcp.tool
def contar_linhas(tabela: str) -> int:
    """Conta quantas linhas uma tabela possui."""
    if tabela not in banco.listar_tabelas():
        raise ValueError(f"Tabela '{tabela}' não existe")
    return banco.consultar(f"SELECT COUNT(*) AS total FROM {tabela}")[0]["total"]


if __name__ == "__main__":
    mcp.run()
