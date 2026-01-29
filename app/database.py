from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
#definimos las variables de entorno para la conexión a la base de datos MySQL desde el archivo .env
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")
MYSQL_HOST = "mysql"
#definimos la URL de conexión a la base de datos MySQL
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}/{MYSQL_DB}"
)
#creamos el motor de la base de datos utilizando SQLAlchemy
engine = create_engine(DATABASE_URL)
#creamos la clase SessionLocal para manejar las sesiones de la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
#creamos la clase Base para definir los modelos de la base de datos, todas las clases(tablas) de modelos heredarán de esta clase
Base = declarative_base()
