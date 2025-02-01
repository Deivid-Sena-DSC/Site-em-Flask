from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from site_flask.models import Usuarios
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(3, 20)])
    email_criar_conta = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confimação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email_criar_conta(self, email_criar_conta):
        usuario = Usuarios.query.filter_by(email=email_criar_conta.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado')
        
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormEditarperfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(3, 20)])
    email_editar = StringField('Email', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editar = SubmitField('Confirmar Edição')

    def validate_email_editar(self, email_editar):
        if current_user.email != email_editar.data:
            usuario = Usuarios.query.filter_by(email=email_editar.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse email')
