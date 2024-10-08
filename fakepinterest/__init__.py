from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app=Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")#Altera a variavel para o link do external no Render, roda criar banco uma única vez pra criar o banco e depois volta a variavel normal
app.config["SECRET_KEY"] = "79d66f3e1defe9f4a71bf7cc6b5641fa"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"
from fakepinterest import routes