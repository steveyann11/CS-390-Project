from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with your own secret key
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database path

#db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
#id = db.Column(db.Integer, primary_key=True)
 #   username = db.Column(db.String(100), unique=True, nullable=False)
  #  password = db.Column(db.String(100), nullable=False)

# Create the user table
#db.create_all()

#@login_manager.user_loader
#def load_user(user_id):
 #   return User.query.get(int(user_id))


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
    return render_template('homepage.html')


@app.route('/calendar')
@login_required
def calendar():
    return render_template ('calendar.html')


@app.route('/scheduling')
@login_required
def scheduling():
    return render_template ('scheduling.html')


if __name__ == '__main__':
    app.run(debug=True)
