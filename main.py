import os
from dotenv import load_dotenv
from banco import BancoNeon
from assistente import AssistenteGPT

load_dotenv(".env")
banco = BancoNeon(os.getenv("NEON"))
banco.listar_tabelas()
    ['pnadc', 'pnadc_spark']
banco.descrever_tabela("pnadc")
banco.consultar("SELECT * FROM pnadc LIMIT 3")

print(banco.esquema_completo())


from assistente import AssistenteGPT
gpt = AssistenteGPT(os.getenv("GPT"))
sql = gpt.gerar_sql("Quantas linhas tem a tabela pnadc?", banco.esquema_completo())
sql
'SELECT COUNT(*) FROM pnadc;'
dados = banco.consultar(sql)
gpt.explicar_resultado("Quantas linhas tem a tabela pnadc?", dados)


