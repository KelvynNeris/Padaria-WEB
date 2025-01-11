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
        self.curso = None
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
            sql = "INSERT INTO tb_cliente (nome_comp, telefone, email, id_curso, senha, tipo) VALUES (%s, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (nome, telefone, email, curso, senha, tipo))
            
            # Atualiza os atributos do objeto
            self.tel = telefone
            self.nome = nome
            self.senha = senha
            self.curso = curso
            self.email = email
            self.tipo = tipo
            self.logado = True  # Marca o usuário como logado
            
            mydb.commit()  # Confirma as alterações no banco de dados
            mydb.close()  # Fecha a conexão
            return True
        except Exception as e:
            print(f"Ocorreu um erro: {e}")  # Exibe uma mensagem de erro em caso de falha
            return False