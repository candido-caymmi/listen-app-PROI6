import sqlite3

class Database:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.verificar_e_corrigir_tabela_ratings()

    def verificar_e_corrigir_tabela_ratings(self):
        self.cursor.execute("PRAGMA table_info(ratings)")
        colunas = self.cursor.fetchall()
        print("DEBUG - Colunas na tabela ratings:", colunas)

        # Verifica colunas existentes
        colunas_existentes = [col[1] for col in colunas]

        # Verifica e adiciona a coluna 'item_id' se necessário
        if "item_id" not in colunas_existentes:
            print("A coluna 'item_id' está ausente. Adicionando ao banco de dados...")
            self.cursor.execute("ALTER TABLE ratings ADD COLUMN item_id TEXT")
            self.conn.commit()
            print("Coluna 'item_id' adicionada com sucesso.")
        else:
            print("A coluna 'item_id' já existe.")

        # Verifica e adiciona a coluna 'tipo_item' se necessário
        if "tipo_item" not in colunas_existentes:
            print("A coluna 'tipo_item' está ausente. Adicionando ao banco de dados...")
            self.cursor.execute("ALTER TABLE ratings ADD COLUMN tipo_item TEXT")
            self.conn.commit()
            print("Coluna 'tipo_item' adicionada com sucesso.")
        else:
            print("A coluna 'tipo_item' já existe.")

    def create_tables(self):
        # Criação da tabela de usuários com ID do Spotify
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                spotify_user_id TEXT UNIQUE NOT NULL
            )
        ''')

        # Criação da tabela de avaliações de músicas
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,              -- ID do usuário que fez a avaliação
                music_id TEXT NOT NULL,                -- ID da música avaliada (do Spotify)
                rating INTEGER NOT NULL,               -- Nota da avaliação (0 a 5)
                comment TEXT,                          -- Comentário opcional do usuário
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data e hora da avaliação
                FOREIGN KEY (user_id) REFERENCES users (id) -- Chave estrangeira para usuários
            )
        ''')
        self.conn.commit()

    def add_user(self, username, email, spotify_user_id):
        self.cursor.execute("INSERT INTO users (username, email, spotify_user_id) VALUES (?, ?, ?)", 
                            (username, email, spotify_user_id))
        self.conn.commit()

    def get_user_by_spotify(self, spotify_user_id):
        self.cursor.execute("SELECT * FROM users WHERE spotify_user_id = ?", (spotify_user_id,))
        return self.cursor.fetchone()

    def get_ratings(self, user_id):
        """Retorna todas as avaliações de um usuário"""
        try:
            self.cursor.execute("SELECT music_id, rating, comment, timestamp FROM ratings WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar avaliações: {e}")
            return []
        
    def get_rating(self, user_id, item_id, tipo_item):
        """
        Retorna uma avaliação específica para um usuário e item.
        """
        try:
            self.cursor.execute(
                "SELECT rating, comment, timestamp FROM ratings WHERE user_id = ? AND music_id = ? AND tipo_item = ?",
                (user_id, item_id, tipo_item)
            )
            return self.cursor.fetchone()  # Retorna a avaliação encontrada ou None
        except Exception as e:
            print(f"Erro ao buscar avaliação: {e}")
            return None

    def add_rating(self, user_id, music_id, tipo_item, rating):
        """
        Adiciona uma avaliação ao banco de dados, se o usuário ainda não avaliou o item.
        """
        # Verifica se o ID da música ou tipo_item são válidos
        if not music_id or not tipo_item:
            print("Erro: ID da música ou tipo do item não podem ser vazios.")
            return

        try:
            # Verifica se já existe uma avaliação para este usuário e música
            self.cursor.execute(
                "SELECT * FROM ratings WHERE user_id = ? AND music_id = ? AND tipo_item = ?",
                (user_id, music_id, tipo_item)
            )
            avaliacao_existente = self.cursor.fetchone()

            if avaliacao_existente:
                print("Erro: Você já avaliou este item.")
                return  # Não permite duplicar a avaliação

            # Insere a nova avaliação, pois não foi encontrada nenhuma existente
            self.cursor.execute(
                "INSERT INTO ratings (user_id, music_id, tipo_item, rating) VALUES (?, ?, ?, ?)",
                (user_id, music_id, tipo_item, rating)
            )
            self.conn.commit()
            print(f"Avaliação adicionada com sucesso para music_id: {music_id}")
        except Exception as e:
            print(f"Erro ao adicionar avaliação: {e}")


    def get_average_rating(self, music_id):
        self.cursor.execute(''' 
            SELECT AVG(rating) AS average_rating 
            FROM ratings 
            WHERE music_id = ? 
        ''', (music_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()
