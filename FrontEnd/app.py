from flask import Flask, flash, redirect, render_template, request, url_for
import mysql.connector 

app = Flask(__name__)
app.secret_key = "senha_secreta"

def get_curso():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM curso")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return cursos

def get_relat():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM relatorio")
    relat = cursor.fetchall()
    cursor.close()
    conn.close()
    return relat

# Rota para mostrar os cursos

@app.route("/") 
def index():
    return render_template("Login/Login.html")

@app.route("/alunoCurso") 
def alunoCurso():
    relat=get_relat()
    return render_template("Tela de Aluno/alunoCurso.html", rela=relat)    

@app.route("/adminCursos") 
def adminCursos():
    return render_template("Telas de admin/adminCursos.html")

@app.route("/adminOutrosAdmin") 
def adminOutros():
    return render_template("Telas de admin/adminOutrosAdmins.html")

@app.route("/adminProfessores") 
def adminProfessores():
    return render_template("Telas de admin/adminProfessores.html")

@app.route("/cadastro") 
def cadastro():
    return render_template("CadastroAluno/Cadastro.html")

@app.route("/profCursos")
def profCursos():
    cursos = get_curso()
    return render_template("Telas dos Professores/profCursos.html", curso=cursos)

@app.route("/profNeF")
def profNeF():
    return render_template("Telas dos Professores/profNotasEFaltasDoCurso.html")

def verifica_login(email, senha):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aluno WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def verifica_login2(email, senha):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM professor WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def verifica_login3(email, senha):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE email=%s AND senha=%s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = verifica_login(email, senha)
        usuario2 = verifica_login2(email, senha)
        usuario3 = verifica_login3(email, senha)

        if usuario3:
            return redirect(url_for("adminCursos"))
        else:
            if usuario2:
                return redirect(url_for("profCursos"))
            else:
                if usuario:
                    return redirect(url_for("alunoCurso"))
                else:
                    flash("Email ou senha incorretos!")
                    return redirect(url_for("login"))

    return render_template("Login/Login.html")


if __name__ == "__main__":
    app.run(debug=True)
