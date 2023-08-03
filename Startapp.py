from flask import Flask
from reg_login.auth_views import auth_views
from bank.bank_views import bank_views
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)

app.register_blueprint(auth_views, url_prefix="/")
app.register_blueprint(bank_views, url_prefix="/bank/")



if __name__ == "__main__":
    print("app")
    app.run(debug=True)