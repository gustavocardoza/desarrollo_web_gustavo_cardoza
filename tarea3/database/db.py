from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, DateTime, Enum, func, case
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date, datetime

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ___ MODELOS ___

class Aviso_adopcion(Base):
    __tablename__ = 'aviso_adopcion'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(String(500), nullable=True)
    comuna_id = Column(BigInteger, ForeignKey('comuna.id'), nullable=False)

class Comuna(Base):
    __tablename__ = 'comuna'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)

class Region(Base):
    __tablename__ = 'region'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

class Foto(Base):
    __tablename__ = 'foto'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False) # ForeignKey quiere decir q siosi debe haber un aviso asociado

class Contactar_por(Base):
    __tablename__ = 'contactar_por'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)   
    identificador = Column(String(150), nullable=False)
    aviso_id = Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False)

class Comentario(Base):
    __tablename__='comentario'

    id= Column(BigInteger, primary_key=True, autoincrement=True)
    nombre= Column(String(80), nullable=False)
    texto= Column(String(200), nullable=False)
    fecha= Column(DateTime, nullable=False)
    aviso_id= Column(BigInteger, ForeignKey('aviso_adopcion.id'), nullable=False)

# ___ FUNCIONES DE LA BASE DE DATOS ___

# Añade un nuevo aviso a la tabla 'Avisos_adopcion'.
def create_aviso_adopcion(id_comuna, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    # Fecha de ingreso
    fecha_ingreso = datetime.now()

    # Creamos un nuevo aviso en la base de datos
    session = SessionLocal()
    nuevo_aviso = Aviso_adopcion(comuna_id=id_comuna, fecha_ingreso=fecha_ingreso, sector=sector, nombre=nombre, email=email,
                                celular=celular, tipo=tipo, edad=edad, cantidad=cantidad, unidad_medida=unidad_medida, fecha_entrega=fecha_entrega, descripcion=descripcion)
    session.add(nuevo_aviso)
    # Lo añadimos a la base de datos
    session.commit()
    id_nuevo_aviso = nuevo_aviso.id
    session.close()
    return id_nuevo_aviso

# Añade una nueva foto a la tabla 'Foto'.
def create_foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    nueva_foto = Foto(ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo, aviso_id=actividad_id)
    session.add(nueva_foto)
    session.commit()
    session.close()

# Añade un nuevo método de contacto a la tabla 'Contactar_por'.
def create_contactar_por(metodo_contacto, detalle_contacto, aviso_id):
    session = SessionLocal()
    nuevo_contactar_por = Contactar_por(nombre=metodo_contacto, identificador=detalle_contacto, aviso_id=aviso_id)
    session.add(nuevo_contactar_por)
    session.commit()
    session.close()

# Añade un nuevo comentario a la base de datos de comentarios
def create_comentario(id, nombre, texto):
    fecha_comentario = datetime.now()
    session = SessionLocal()
    nuevo_comentario = Comentario(nombre=nombre, texto=texto, fecha=fecha_comentario, aviso_id=id)
    session.add(nuevo_comentario)
    session.commit()
    session.close()
    # hacemos q retorne la fecha para conveniencia
    return fecha_comentario

def get_comentarios_by_id(id):
    session = SessionLocal()
    comentarios = session.query(Comentario).filter_by(aviso_id=id).all()
    session.close()
    return comentarios

# Obtiene los 'n' avisos de adopción mas recientes de la tabla 'Avisos_adopcion'
def get_avisos_adopcion(n):
    session = SessionLocal()
    avisos_adopcion = session.query(Aviso_adopcion).order_by(Aviso_adopcion.fecha_ingreso.desc()).limit(n).all()
    session.close()
    return avisos_adopcion

# Obtiene todos los avisos de adopcion de la tabla 'Avisos_adopcion'.
def get_slices_avisos_adopcion(comienzo, final):
    session = SessionLocal()
    avisos_adopcion = session.query(Aviso_adopcion).order_by(Aviso_adopcion.fecha_ingreso.desc()).offset(comienzo).limit(final-comienzo).all()
    session.close()
    return avisos_adopcion

# Obtiene una comuna segun su ID de la tabla 'Comuna'
def get_comuna_by_id(id_comuna):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(id=id_comuna).first()
    session.close()
    return comuna

# Obtiene las fotos asociadas a un aviso de adopción
def get_foto_by_id(id_aviso):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(aviso_id=id_aviso)
    session.close()
    return fotos

# Obtiene el aviso asociado a cierto id.
def get_aviso_by_id(id_aviso):
    session = SessionLocal()
    aviso = session.query(Aviso_adopcion).filter_by(id=id_aviso).first()
    session.close()
    return aviso

# Obtiene los contactos asociados a cierto aviso por una id.
def get_contacto_by_id(id_aviso):
    session = SessionLocal()
    contactos = session.query(Contactar_por).filter_by(aviso_id=id_aviso)
    session.close()
    return contactos

# Obtiene la region asociada a cierta id.
def get_region_by_id(id_region):
    session = SessionLocal()
    region = session.query(Region).filter_by(id=id_region).first()
    session.close()
    return region

# Obtiene el número total de avisos.
def get_total_avisos():
    session = SessionLocal()
    nro_total = session.query(func.count(Aviso_adopcion.id)).scalar()
    session.close()
    return nro_total

# Vemos si la id escogida está en la base de datos
def validacion_id_region(id_region):
    session = SessionLocal()
    flag = session.query(Region).filter_by(id=id_region).first()
    session.close()
    if flag:
        return True
    return False

# Vemos si la id escogida está en la base de datos
def validacion_id_comuna(id_comuna):
    session = SessionLocal()
    flag = session.query(Comuna).filter_by(id=id_comuna).first()
    session.close()
    if flag:
        return True
    return False

# Obtenemos datos para la pestaña de estadisticas.
def get_estadisticas():
    session = SessionLocal()

    # 1er gráfico: Cantidad de avisos por día.
    query1 = (
        session.query(
            func.date(Aviso_adopcion.fecha_ingreso).label('fecha'),
            func.count(Aviso_adopcion.id).label('cantidad_avisos')
        )
        .group_by(func.date(Aviso_adopcion.fecha_ingreso))
        .order_by(func.date(Aviso_adopcion.fecha_ingreso))
    )

    avisos_por_dia = query1.all()

    # 2do gráfico: Cantidad total de perros y gatos.
    query = session.query(
        func.sum(case((Aviso_adopcion.tipo == 'perro', 1), else_=0)).label('cantidad_perros'),
        func.sum(case((Aviso_adopcion.tipo == 'gato', 1), else_=0)).label('cantidad_gatos')
    ).one()

    total_perros_gatos = query

    # 3er gráfico: Cantidad perros y gatos por mes.
    query = (
    session.query(
        func.date_format(Aviso_adopcion.fecha_ingreso, '%Y-%m').label('mes'),
        func.sum(case((Aviso_adopcion.tipo == 'perro', 1), else_=0)).label('cantidad_perros'),
        func.sum(case((Aviso_adopcion.tipo == 'gato', 1), else_=0)).label('cantidad_gatos')
        )
        .group_by(func.date_format(Aviso_adopcion.fecha_ingreso, '%Y-%m'))
        .order_by(func.date_format(Aviso_adopcion.fecha_ingreso, '%Y-%m'))
    )
    perros_gatos_mensual = query.all()

    session.close()
    return avisos_por_dia, total_perros_gatos, perros_gatos_mensual


