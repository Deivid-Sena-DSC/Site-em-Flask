from flask import render_template, redirect, url_for, flash, request
from site_flask import app, database, bcrypt
from site_flask.forms import FormCriarConta, FormLogin, FormEditarperfil
from site_flask.models import Usuarios
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def home():
    return render_template('home.html') 

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = database.session.query(Usuarios).all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuarios.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso! Email: {form_login.email.data}', "alert-success")
            page_next = request.args.get('next')
            if page_next:
                return redirect(page_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login ou senha ínvalidos', 'alert-danger')
    
    if form_criarconta.validate_on_submit() and "botao_submit_criarconta" in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuarios(username=form_criarconta.username.data, email=form_criarconta.email_criar_conta.data, senha=senha_crypt)
        with app.app_context():
            database.session.add(usuario)
            database.session.commit()    
        flash(f'Conta criada com sucesso para o email: {form_criarconta.email_criar_conta.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login_criar_conta.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('cria_post.html')

@app.route('/perfil/editar', methods=["GET", "POST"])
@login_required
def editar_perfil():
    form_editar = FormEditarperfil()
    if form_editar.validate_on_submit():
        current_user.email = form_editar.email_editar.data
        current_user.username = form_editar.username.data
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form_editar.username.data = current_user.username
        form_editar.email_editar.data = current_user.email

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editar=form_editar)
