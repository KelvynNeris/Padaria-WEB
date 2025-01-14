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