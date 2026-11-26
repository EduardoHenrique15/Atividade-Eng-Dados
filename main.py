import os

from dotenv import load_dotenv

from assistente import AssistenteGPT
from banco import BancoNeon

load_dotenv(".env")

banco = BancoNeon(os.getenv("NEON"))
print("Tabelas:", banco.listar_tabelas())
print("Colunas de pnadc:", banco.descrever_tabela("pnadc"))
print("Amostra:", banco.consultar("SELECT * FROM pnadc LIMIT 3"))
print(banco.esquema_completo())

gpt = AssistenteGPT(os.getenv("GPT"))
pergunta = "Quantas linhas tem a tabela pnadc?"
sql = gpt.gerar_sql(pergunta, banco.esquema_completo())
print("SQL:", sql)
dados = banco.consultar(sql)
print("Resposta:", gpt.explicar_resultado(pergunta, dados))
