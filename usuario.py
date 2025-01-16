from conexao import Conexao
from hashlib import sha256

class Usuario:
    
    """
    Classe responsável por gerenciar as operações de usuários e produtos no sistema.
    Essa classe oferece funcionalidades como cadastrar usuários, logar, exibir cursos e categorias, 
    inserir produtos, entre outras operações relacionadas ao usuário e suas interações com o sistema.
    """
    
    def __init__(self):
        """
        Método inicializador que define os atributos da classe Usuario. Esses atributos
        armazenam informações como telefone, nome, senha, email, curso, tipo, e o estado de login do usuário.
        """
        self.tel = None
        self.nome = None
        self.senha = None
        self.email = None
        self.imagem = None
        self.nomeP = None
        self.categoria = None
        self.tipo = None
        self.logado = False

    # Função de cadastro do usuário
    def cadastrar(self, nome, telefone, email, senha, tipo):
        senha = sha256(senha.encode()).hexdigest()  # Criptografa a senha usando o algoritmo sha256
        
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            mycursor = mydb.cursor()

            # Verifica se o email ou telefone já estão cadastrados
            mycursor.execute(
                "SELECT id_usuario FROM tb_usuarios WHERE email = %s OR telefone = %s",
                (email, telefone)
            )
            existing_user = mycursor.fetchone()
            
            if existing_user:
                # Retorna False para indicar que o cadastro foi impedido por duplicidade
                return False

            # Insere o novo usuário caso não haja duplicidade
            sql = "INSERT INTO tb_usuarios (nome, telefone, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(sql, (nome, telefone, email, senha, tipo))
            
            # Atualiza os atributos do objeto
            self.tel = telefone
            self.nome = nome
            self.senha = senha
            self.email = email
            self.tipo = tipo
            self.logado = True  # Marca o usuário como logado
            
            mydb.commit()  # Confirma as alterações no banco de dados
            mydb.close()  # Fecha a conexão
            return True
        except Exception as e:
            print(f"Ocorreu um erro: {e}")  # Exibe uma mensagem de erro em caso de falha
            return False
        
    def verificar_duplicidade(self, email, telefone):
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT id_usuario FROM tb_usuarios WHERE email = %s OR telefone = %s",
            (email, telefone)
        )
        return bool(mycursor.fetchone())
    
    def entrar(self, email, senha):
        """
        Realiza o login de um usuário verificando o email e a senha criptografada no banco de dados.
        Se a combinação for encontrada, o estado do usuário é marcado como logado e os dados do usuário
        são carregados para os atributos da classe.
        
        Parâmetros:
        - email: endereço de email do usuário.
        - senha: senha do usuário, que será criptografada antes da verificação.
        
        Retorno:
        - None. O estado de login e os dados do usuário são atualizados nos atributos da classe.
        """
        senha = sha256(senha.encode()).hexdigest()  # Criptografa a senha usando o algoritmo sha256
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        try:
            # Query SQL para verificar se o email e a senha correspondem a um registro no banco de dados
            sql = "SELECT * FROM tb_usuarios WHERE email = %s AND senha = %s"
            mycursor.execute(sql, (email, senha))

            # Busca um único registro (se houver)
            resultado = mycursor.fetchone()

            # Se um registro for encontrado, atualiza os atributos do usuário
            if resultado:
                self.logado = True
                self.id_usuario = resultado[0]
                self.nome = resultado[1]
                self.email = resultado[2]
                self.senha = resultado[3]
                self.tel = resultado[4]
                self.tipo = resultado[5]
                self.primeiro_login = bool(resultado[7])  # Converte para bool
            else:
                self.logado = False
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            mycursor.close()
            mydb.close()

    def atualizar_email(self, id_usuario, email):
        """
        Atualiza o email do usuario no banco de dados.

        Parâmetros:
        - id_usuario: ID do usuario que terá o telefone atualizado
        - email: Novo email a ser salvo

        Retorno:
        - True se a atualização for bem-sucedida, False caso contrário
        """
        # Conectar ao banco de dados
        mydb = Conexao.conectar()  
        mycursor = mydb.cursor()

        try:
            # Comando SQL para atualizar o telefone
            sql = "UPDATE tb_usuarios SET email = %s WHERE id_usuario = %s"
            valores = (email, id_usuario)

            # Executa a atualização
            mycursor.execute(sql, valores)
            mydb.commit()
            print("Email atualizado com sucesso!")
            return True
        except Exception as e:
            print("Erro ao atualizar o email:", e)
            mydb.rollback()
            return False
        finally:
            # Fecha o cursor e a conexão com o banco
            mycursor.close()
            mydb.close()

    def atualizar_dados(self, id_cliente, telefone, email, senha):
        """
        Atualiza o telefone, email e senha do administrador e define 'primeiro_login' como False.
        
        Parâmetros:
        - id_cliente: ID do cliente (administrador) a ser atualizado
        - telefone: Novo número de telefone
        - email: Novo email
        - senha: Nova senha em texto puro que será criptografada para o banco de dados
        
        Retorno:
        - True se a atualização for bem-sucedida, False caso contrário
        """
        # Hash da senha antes de armazenar no banco
        hashed_password = sha256(senha.encode()).hexdigest()
        
        # Conecta ao banco de dados
        mydb = Conexao.conectar()  
        mycursor = mydb.cursor()

        try:
            # Query para atualizar os dados do administrador e marcar `primeiro_login` como `False`
            sql = """
                UPDATE tb_usuarios
                SET telefone = %s, email = %s, senha = %s, primeiro_login = %s
                WHERE id_usuario = %s
            """
            valores = (telefone, email, hashed_password, False, id_cliente)

            # Executa a query
            mycursor.execute(sql, valores)
            mydb.commit()
            
            # Atualiza o atributo `primeiro_login` localmente
            self.primeiro_login = False
            return True
        except Exception as e:
            print("Erro ao atualizar dados do administrador:", e)
            mydb.rollback()
            return False
        finally:
            # Fecha o cursor e a conexão
            mycursor.close()
            mydb.close()