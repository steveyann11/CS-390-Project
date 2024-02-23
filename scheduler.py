from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)

@app.route("/index")
def hello_world():
    return render_template 'index.html'




app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with your own secret key

login_manager = LoginManager()
login_manager.init_app(app)

# Example user class (replace with your own user model)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Example user database (replace with your own user database)
users = {'user_id': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Example login form
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users and password == users[user_id]['password']:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Protected route
@app.route('/')
@login_required
def index():
    return 'Hello, {}'.format(current_user.id)

if __name__ == '__main__':
    app.run(debug=True)
