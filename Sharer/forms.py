from wtforms import validators
from wtforms.fields.simple import TextField, PasswordField, TextAreaField
from wtforms.form import Form

class CadastroUsuario(Form):
    _vnome = "Nome deve ter entre 4 e 60 caracteres. Por favor, corrija!"
    _vemail = "E-mail deve ter entre 6 e 40 caracteres. Por favor, corrija!"
    _vusuario = "Usuario deve ter entre 5 e 30 caracteres. Por favor, corrija!"
    _vsenha = "Senha deve ter entre 5 e 30 caracteres. Por favor, corrija!"
    _vconfirm = "A confirmacao da senha nao confere com a senha informada. Por favor, corrija!"
    
    nome = TextField("Nome", [validators.length(4, 60, _vnome)])
    email = TextField("E-mail", [validators.length(6, 40, _vemail)])
    usuario = TextField("Usuario", [validators.length(5, 30, _vusuario)])    
    senha = PasswordField("Senha", [validators.length(3, 30, _vsenha)])
    confirma = PasswordField("Repita a Senha", [validators.EqualTo("senha", _vconfirm)])
    
class NovoPost(Form):
    _vtitulo = "O titulo deve ter entre 5 e 60 caracteres. Por favor, corrija!"
    _vtext = "O texto deve ter entre 10 e 1024 caracteres. Por favor, corrija!"
    
    titulo = TextField("Titulo", [validators.length(5, 60, _vtitulo)])
    texto = TextAreaField("Texto", [validators.length(10, 1024, _vtext)])
    
class LoginForm(Form):
    _vusuario = "Usuario deve ter entre 5 e 30 caracteres. Por favor, corrija!"
    _vsenha = "Senha deve ter entre 5 e 30 caracteres. Por favor, corrija!"
    
    usuario = TextField("Usuario", [validators.length(5, 30, _vusuario)])    
    senha = PasswordField("Senha", [validators.length(3, 30, _vsenha)])