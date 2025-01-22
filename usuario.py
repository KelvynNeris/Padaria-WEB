from conexao import Conexao
from hashlib import sha256
from flask import jsonify

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

    def atualizar_dados(self, id_usuario, telefone, email, senha):
        """
        Atualiza o telefone, email e senha do administrador e define 'primeiro_login' como False.
        
        Parâmetros:
        - id_usuario: ID do usuario (administrador) a ser atualizado
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
            valores = (telefone, email, hashed_password, False, id_usuario)

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

    def inserir_fornecedor(self, email, telefone, endereco, nome):
        try:
            # Conecta ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # SQL para inserir os dados
            sql = """
                INSERT INTO tb_fornecedores (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)
            """
            val = (nome, telefone, email, endereco)

            mycursor.execute(sql, val)  # Executa a query
            mydb.commit()  # Salva as alterações

            return True  # Retorna sucesso
        except Exception as e:
            print(f"Erro ao inserir fornecedor: {e}")
            return False  # Retorna falha
        finally:
            # Fecha a conexão
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def inserir_categoria(self, descricao, nome):
        try:
            # Conecta ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # SQL para inserir os dados
            sql = """
                INSERT INTO tb_categorias (nome, descricao) VALUES (%s, %s)
            """
            val = (nome, descricao)

            mycursor.execute(sql, val)  # Executa a query
            mydb.commit()  # Salva as alterações

            return True  # Retorna sucesso
        except Exception as e:
            print(f"Erro ao inserir categoria: {e}")
            return False  # Retorna falha
        finally:
            # Fecha a conexão
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def inserir_cliente_fiado(self, telefone, nome, email, endereco):
        try:
            # Conecta ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # SQL para inserir os dados
            sql = """
                INSERT INTO tb_clientes_fiado (telefone, nome, email, endereco) VALUES (%s, %s, %s, %s)
            """
            val = (telefone, nome, email, endereco)

            mycursor.execute(sql, val)  # Executa a query
            mydb.commit()  # Salva as alterações

            return True  # Retorna sucesso
        except Exception as e:
            print(f"Erro ao inserir cliente: {e}")
            return False  # Retorna falha
        finally:
            # Fecha a conexão
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def inserir_produto(self, nome, descricao, estocado, categoria, fornecedor, preco):
        try:
            # Conecta ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # SQL para inserir os dados
            sql = """
                INSERT INTO tb_produtos (nome, descricao, quantidade_estoque, id_categoria, id_fornecedor, preco) VALUES (%s, %s, %s, %s, %s, %s)
            """
            val = (nome, descricao, estocado, categoria, fornecedor, preco)

            mycursor.execute(sql, val)  # Executa a query
            mydb.commit()  # Salva as alterações

            return True  # Retorna sucesso
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
            return False  # Retorna falha
        finally:
            # Fecha a conexão
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def exibir_fornecedor(self):
        # Conecta ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = """
            SELECT * FROM tb_fornecedores
        """

        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_fornecedor = [{'id_fornecedor': fornecedor[0], 'nome': fornecedor[1]} for fornecedor in resultado]

        mydb.close()
        return lista_fornecedor
    
    def exibir_categoria(self):
        """
        Retorna uma lista com todas as categorias de produtos disponíveis, consultando a tabela `tb_categoria`.
        Cada categoria contém o ID da categoria e o nome da categoria.
        
        Retorno:
        - Uma lista de dicionários, onde cada dicionário representa uma categoria com 'id_categoria' e 'nome'.
        """
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        # Query SQL para selecionar todas as categorias
        sql = "SELECT * from tb_categorias"
        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_categoria = [{'id_categoria': categoria[0], 'nome': categoria[1]} for categoria in resultado]

        mydb.commit()
        mydb.close()
        return lista_categoria

    def exibir_produtos(self):
        """
        Retorna uma lista com todos os produtos, incluindo informações da categoria e do fornecedor,
        consultando as tabelas `tb_produtos`, `tb_categorias` e `tb_fornecedores`.

        Retorno:
        - Uma lista de dicionários, onde cada dicionário representa um produto com seus detalhes.
        """
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        # Query SQL para obter os produtos com suas respectivas categorias e fornecedores
        sql = """
            SELECT 
                p.id_produto,
                p.nome AS nome_produto,
                p.descricao,
                p.quantidade_estoque,
                p.preco,
                c.nome AS nome_categoria,
                f.nome AS nome_fornecedor
            FROM tb_produtos p
            INNER JOIN tb_categorias c ON p.id_categoria = c.id_categoria
            INNER JOIN tb_fornecedores f ON p.id_fornecedor = f.id_fornecedor
            WHERE p.ativo = 1
        """
        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_produto = [
            {
                'id_produto': produto[0],
                'nome_produto': produto[1],
                'descricao': produto[2],
                'quantidade_estoque': produto[3],
                'preco': produto[4],
                'nome_categoria': produto[5],
                'nome_fornecedor': produto[6]
            }
            for produto in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco de dados
        return lista_produto
    
    def exibir_usuarios(self):
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        sql = """
            SELECT * FROM tb_usuarios
            WHERE primeiro_login = 1
        """
        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_usuario = [
            {
                'id_usuario': usuario[0],
                'nome': usuario[1],
                'tipo': usuario[5],
            }
            for usuario in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco de dados
        return lista_usuario
    
    def deletar_usuario(self, id_usuario):
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            mycursor = mydb.cursor()

            # Comando SQL para deletar
            sql = "DELETE FROM tb_usuarios WHERE id_usuario = %s"
            val = (id_usuario,)

            mycursor.execute(sql, val)  # Executa o comando
            mydb.commit()  # Salva as alterações

            print(f"Usuário com ID {id_usuario} deletado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return False
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def aceitar_usuario(self, id_usuario):
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            mycursor = mydb.cursor()

            # Comando SQL para alterar o estado de primeiro_login
            sql = "UPDATE tb_usuarios SET primeiro_login = 0 WHERE id_usuario = %s"
            val = (id_usuario,)

            mycursor.execute(sql, val)  # Executa o comando
            mydb.commit()  # Salva as alterações

            print(f"Usuário com ID {id_usuario} aceito com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao aceitar usuário: {e}")
            return False
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    # Método para verificar o status de aprovação
    def verificar_status(self, id_usuario):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            sql = "SELECT primeiro_login FROM tb_usuarios WHERE id_usuario = %s"
            mycursor.execute(sql, (id_usuario,))
            resultado = mycursor.fetchone()

            return {'primeiro_login': resultado[0]} if resultado else {'primeiro_login': True}

        except Exception as e:
            print(f"Erro ao verificar status: {e}")
            return {'primeiro_login': True}
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def processar_atualizacao_quantidade(self, data):
        id_produto = data.get('id_produto')
        quantidade = int(data.get('quantidade'))
        acao = data.get('acao')

        if not id_produto or not quantidade or not acao:
            return jsonify({'success': False, 'error': 'Dados inválidos.'}), 400

        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # Atualização no banco de dados
            if acao == 'retirar':
                sql = "UPDATE tb_produtos SET quantidade_estoque = quantidade_estoque - %s WHERE id_produto = %s"
            elif acao == 'colocar':
                sql = "UPDATE tb_produtos SET quantidade_estoque = quantidade_estoque + %s WHERE id_produto = %s"
            else:
                return jsonify({'success': False, 'error': 'Ação inválida.'}), 400

            mycursor.execute(sql, (quantidade, id_produto))
            mydb.commit()

            # Obtém a nova quantidade
            mycursor.execute("SELECT quantidade_estoque FROM tb_produtos WHERE id_produto = %s", (id_produto,))
            nova_quantidade = mycursor.fetchone()[0]

            return jsonify({'success': True, 'nova_quantidade': nova_quantidade})

        except Exception as e:
            print(f"Erro ao atualizar a quantidade: {e}")
            return jsonify({'success': False, 'error': 'Erro no servidor.'}), 500

        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def remover_produto(id_produto):
        try:
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # Atualiza o status do produto para inativo
            sql = "UPDATE tb_produtos SET ativo = FALSE WHERE id_produto = %s"
            mycursor.execute(sql, (id_produto,))
            mydb.commit()

            return jsonify({'success': True, 'message': 'Produto removido com sucesso.'})

        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            return jsonify({'success': False, 'error': 'Erro ao remover produto.'}), 500

        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()

    def exibir_select_produtos(self):
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        sql = """
            SELECT * FROM tb_produtos
            WHERE ativo = 1
        """
        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_select_produtos = [
            {
                'id_produto': select_produtos[0],
                'nome': select_produtos[1],
                'preco': select_produtos[4],
            }
            for select_produtos in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco de dados
        return lista_select_produtos