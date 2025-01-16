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
    return render_template("index.html")

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
        return redirect("/")

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
        return render_template("verificacao.html")

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
            return redirect("/")

        elif tipo_verificacao == "atualizar_dados_iniciais":
            id_usuario = session['usuario_logado']['id_usuario']
            telefone = session['telefone']
            email = session.pop('email_pendente')
            senha = session.pop('senha_pendente')
            usuario = Usuario()
            usuario.atualizar_email(id_usuario, email)
            usuario.atualizar_dados(id_usuario, telefone, email, senha)
            session.pop('verification_code', None)
            session.pop('tipo_verificacao', None)
            session.pop('verificacao_incompleta', None)
            return redirect("/")

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
                return redirect("/")
            else:
                return redirect("/")
            
        
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
            return redirect("/inicialadm")

        if usuario.tipo != 'Funcionario' and usuario.primeiro_login:
            session['verificacao_incompleta'] = True
            return redirect("/atualizar_dados_iniciais")

        
        session['login_sucesso'] = True
        return redirect("/")
        
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
    usuario.atualizar_email(id_usuario, email)

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # Define o host como localhost e a porta como 8080