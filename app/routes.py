from flask import render_template, flash, redirect, url_for, request
from flask_smorest import Api
from app import app, db
from app.forms import RegistrationForm
from app.models import User, Transaction
from flask_login import LoginManager, login_user, current_user, logout_user
from app.forms import LoginForm
from werkzeug.urls import url_parse
from flask_login import logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.resources import blp as transactionBlueprint
import yaml
from flask_login import login_required

app.config["API_TITLE"] = "Library API"
app.config["API_VERSION"] = "v0.0.1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_DESCRIPTION"] = "A simple library API"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

api = Api(app)
api.register_blueprint(transactionBlueprint)

# Add server information to the OpenAPI spec
api.spec.options["servers"] = [
    {
        "url": "http://127.0.0.1:5000",
        "description": "Local development server"
    }
]


# Serve OpenAPI spec document endpoint for download
@app.route("/openapi.yaml")
@login_required
def openapi_yaml():
    spec = api.spec.to_dict()
    return app.response_class(
        yaml.dump(spec, default_flow_style=False),
        mimetype="application/x-yaml"
    )


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# перенаправлнение на страницу после входа пользователя
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user)
    else:
        return redirect(url_for('login'))


# маршрут корневой страницы
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')


# страница пользователей с их данными
@app.route('/balanse')
@login_required
def users():
    all_users = User.query.all()
    return render_template('balanse.html', users=all_users)


# маршрут регистрации пользовователей
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    balance=form.balance.data, commission_rate=form.commission_rate.data,
                    URL_webhook=form.URL_webhook.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# маршрут изменения данных пользователя
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.username = request.form['username']
        user.password = generate_password_hash(request.form['password'])
        user.email = request.form['email']
        user.balance = request.form['balance']
        user.commission_rate = request.form['commission_rate']
        user.URL_webhook = request.form['URL_webhook']
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('edit.html', user=user)


# маршрут для входа пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# маршрут для удаления пользователя
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('profile'))


# маршрут для выхода пользователя
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# маршрут для вывода транзакций
@app.route('/transaction')
@login_required
def transactions():
    transaction_list = Transaction.query.all()
    return render_template('transaction.html', transactions=transaction_list)
