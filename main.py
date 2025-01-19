from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormCriarConta, FormLogin

app = Flask(__name__)

app.config['SECRET_KEY'] = '0be83548ee3e85c769b3b51d1324da50'

lista_usuarios = ['Paulo', 'lira', 'Deivid']

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com sucesso! Email: {form_login.email.data}', "alert-success")
        return redirect(url_for('home'))
    
    if form_criarconta.validate_on_submit() and "botao_submit_criarconta" in request.form:    
        flash(f'Conta criada com sucesso para o email: {form_criarconta.email_criar_conta.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login_criar_conta.html', form_login=form_login, form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)