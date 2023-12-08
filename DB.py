from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
import os 

app = Flask(__name__)

# Veritabanı yapılandırması
# Ana veritabanı için
base_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_directory, 'main_database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Arızalı ürünler veritabanı için
app.config['SQLALCHEMY_BINDS'] = {'arizali': 'sqlite:///' + os.path.join(base_directory, 'arizali_database.sqlite')}

# Ana veritabanı için SQLAlchemy nesnesi oluşturma
main_db = SQLAlchemy(app)

# Marshmallow nesnesi oluşturma
serializer = Marshmallow(app)
