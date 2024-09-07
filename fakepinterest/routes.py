#criar as rotas do site
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename #biblioteca já instalada no python para colocar nomes que evitem dar problema no site(sem caracteres especiais)


@app.route("/", methods=["GET", "POST"])#permitir os metodos enviar(GET) e receber(POST)
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)#form é o nome que será usado no HTML

@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()    
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=formcriarconta.username.data, senha=senha, email=formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=formcriarconta)#form é o nome que será usado no HTML


@app.route("/Perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #perfil do usuario, pode enviar foto
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),#tras o caminho de onde o arquivo routes que é o "__file__" está escrito
                              app.config["UPLOAD_FOLDER"], nome_seguro) #caminho do projeto / app.config["UPLOAD_FOLDER"] / nome_seguro
            arquivo.save(caminho)
            #registrar o arquivo no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)#adiciona foto no bancode dados
            database.session.commit()#salva foto no banco de dados
        return render_template("perfil.html", usuario=current_user, form=formfoto)#Perfil do usuario logado
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)#Perfil de outro usuário, não pode enviar nada, só visualizar


@app.route("/logout")
@login_required
def logout():
    logout_user()#mesmo não colocando o ccurrent_user, ele entende que é o usuário logado
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()[:100]#Se quiser limitar a quantidade de fotos passa entre colchetes
    return render_template("feed.html", fotos = fotos)