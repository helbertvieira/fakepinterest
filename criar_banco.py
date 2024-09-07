from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto #importa do arquivo models as classes criadas

with app.app_context():
    database.create_all()