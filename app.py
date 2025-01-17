from flask import Flask, render_template
import smtplib
import os
import random
from flask import Flask, render_template, request, redirect, session, flash
import email.message
from dotenv import load_dotenv
from usuario import Usuario  # Substitua pelo seu modelo de usuário
import re

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = '988430466tel'  # Chave secreta para gerenciamento de sessões

def verificar_sessao():
    """
    Função genérica para verificar o estado da sessão do usuário.
    Se o usuário estiver no meio do processo de verificação incompleta,
    a sessão será limpa.
    """
    if 'usuario_logado' in session and session.get('verificacao_incompleta'):
        # Limpa a sessão de usuário e a flag de verificação incompleta
        session.pop('usuario_logado', None)
        session.pop('verificacao_incompleta', None)

@app.route("/")
def inicio():
    verificar_sessao()
    if 'usuario_logado' in session:
        return redirect("/principal")
    return render_template("index.html")

@app.route("/principal")
def princiapal():
    verificar_sessao()
    return render_template("inicial.html")


# Função para enviar e-mail
def enviar_email(destinatario, codigo_verificacao):
    try:
        # Corpo do e-mail com o código de verificação
        corpo_email = f"""
        <p>{codigo_verificacao}</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Código de Verificação"
        msg['From'] = 'kelvyn.neris4305@gmail.com'  # Substitua pelo seu e-mail
        msg['To'] = destinatario  # Substitua pelo e-mail do destinatário
        password = 'yjnr ycly yaes xzur'  # Substitua pela sua senha

        # Definindo o tipo de conteúdo como HTML
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        # Conectando ao servidor SMTP do Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()  # Inicia a conexão segura
            # Login com o e-mail e a senha
            s.login(msg['From'], password)
            # Envia o e-mail
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        
        print('E-mail enviado com sucesso!')

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
    return True

# Rota de cadastro
@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    if 'usuario_logado' in session:
        return redirect("/principal")

    if request.method == 'GET':
        usuario = Usuario()
        return render_template("cadastrar-usuario.html")
    else:
        nome = request.form["nome"]
        telefone = request.form["tel"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = "funcionario"

        usuario = Usuario()

        if usuario.verificar_duplicidade(email, telefone):
            flash("Email ou telefone já cadastrado.")
            return redirect("/cadastrar_usuario")

        verification_code = str(random.randint(1000, 9999)).zfill(4)
        if not enviar_email(email, verification_code):
            flash("Erro ao enviar o e-mail. Tente novamente.")
            return redirect("/cadastrar_usuario")

        session['dados_cadastro'] = {
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "senha": senha,
            "tipo_verificacao": tipo,
            "verification_code": verification_code
        }
        session['tipo_verificacao'] = "cadastro"
        return redirect("/verificacao")

@app.route("/verificacao", methods=["GET", "POST"])
def verificacao():
    if 'dados_cadastro' not in session and 'email_pendente' not in session:
        session.pop('usuario_logado', None)
        return redirect("/logar")
    
    if request.method == 'GET':
        if session.get('tipo_verificacao') == 'cadastro':
            email = session.get('dados_cadastro', {}).get('email')
        else:
            email = session.get('email_pendente')
        
        return render_template("verificacao.html", email=email)  # Passando o 'email' como argumento

    codigo_inserido = "".join([  # Obtendo o código inserido
        request.form["codigo1"],
        request.form["codigo2"],
        request.form["codigo3"],
        request.form["codigo4"]
    ])
    
    # Obtendo o código de verificação da sessão
    verification_code = session.get('dados_cadastro', {}).get('verification_code') or session.get('atualizar_code')
    tipo_verificacao = session.get('tipo_verificacao')

    if codigo_inserido == verification_code or codigo_inserido == '6169':  # Código correto ou código de testes
        if tipo_verificacao == "cadastro":
            dados_cadastro = session.pop('dados_cadastro', None)
            if dados_cadastro:
                usuario = Usuario()
                usuario.cadastrar(
                    dados_cadastro["nome"],
                    dados_cadastro["telefone"],
                    dados_cadastro["email"],
                    dados_cadastro["senha"],
                    dados_cadastro["tipo_verificacao"]
                )
                usuario.entrar(dados_cadastro["email"], dados_cadastro["senha"])
                if usuario.logado:
                    session['usuario_logado'] = {
                        "nome": usuario.nome,
                        "email": usuario.email,
                        "tel": usuario.tel,
                        "id_usuario": usuario.id_usuario,
                        "tipo": usuario.tipo
                    }
            # Remover o código de verificação somente depois de cadastrar o usuário
            session.pop('verification_code', None)
            session.pop('tipo_verificacao', None)
            return redirect("/principal")

        elif tipo_verificacao == "atualizar_dados_iniciais":
            try:
                id_usuario = session['usuario_logado']['id_usuario']
                telefone = session['telefone']
                email = session.pop('email_pendente', None)
                senha = session.pop('senha_pendente', None)
                
                # Verifica se os dados obrigatórios estão presentes
                if not all([id_usuario, telefone, email, senha]):
                    raise ValueError("Dados incompletos para atualização.")
                
                usuario = Usuario()

                # Atualiza o e-mail
                if not usuario.atualizar_email(id_usuario, email):
                    raise Exception("Erro ao atualizar o e-mail.")

                # Atualiza os outros dados
                if not usuario.atualizar_dados(id_usuario, telefone, email, senha):
                    raise Exception("Erro ao atualizar os dados do usuário.")
                
                # Limpa a sessão após sucesso
                session.pop('verification_code', None)
                session.pop('tipo_verificacao', None)
                session.pop('verificacao_incompleta', None)

                return redirect("/principal")

            except Exception as e:
                # Limpa a sessão e redireciona ao login em caso de erro
                print(f"Erro ao atualizar dados iniciais: {e}")
                session.pop('usuario_logado', None)
                session.pop('verification_code', None)
                session.pop('tipo_verificacao', None)
                session.pop('verificacao_incompleta', None)
                session.pop('telefone', None)
                session.pop('email_pendente', None)
                session.pop('senha_pendente', None)
                flash("Ocorreu um erro ao atualizar os dados. Faça login novamente.")
                return redirect("/entrar")


    else:
        return render_template("verificacao.html", erro="Código incorreto. Tente novamente.")

@app.route("/entrar", methods=['GET', 'POST'])
def entrar():
    if request.method == 'GET':
        # Verifica se o usuário já está logado
        if 'usuario_logado' in session:
            usuario = session['usuario_logado']
            # Redireciona conforme o tipo do usuário
            if usuario.get('tipo') == 'Administrador':
                return redirect("/principal")
            else:
                return redirect("/principal")
            
        
        # Renderiza a página de login para usuários não logados
        erro = session.pop('login_erro', False)
        return render_template('entrar.html', success=False, erro=erro)
    
    # Processa o formulário de login
    senha = request.form['senha']
    email = request.form['email']
    usuario = Usuario()
    usuario.entrar(email, senha)
    
    if usuario.logado:
        # Define os dados do usuário na sessão
        session['usuario_logado'] = {
            "nome": usuario.nome, 
            "email": usuario.email, 
            "tel": usuario.tel, 
            "id_usuario": usuario.id_usuario, 
            "tipo": usuario.tipo,
            "senha": usuario.senha,
            "primeiro_login": usuario.primeiro_login
        }
        
        print("Sessão após login:", session)  # Verificação de sessão
        
        if usuario.tipo != 'Funcionario' and not usuario.primeiro_login:
            return redirect("/principal")

        if usuario.tipo != 'Funcionario' and usuario.primeiro_login:
            session['verificacao_incompleta'] = True
            return redirect("/atualizar_dados_iniciais")

        
        session['login_sucesso'] = True
        return redirect("/principal")
        
    # Define erro de login na sessão e redireciona para login
    session['login_erro'] = True
    return redirect("/logar")

@app.route("/atualizar_dados_iniciais", methods=["GET", "POST"])
def atualizar_dados_iniciais():
    # Verifica se o usuário está logado e se a verificação está pendente
    if 'usuario_logado' not in session:
        return redirect("/logar")
    
    if not session.get('verificacao_incompleta'):
        return redirect("/")
    
    if request.method == 'GET':
        return render_template("atualizar_dados_iniciais.html")

    # Processa a atualização dos dados
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not telefone or not email or not senha:
        return render_template("atualizar_dados_iniciais.html", erro="Preencha todos os campos corretamente.")

    # Exemplo de validação de e-mail (usando regex)
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return render_template("atualizar_dados_iniciais.html", erro="E-mail inválido.")

    id_usuario = session['usuario_logado']['id_usuario']
    usuario = Usuario()
    # Tenta atualizar o e-mail e verifica se houve sucesso
    try:
        if not usuario.atualizar_email(id_usuario, email):
            raise Exception("Erro ao atualizar o e-mail. Certifique-se de que ele não está em uso.")
    except Exception as e:
        return render_template("atualizar_dados_iniciais.html", erro=str(e))

    # Salva os dados pendentes na sessão
    session['telefone'] = telefone
    session['email_pendente'] = email
    session['senha_pendente'] = senha
    session['atualizar_code'] = str(random.randint(1000, 9999)).zfill(4)  # Gera um código de verificação
    session['tipo_verificacao'] = "atualizar_dados_iniciais"

    # Envia o código de verificação por e-mail
    if not enviar_email(email, session.get('atualizar_code')):
        return render_template("atualizar_dados_iniciais.html", erro="Erro ao enviar o e-mail de verificação. Tente novamente.")

    session['verificacao_incompleta'] = True
    return redirect("/verificacao")

# Rota para logout de usuários
@app.route('/sair')
def sair():
    if request.method == 'GET':
        session.clear()  # Limpa a sessão
        return redirect("/")  # Redireciona para a página inicial
  
@app.route('/produtos')
def produtos():
    usuario = Usuario()
    produtos = usuario.exibir_produtos()
    return render_template('produtos.html', produtos=produtos)

@app.route('/inserir_fornecedor', methods=['GET', 'POST'])
def inserir_fornecedor():
    if request.method == 'POST':
        # Obtém os dados do formulário
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        nome = request.form.get('nome')

        # Valida os campos obrigatórios
        if not (email and telefone and endereco and nome):
            return "Todos os campos são obrigatórios!", 400

        usuario = Usuario()

        # Chama a função para inserir o fornecedor
        sucesso = usuario.inserir_fornecedor(email, telefone, endereco, nome)

        if sucesso:
            return render_template('cad-fornecedor.html', mensagem="Fornecedor inserido com sucesso!")
        else:
            return "Erro ao inserir o fornecedor. Tente novamente.", 500

    # Exibe o formulário se for uma requisição GET
    return render_template('cad-fornecedor.html')

@app.route('/inserir_produto', methods=['GET', 'POST'])
def inserir_produto():
    usuario = Usuario()
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        estocado = request.form.get('estocado')
        categoria = request.form.get('categoria')
        fornecedor = request.form.get('fornecedor')
        preco = request.form.get('preco')

        # Valida os campos obrigatórios
        if not (estocado and descricao and categoria and nome and fornecedor and preco):
            return "Todos os campos são obrigatórios!", 400

        # Chama a função para inserir o fornecedor
        sucesso = usuario.inserir_produto(nome, descricao, estocado, categoria, fornecedor, preco)

        if sucesso:
            categorias = usuario.exibir_categoria()
            fornecedores = usuario.exibir_fornecedor()
            return render_template('cad-produto.html', mensagem="Produto inserido com sucesso!", categorias=categorias, fornecedores=fornecedores)
        else:
            return "Erro ao inserir o produto. Tente novamente.", 500
    categorias = usuario.exibir_categoria()
    fornecedores = usuario.exibir_fornecedor()
    return render_template('cad-produto.html', categorias=categorias, fornecedores=fornecedores)

@app.route('/inserir_categoria', methods=['GET', 'POST'])
def inserir_categoria():
    if request.method == 'POST':
        # Obtém os dados do formulário
        descricao = request.form.get('descricao')
        nome = request.form.get('nome')

        # Valida os campos obrigatórios
        if not (descricao and nome):
            return "Todos os campos são obrigatórios!", 400

        usuario = Usuario()

        # Chama a função para inserir o fornecedor
        sucesso = usuario.inserir_categoria(descricao, nome)

        if sucesso:
            return render_template('cad-fornecedor.html', mensagem="Fornecedor inserido com sucesso!")
        else:
            return "Erro ao inserir o fornecedor. Tente novamente.", 500

    # Exibe o formulário se for uma requisição GET
    return render_template('cad-categoria.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # Define o host como localhost e a porta como 8080