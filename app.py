from flask import Flask, render_template
# from usuario import Usuario

app = Flask(__name__)
app.secret_key = '988430466tel'  # Chave secreta para gerenciamento de sessões

@app.route("/")
def inicio():
    return render_template("entrar.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # Define o host como localhost e a porta como 8080