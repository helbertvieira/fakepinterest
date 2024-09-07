#Criar a estrutura de banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) #numero inteiro e id automatico
    username = database.Column(database.String, nullable=False) #nome e não pode ser vazio
    email = database.Column(database.String, nullable=False, unique=True) #nome e não pode ser vazio e tem que ser unico
    senha = database.Column(database.String, nullable=False) #nome e não pode ser vazio
    fotos = database.relationship("Foto", backref="usuario", lazy=True) # relação da coluna Usuario com a coluna foto como se estivesse fazendo "FOTO.usuario" / lazy= True é pra melhorar a interação entre as tabelas não esplicou a fundo
    
class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")# vai trazer o nome da imagem e a imagem será retirada da pasta static
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow()) #data da hora da postagem da foto utilizando a biblioteca datetime
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)#foreignKey é tabela estrangeira, faz a relação da tabela/coluna que tem relação  /  ordem do python / primero argumentos de posição, depois argumentos que tem nome 