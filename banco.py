from contextlib import closing

import psycopg2


class BancoNeon:
    def __init__(self, url_conexao):
        self.url_conexao = url_conexao

    def _conectar(self):
        conexao = psycopg2.connect(self.url_conexao)
        conexao.set_session(readonly=True)
        return conexao

    def consultar(self, sql):
        """Executa um SELECT e devolve uma lista de dicionários."""
        with closing(self._conectar()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(sql)
                colunas = [coluna[0] for coluna in cursor.description]
                linhas = cursor.fetchall()

        return [dict(zip(colunas, linha)) for linha in linhas]

    def listar_tabelas(self):
        """Retorna o nome de todas as tabelas do schema public."""
        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """
        return [linha["table_name"] for linha in self.consultar(sql)]

    def descrever_tabela(self, tabela):
        """Retorna as colunas e os tipos de uma tabela."""
        with closing(self._conectar()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position
                    """,
                    (tabela,),
                )
                return [{"coluna": c, "tipo": t} for c, t in cursor.fetchall()]

    def esquema_completo(self):
        """Monta um texto com todas as tabelas e colunas (usado pelo GPT)."""
        texto = ""
        for tabela in self.listar_tabelas():
            colunas = self.descrever_tabela(tabela)
            lista = ", ".join(f"{c['coluna']} ({c['tipo']})" for c in colunas)
            texto += f"- {tabela}: {lista}\n"
        return texto


class BancoComLimite(BancoNeon):
    def __init__(self, url_conexao, limite=10):
        super().__init__(url_conexao)
        self.limite = limite

    def consultar(self, sql):
        linhas = super().consultar(sql)
        return linhas[: self.limite]
