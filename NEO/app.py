from flask import Flask, flash, redirect, render_template, request, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "senha_secreta"

# --------------------------
# CLASSES DE MODELO
# --------------------------
class Database:
    """Classe para conexão com o banco de dados"""
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mydb"
        )

class Curso:
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM curso")
        cursos = cursor.fetchall()
        cursor.close()
        conn.close()
        return cursos

class Aluno:
    @staticmethod
    def get(aluno_id=None):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        if aluno_id:
            cursor.execute("SELECT * FROM aluno WHERE IDAluno=%s", (aluno_id,))
            aluno = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM aluno")
            aluno = cursor.fetchall()
        cursor.close()
        conn.close()
        return aluno

    @staticmethod
    def verifica_login(email, senha):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM aluno WHERE email=%s AND senha=%s", (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def get_relatorios(aluno_id=None):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        if aluno_id:
            cursor.execute("SELECT * FROM relatorio WHERE Aluno_IDAluno=%s", (aluno_id,))
        else:
            cursor.execute("SELECT * FROM relatorio")
        relat = cursor.fetchall()
        cursor.close()
        conn.close()
        return relat

    @staticmethod
    def esta_inscrito(aluno_id, curso_id):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM relatorio WHERE Aluno_IDAluno=%s AND Curso_IDCurso=%s", (aluno_id, curso_id))
        inscrito = cursor.fetchone()
        cursor.close()
        conn.close()
        return inscrito

class Professor:
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM professor")
        prof = cursor.fetchall()
        cursor.close()
        conn.close()
        return prof

    @staticmethod
    def verifica_login(email, senha):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM professor WHERE email=%s AND senha=%s", (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

class Admin:
    @staticmethod
    def get_all():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin")
        admins = cursor.fetchall()
        cursor.close()
        conn.close()
        return admins

    @staticmethod
    def verifica_login(email, senha):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE email=%s AND senha=%s", (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

# --------------------------
# ROTAS PRINCIPAIS
# --------------------------
@app.route("/")
def index():
    return render_template("Login/Login.html")

@app.route("/Cadastro", methods=["GET", "POST"])
def Cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        telefone = request.form.get("telefone")
        genero = request.form.get("genero")
        nascimento = request.form.get("nascimento")
        endereco = request.form.get("endereco")

        # Conectar ao banco e inserir
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO aluno (Nome, email, senha, Telefone, Genero, Nascimento, Endereco)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, senha, telefone, genero, nascimento, endereco))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Cadastro realizado com sucesso!")
        return redirect(url_for("login"))

    return render_template("CadastroAluno/Cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Admin.verifica_login(email, senha)
        if usuario:
            session['aluno_id'] = None
            return redirect(url_for("adminCursos"))

        usuario = Professor.verifica_login(email, senha)
        if usuario:
            session['aluno_id'] = None
            return redirect(url_for("profCursos"))

        usuario = Aluno.verifica_login(email, senha)
        if usuario:
            session['aluno_id'] = usuario['IDAluno']
            return redirect(url_for("alunoCurso"))

        flash("Email ou senha incorretos!")
        return redirect(url_for("login"))

    return render_template("Login/Login.html")

# --------------------------
# ROTAS DE ALUNO
# --------------------------
@app.route("/alunoCurso")
def alunoCurso():
    if 'aluno_id' not in session:
        flash("Faça login para acessar seus cursos!")
        return redirect(url_for("login"))

    aluno_id = session['aluno_id']
    relat = Aluno.get_relatorios(aluno_id)
    return render_template("Tela de Aluno/alunoCurso.html", relat=relat)

@app.route("/alunoEntrarCurso")
def alunoEntrarCurso():
    if 'aluno_id' not in session:
        flash("Faça login para acessar os cursos!")
        return redirect(url_for("login"))

    aluno_id = session['aluno_id']
    cursos = Curso.get_all()
    relat = Aluno.get_relatorios(aluno_id)
    cursos_disponiveis = [c for c in cursos if not Aluno.esta_inscrito(aluno_id, c['IDCurso'])]

    return render_template("Tela de Aluno/alunoEntrarCurso.html",
                           curso=cursos_disponiveis,
                           aluno=Aluno.get(aluno_id),
                           relat=relat)

@app.route("/entrar_curso", methods=["POST"])
def entrar_curso():
    if 'aluno_id' not in session:
        flash("Você precisa estar logado para entrar em um curso!")
        return redirect(url_for("login"))

    aluno_id = session['aluno_id']
    curso_id = request.form.get("Curso_IDCurso")

    if Aluno.esta_inscrito(aluno_id, curso_id):
        flash("Você já está inscrito nesse curso!")
        return redirect(url_for("alunoEntrarCurso"))

    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO relatorio (Aluno_IDAluno, Curso_IDCurso, NotaAluno, FaltaAluno) VALUES (%s,%s,0,0)",
                   (aluno_id, curso_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Inscrição realizada com sucesso!")
    return redirect(url_for("alunoEntrarCurso"))

# --------------------------
# ROTAS ADMIN
# --------------------------
@app.route("/adminCursos")
def adminCursos():
    cursos = Curso.get_all()
    return render_template("Telas de admin/adminCursos.html", curso=cursos)

@app.route("/adminAlunos")
def adminAlunos():
    alunos = Aluno.get()
    return render_template("Telas de admin/adminAlunos.html", aluno=alunos)

@app.route("/adminOutrosAdmin")
def adminOutrosAdmin():
    admins = Admin.get_all()
    return render_template("Telas de admin/adminOutrosAdmin.html", adminO=admins)

@app.route("/adminProfessores")
def adminProfessores():
    profs = Professor.get_all()
    return render_template("Telas de admin/adminProfessores.html", prof=profs)

# --------------------------
# ROTAS PROFESSOR
# --------------------------
@app.route("/profCursos")
def profCursos():
    cursos = Curso.get_all()
    return render_template("Telas dos Professores/profCursos.html", curso=cursos)

@app.route("/profNeF")
def profNeF():
    alunos = Aluno.get()
    relat = Aluno.get_relatorios()  # mostra todos os relatórios
    return render_template("Telas dos Professores/profNotasEFaltasDoCurso.html", alunos=alunos, relat=relat)

# --------------------------
# ROTAS DE NOTAS
# --------------------------
@app.route("/salvar_notas", methods=["POST"])
def salvar_notas():
    aluno_id = request.form.get("Aluno_IDAluno")
    nova_nota = request.form.get("NotaAluno")
    nova_falta = request.form.get("FaltaAluno")
    curso_id = request.form.get("Curso_IDCurso")

    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE relatorio SET NotaAluno=%s, FaltaAluno=%s WHERE Aluno_IDAluno=%s AND Curso_IDCurso=%s",
                   (nova_nota, nova_falta, aluno_id, curso_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("profNeF"))

# --------------------------
# EXECUÇÃO
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
