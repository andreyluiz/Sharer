# -*- coding: UTF-8 -*-
# ------ Imports ------
from flask import Flask, request, redirect, url_for, session, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from forms import CadastroUsuario, NovoPost, LoginForm
import datetime

# ------ Instâncias da Aplicação ------
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
user = None

# ------ Modelos ------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60))
    email = db.Column(db.String(40))
    usuario = db.Column(db.String(30))
    senha = db.Column(db.String(30))
    data_cad = db.Column(db.DateTime)
    
    def __init__(self, nome, email, usuario, senha, data_cad = None):
        self.nome = nome
        self.email = email
        self.usuario = usuario
        self.senha = senha
        if data_cad is None: self.data_cad = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Usuario %i - %s>' % (self.id, self.nome)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60))
    texto = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref=db.backref('usuarios', lazy='dynamic'))
    data_pub = db.Column(db.DateTime)
    
    def __init__(self, titulo, texto, usuario, data_pub = None):
        self.titulo = titulo
        self.texto = texto
        self.usuario = usuario
        if data_pub is None: self.data_pub = datetime.datetime.utcnow()
        
    def __repr__(self):
        return '<Post %s>' % self.titulo

# ------ Métodos úteis ------
def null(var1, var2):
    if var1 is None:
        return var2
    else:
        return var1

# ------ Métodos de Aplicação ------
@app.route("/", methods=["GET", "POST"])
def index():
    form = NovoPost(request.form)
    posts = Post.query.order_by(Post.id.desc()).all()
    if request.method == "POST" and form.validate():        
        _usuario = None
        if 'usuarioid' in session:
            _usuario = Usuario.query.filter_by(id = session['usuarioid']).first()
        
        post = Post(form.titulo.data, form.texto.data, _usuario)
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for("index"))    
    return render_template("index.html", posts=posts, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    erro = None
    if request.method == "POST" and form.validate():
        db_usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        
        if db_usuario is None:            
            erro = "Usuario nao encontrado."
        else:
            if db_usuario.senha != form.senha.data:
                erro = "Senha invalida."
            else:
                session['logado'] = True
                session['usuario'] = form.usuario.data
                session['usuarioid'] = db_usuario.id
                flash("Bem vindo %s." % db_usuario.nome)
                return redirect(url_for("index"))
    return render_template("login.html", form=form, erro=erro)
    
@app.route("/logout")
def logout():
    session.pop('logado', None)
    session.pop('usuarioid', None)
    return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroUsuario(request.form)
    if request.method == "POST" and form.validate():                
        usuario = Usuario(form.nome.data, form.email.data, form.usuario.data, form.senha.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        return redirect(url_for("login"))        
    return render_template("cadastro.html", form=form)

@app.route("/editar/<int:post_id>", methods=["GET", "POST"])
def editar(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = NovoPost(request.form, obj=post)
    
    if request.method == "POST" and form.validate():
        post.titulo = form.titulo.data
        post.texto = form.texto.data
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for("index"))
    return render_template("editar.html", form=form, post_id=post.id)

@app.route("/deletar/<int:post_id>")
def deletar(post_id):
    _post = Post.query.filter_by(id=post_id).first()
    db.session.delete(_post)
    db.session.commit()
    
    return redirect(url_for("index"))        
    
@app.route("/usuario/<usuario>")
def usuario(usuario):
    _usuario = Usuario.query.filter_by(usuario=usuario).first()
    return render_template("usuario.html", usuario=_usuario)    
    
# ------ Método principal ------
if __name__ == '__main__':
    app.run()