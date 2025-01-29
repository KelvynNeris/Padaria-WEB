from conexao import Conexao
from hashlib import sha256
from flask import jsonify
from datetime import datetime

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

    def inserir_produto(self, nome, descricao, unidade_estocado, kilo_estocado, categoria, fornecedor, preco, preco_kilo, vendido_por_kilo):
        try:
            # Conecta ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # SQL para inserir os dados
            sql = """
                INSERT INTO tb_produtos (
                    nome, descricao, quantidade_estoque, quantidade_estoque_kilos, 
                    id_categoria, id_fornecedor, preco, preco_por_kilo, vendido_por_kilo
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Verifica o tipo de venda
            if vendido_por_kilo:
                # Produto vendido por kilo
                val = (nome, descricao, unidade_estocado, kilo_estocado, categoria, fornecedor, preco, preco_kilo, True)
            else:
                # Produto vendido por unidade
                val = (nome, descricao, unidade_estocado, kilo_estocado, categoria, fornecedor, preco, preco_kilo, False)

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
        Retorna uma lista com todos os produtos, incluindo informações da categoria, fornecedor e tipo (unidade ou kilo).
        """
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        # Query SQL para obter os produtos com informações adicionais
        sql = """
            SELECT 
                p.id_produto,
                p.nome AS nome_produto,
                p.descricao,
                p.quantidade_estoque,
                p.quantidade_estoque_kilos,
                p.preco,
                p.preco_por_kilo,
                p.vendido_por_kilo,
                c.nome AS nome_categoria,
                f.nome AS nome_fornecedor
            FROM tb_produtos p
            INNER JOIN tb_categorias c ON p.id_categoria = c.id_categoria
            INNER JOIN tb_fornecedores f ON p.id_fornecedor = f.id_fornecedor
            WHERE p.ativo = 1
        """
        mycursor.execute(sql)

        # Organizar os resultados
        resultado = mycursor.fetchall()
        lista_produto = [
            {
                'id_produto': produto[0],
                'nome_produto': produto[1],
                'descricao': produto[2],
                'quantidade': produto[4] if produto[7] else produto[3],  # Usa kilos ou unidades
                'preco': produto[6] if produto[7] else produto[5],  # Preço por kilo ou por unidade
                'vendido_por_kilo': produto[7],
                'nome_categoria': produto[8],
                'nome_fornecedor': produto[9],
            }
            for produto in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco
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
                'preco_por_kilo': select_produtos[5],
                'vendido_kilo': select_produtos[8]
            }
            for select_produtos in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco de dados
        return lista_select_produtos
    
    from flask import jsonify

    def exibir_clientes(self):
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        sql = """
            SELECT * FROM tb_clientes_fiado
        """

        mycursor.execute(sql)

        # Obtém os resultados e os organiza em uma lista
        resultado = mycursor.fetchall()
        lista_clientes = [
            {
                'id_cliente': clientes[0],
                'nome': clientes[1],
                'saldo': clientes[5],
            }
            for clientes in resultado
        ]

        mydb.close()  # Fecha a conexão com o banco de dados
        return lista_clientes

    def buscar_cliente_por_id(self, id_cliente):
        """
        Busca um cliente no banco de dados pelo ID.
        :param id_cliente: ID do cliente a ser buscado.
        :return: Dicionário contendo os dados do cliente ou None se não encontrado.
        """
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            with mydb.cursor() as mycursor:
                # Query para buscar cliente pelo ID
                sql = "SELECT id_cliente, nome, saldo_em_aberto FROM tb_clientes_fiado WHERE id_cliente = %s LIMIT 1"
                mycursor.execute(sql, (id_cliente,))
                resultado = mycursor.fetchone()

                # Retorna um dicionário com os dados do cliente ou None
                return {"id_cliente": resultado[0], "nome": resultado[1], "saldo_em_aberto": resultado[2]} if resultado else None
        except Exception as e:
            print(f"Erro ao buscar cliente por ID: {e}")
            raise
        finally:
            mydb.close()


    def calcular_total_venda(self, itens):
        """
        Calcula o total da venda com base nos itens fornecidos.
        """
        return sum(item['quantidade'] * item['preco_unitario'] for item in itens)

    def inserir_venda(self, id_usuario, total_venda, pagamento, id_cliente=None):
        """
        Insere uma venda no banco de dados e retorna o ID gerado.
        :param id_usuario: ID do usuário que realizou a venda.
        :param total_venda: Valor total da venda.
        :param pagamento: Tipo de pagamento (ex: 'dinheiro', 'cartão', 'fiado').
        :param id_cliente: ID do cliente (opcional).
        :return: ID da venda gerado.
        """
        try:
            sql_venda = """
                INSERT INTO tb_vendas (id_usuario, total, pagamento, id_cliente) 
                VALUES (%s, %s, %s, %s)
            """
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            mycursor = mydb.cursor()
            
            mycursor.execute(sql_venda, (id_usuario, total_venda, pagamento, id_cliente))
            id_venda = mycursor.lastrowid  # Obtém o último ID inserido
            
            mydb.commit()  # Confirma a transação
            mycursor.close()
            mydb.close()
            
            return id_venda
        except Exception as e:
            print(f"Erro ao inserir venda: {e}")
            raise


    def atualizar_estoque(self, itens):
        """
        Atualiza o estoque no banco de dados com base nos itens vendidos.
        :param itens: Lista de itens contendo id_produto e quantidade.
        """
        try:
            sql_buscar_estoque = """
                SELECT quantidade_estoque, quantidade_estoque_kilos, vendido_por_kilo 
                FROM tb_produtos 
                WHERE id_produto = %s
            """
            sql_atualizar_estoque = """
                UPDATE tb_produtos
                SET 
                    quantidade_estoque = CASE
                        WHEN vendido_por_kilo = FALSE THEN quantidade_estoque - %s
                        ELSE quantidade_estoque
                    END,
                    quantidade_estoque_kilos = CASE
                        WHEN vendido_por_kilo = TRUE THEN quantidade_estoque_kilos - %s
                        ELSE quantidade_estoque_kilos
                    END
                WHERE id_produto = %s
            """
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            for item in itens:
                id_produto = item['id_produto']  # ID do produto
                quantidade = item['quantidade']  # Quantidade vendida (em unidades ou quilos)

                # Buscar informações do estoque e tipo de venda do produto
                mycursor.execute(sql_buscar_estoque, (id_produto,))
                resultado = mycursor.fetchone()

                if resultado is None:
                    raise Exception(f"Produto com ID {id_produto} não encontrado.")

                quantidade_estoque, quantidade_estoque_kilos, vendido_por_kilo = resultado

                # Verificar disponibilidade do produto
                if not vendido_por_kilo and quantidade_estoque < quantidade:
                    raise Exception(f"Produto com ID {id_produto} está indisponível para a quantidade solicitada.")
                if vendido_por_kilo and quantidade_estoque_kilos < quantidade:
                    raise Exception(f"Produto com ID {id_produto} está indisponível para a quantidade solicitada.")

                # Para produtos vendidos por unidade, a quantidade em quilos será 0 e vice-versa
                quantidade_unidade = quantidade if not vendido_por_kilo else 0
                quantidade_kilos = quantidade if vendido_por_kilo else 0

                # Atualizar estoque
                mycursor.execute(sql_atualizar_estoque, (quantidade_unidade, quantidade_kilos, id_produto))

            mydb.commit()
            mycursor.close()
            mydb.close()

        except Exception as e:
            print(f"Erro ao atualizar estoque: {e}")
            raise

    def inserir_itens_venda(self, id_venda, itens):
        """
        Insere os itens de uma venda no banco de dados.
        :param id_venda: ID da venda associada.
        :param itens: Lista de itens contendo id_produto, quantidade e preco_unitario.
        """
        try:
            sql_item = """
                INSERT INTO tb_itens_venda (id_venda, id_produto, quantidade, preco_unitario) 
                VALUES (%s, %s, %s, %s)
            """
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            mycursor = mydb.cursor()
            
            for item in itens:
                mycursor.execute(sql_item, (id_venda, item['id_produto'], item['quantidade'], item['preco_unitario']))
            
            mydb.commit()  # Confirma a transação
            mycursor.close()
            mydb.close()
        except Exception as e:
            print(f"Erro ao inserir itens da venda: {e}")
            raise

    def relatorio_mais_vendidos_produtos(self):
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        try:
            # Consulta SQL para obter os produtos mais vendidos por quantidade
            sql_1 = """
                SELECT 
                    p.nome, 
                    SUM(i.quantidade) AS total_vendido,
                    SUM(i.quantidade * i.preco_unitario) AS total_arrecadado,
                    v.data_venda
                FROM 
                    tb_itens_venda i
                JOIN 
                    tb_produtos p ON i.id_produto = p.id_produto
                JOIN 
                    tb_vendas v ON i.id_venda = v.id_venda
                GROUP BY 
                    p.id_produto, v.data_venda
                ORDER BY 
                    total_vendido DESC;
            """

            # Consulta SQL para obter os produtos mais vendidos por total arrecadado
            sql_2 = """
                SELECT 
                    p.nome, 
                    SUM(i.quantidade) AS total_vendido,
                    SUM(i.quantidade * i.preco_unitario) AS total_arrecadado,
                    v.data_venda
                FROM 
                    tb_itens_venda i
                JOIN 
                    tb_produtos p ON i.id_produto = p.id_produto
                JOIN 
                    tb_vendas v ON i.id_venda = v.id_venda
                GROUP BY 
                    p.id_produto, v.data_venda
                ORDER BY 
                    total_arrecadado DESC;
            """

            # Executa a primeira consulta (ordenada por total vendido)
            mycursor.execute(sql_1)
            resultados_1 = mycursor.fetchall()

            # Executa a segunda consulta (ordenada por total arrecadado)
            mycursor.execute(sql_2)
            resultados_2 = mycursor.fetchall()

            # Prepara os resultados para a quantidade vendida
            lista_mais_vendidos_produtos_quantidade = [
                {
                    'nome': produto[0],
                    'total_vendido': produto[1],
                    'total_arrecadado': produto[2],
                    'data': produto[3]
                }
                for produto in resultados_1
            ]

            # Prepara os resultados para o total arrecadado
            lista_mais_vendidos_produtos_arrecadado = [
                {
                    'nome': produto[0],
                    'total_vendido': produto[1],
                    'total_arrecadado': produto[2],
                    'data': produto[3]
                }
                for produto in resultados_2
            ]

            return lista_mais_vendidos_produtos_quantidade, lista_mais_vendidos_produtos_arrecadado

        except Exception as e:
            print(f"Erro ao gerar relatório de produtos mais vendidos: {e}")
            return [], []

        finally:
            # Fecha o cursor e a conexão
            mycursor.close()
            mydb.close()

    def relatorio_mais_vendidos_categorias(self):
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        # Consulta SQL para obter as categorias mais vendidas por quantidade
        sql_1 = """
            SELECT 
                c.nome AS nome_categoria,
                SUM(i.quantidade) AS total_vendido,
                SUM(i.quantidade * i.preco_unitario) AS total_arrecadado,
                v.data_venda
            FROM 
                tb_itens_venda i
            JOIN 
                tb_produtos p ON i.id_produto = p.id_produto
            JOIN
                tb_categorias c ON p.id_categoria = c.id_categoria
			JOIN 
				tb_vendas v ON i.id_venda = v.id_venda
            GROUP BY 
                c.id_categoria, v.data_venda
            ORDER BY 
                total_vendido DESC;
        """

        # Consulta SQL para obter as categorias mais vendidas por total arrecadado
        sql_2 = """
            SELECT 
                c.nome AS nome_categoria,
                SUM(i.quantidade) AS total_vendido,
                SUM(i.quantidade * i.preco_unitario) AS total_arrecadado,
                v.data_venda
            FROM 
                tb_itens_venda i
            JOIN 
                tb_produtos p ON i.id_produto = p.id_produto
            JOIN
                tb_categorias c ON p.id_categoria = c.id_categoria
			JOIN 
				tb_vendas v ON i.id_venda = v.id_venda
            GROUP BY 
                c.id_categoria, v.data_venda
            ORDER BY 
                total_arrecadado DESC;
        """

        try:
            # Executa a primeira consulta
            mycursor.execute(sql_1)
            resultados_1 = mycursor.fetchall()

            # Executa a segunda consulta
            mycursor.execute(sql_2)
            resultados_2 = mycursor.fetchall()

            # Prepara os resultados
            lista_mais_vendidos_categorias = [
                {
                    'nome_categoria': vendidos_categorias[0],
                    'total_vendido': vendidos_categorias[1],
                    'total_arrecadado': vendidos_categorias[2],
                    'data': vendidos_categorias[3]
                }
                for vendidos_categorias in resultados_1
            ]

            lista_mais_vendidos_categorias_arrecadado = [
                {
                    'nome_categoria': vendidos_categorias[0],
                    'total_vendido': vendidos_categorias[1],
                    'total_arrecadado': vendidos_categorias[2],
                    'data': vendidos_categorias[3]
                }
                for vendidos_categorias in resultados_2
            ]

            # Fecha o cursor e a conexão
            mycursor.close()
            mydb.close()

            return lista_mais_vendidos_categorias, lista_mais_vendidos_categorias_arrecadado

        except Exception as e:
            print("Erro ao executar as consultas:", e)
            # Fecha o cursor e a conexão em caso de erro
            mycursor.close()
            mydb.close()
            return None, None
    
    def relatorio_metodos_pagamento_mais_usados(self):
        """
        Gera um relatório dos métodos de pagamento mais utilizados.
        Retorna duas listas de dicionários: uma com o tipo de pagamento, a quantidade de transações e o total arrecadado ordenado por transações,
        e outra ordenada por total arrecadado.
        """
        mydb = Conexao.conectar()  # Conecta ao banco de dados
        mycursor = mydb.cursor()

        try:
            # Consulta SQL para obter os métodos de pagamento mais utilizados por quantidade de transações
            sql_1 = """
                SELECT 
                    v.pagamento AS tipo_pagamento,
                    COUNT(v.id_venda) AS total_transacoes,
                    SUM(v.total) AS total_arrecadado,
					v.data_venda
                FROM 
                    tb_vendas v
                GROUP BY 
                    v.pagamento,  v.data_venda
                ORDER BY 
                    total_transacoes DESC;
            """

            # Consulta SQL para obter os métodos de pagamento mais utilizados por total arrecadado
            sql_2 = """
                SELECT 
                    v.pagamento AS tipo_pagamento,
                    COUNT(v.id_venda) AS total_transacoes,
                    SUM(v.total) AS total_arrecadado,
					v.data_venda
                FROM 
                    tb_vendas v
                GROUP BY 
                    v.pagamento,  v.data_venda
                ORDER BY 
                    total_arrecadado DESC;
            """

            # Executa a primeira consulta (ordenada por transações)
            mycursor.execute(sql_1)
            resultados_1 = mycursor.fetchall()

            # Executa a segunda consulta (ordenada por total arrecadado)
            mycursor.execute(sql_2)
            resultados_2 = mycursor.fetchall()

            # Formata os resultados em uma lista de dicionários para a quantidade de transações
            lista_metodos_pagamento_transacoes = [
                {
                    'tipo_pagamento': metodo[0],
                    'total_transacoes': metodo[1],
                    'total_arrecadado': float(metodo[2]),  # Converte para float para facilitar formatação
                    'data': metodo[3]
                }
                for metodo in resultados_1
            ]

            # Formata os resultados em uma lista de dicionários para o total arrecadado
            lista_metodos_pagamento_arrecadado = [
                {
                    'tipo_pagamento': metodo[0],
                    'total_transacoes': metodo[1],
                    'total_arrecadado': float(metodo[2]),  # Converte para float para facilitar formatação
                    'data': metodo[3]
                }
                for metodo in resultados_2
            ]

            return lista_metodos_pagamento_transacoes, lista_metodos_pagamento_arrecadado

        except Exception as e:
            print(f"Erro ao gerar relatório de métodos de pagamento: {e}")
            return [], []

        finally:
            # Fecha o cursor e a conexão
            mycursor.close()
            mydb.close()

    def dentro_do_periodo(self, data, data_inicial=None, data_final=None):
        """
        Checa se uma data está dentro do período especificado.
        """
        if not data_inicial and not data_final:
            return True
        
        # Se a data for um objeto datetime, não precisa converter
        if isinstance(data, str):
            data = datetime.strptime(data, '%Y-%m-%d')

        if data_inicial:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            if data < data_inicial:
                return False
        
        if data_final:
            data_final = datetime.strptime(data_final, '%Y-%m-%d')
            if data > data_final:
                return False

        return True

    def atualizar_saldo_cliente(self, id_cliente, novo_saldo):
        """
        Atualiza o saldo em aberto do cliente fiado no banco de dados.
        :param id_cliente: ID do cliente cujo saldo será atualizado.
        :param novo_saldo: Novo saldo a ser registrado no banco.
        """
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            with mydb.cursor() as mycursor:
                sql = "UPDATE tb_clientes_fiado SET saldo_em_aberto = %s WHERE id_cliente = %s"
                mycursor.execute(sql, (novo_saldo, id_cliente))
                mydb.commit()  # Confirma a alteração no banco
        except Exception as e:
            print(f"Erro ao atualizar saldo do cliente ID {id_cliente}: {e}")
            raise
        finally:
            mydb.close()

    def relatorio_fiado(self):
        """
        Recupera todas as transações fiadas de clientes e calcula o total de fiado, total pago e total pendente.
        :return: Dicionário com a lista de transações e os totais.
        """
        try:
            mydb = Conexao.conectar()  # Conecta ao banco de dados
            with mydb.cursor() as mycursor:
                # Consulta SQL para buscar transações fiadas
                sql = """
                    SELECT 
                        c.nome AS cliente, 
                        t.data_venda AS data, 
                        t.total AS valor, 
                        t.status_pagamento AS status
                    FROM 
                        tb_vendas t
                    JOIN 
                        tb_clientes_fiado c ON t.id_cliente = c.id_cliente
                    WHERE 
                        t.pagamento = 'Fiado'
                """
                mycursor.execute(sql)
                transacoes = mycursor.fetchall()

                # Calcula os totais
                total_fiado = sum(t[2] for t in transacoes)  # Soma os valores das transações
                total_pago = sum(t[2] for t in transacoes if t[3] == 'Pago')  # Soma apenas os pagos
                total_pendente = total_fiado - total_pago  # O restante é pendente

                # Converte para o formato esperado na view
                transacoes_formatted = [
                    {"cliente": t[0], "data": t[1], "valor": t[2], "status": t[3]} 
                    for t in transacoes
                ]

                return {
                    "transacoes": transacoes_formatted,
                    "total_fiado": total_fiado,
                    "total_pago": total_pago,
                    "total_pendente": total_pendente
                }
        except Exception as e:
            print(f"Erro ao gerar relatório de fiado: {e}")
            raise
        finally:
            mydb.close()