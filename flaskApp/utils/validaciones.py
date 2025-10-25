from datetime import datetime, timedelta
import re
import filetype

def validacion_sector(sector):
    if not sector:
        return True
    if len(sector) > 100:
        print("sector")
        return False
    return True

def validacion_nombre(nombre):
    if not nombre:
        print("nombre")
        return False
    if len(nombre) < 2 or len(nombre) > 200:
        print("nombre2")
        return False
    pattern = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' -]+$"
    return bool(re.match(pattern, nombre))

def validacion_email(email):
    if not email:
        print("email")
        return False
    length_valid = len(email) < 100
    pattern = r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    format_valid = bool(re.match(pattern, email))
    print(format_valid, "email")
    return length_valid and format_valid

def validacion_telefono(telefono):
    if not telefono:
        print("fallo celu0")
        return True
    length_valid = len(telefono) == 12
    # formato NNN.NNNNNNNN
    pattern = r'^\d{3}\.\d{8}$'
    format_valid = bool(re.match(pattern, telefono))
    print("fallo celu", format_valid)
    return length_valid and format_valid

def validacion_metodo_y_detalle_contacto(metodo_contacto, detalle_contacto):
    metodos_validos = ["whatsapp", "telegram", "x", "instagram", "tiktok", "otra"]
    if len(metodo_contacto) != len(detalle_contacto):
        print("fallo metodos 1")
        return False
    if len(metodo_contacto) > 5:
        print("fallo metodos 2")
        return False
    for i in range(len(metodo_contacto)):
        if metodo_contacto[i] not in metodos_validos:
            print("fallo metodos 3")
            return False
        if not detalle_contacto[i] or detalle_contacto[i].strip() == "":
            print("fallo metodos 4")
            return False
        if len(detalle_contacto[i]) < 4 and len(detalle_contacto[i]) > 50:
            print("fallo metodos 5")
            return False
    return True

def validacion_tipo(tipo):
    if not tipo:
        print("fallo tipo1")
        return False
    if not (tipo == "perro" or tipo == "gato"):
        print("fallo tipo2")
        return False
    return True 
    
def validacion_cantidad(cantidad):
    if not cantidad:
        print("fallo cantid 1")
        return False
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        print("fallo cantidad 2")
        return False

    if cantidad < 1:
        print("fallo cantid 3")
        return False
    return True

def validacion_edad(edad):
    if not edad:
        print("fallo edad 1")
        return False
    try:
        edad = int(edad)
    except (ValueError, TypeError):
        print("fallo edad 2")
        return False

    if edad < 1:
        print("fallo edad 3")
        return False
    return True

def validacion_unidad_medida(unidad_medida):
    if not unidad_medida:
        print("fallo um 1")
        return False
    if not (unidad_medida == "a" or unidad_medida == "m"):
        print("fallo um 2")
        return False
    return True

def validacion_fecha(fecha_str):
    fecha_input = datetime.fromisoformat(fecha_str)
    fecha_actual = datetime.now()
    fecha_actual_mas_3_horas = fecha_actual + timedelta(hours=3)
    print("fecha",fecha_input >= fecha_actual_mas_3_horas)
    return fecha_input >= fecha_actual_mas_3_horas


def validacion_imagen(imagen_aviso):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "avif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif", "image/avif"}

    if imagen_aviso == None:
        print("fallo imagen 1")
        return False

    if imagen_aviso.filename == "":
        print("fallo imagen 2")
        return False

    ftype_guess = filetype.guess(imagen_aviso)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        print(ftype_guess.extension)
        print("fallo imagen 3")
        return False

    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        print(ftype_guess.mime)
        print("fallo imagen 4")
        return False

    return True

def validacion_imagenes(imagenes_aviso):
    flag = True
    for imagen in imagenes_aviso:
        flag &= validacion_imagen(imagen)
    print("FINALMENTE LA VALIDACION DE LAS IMAGENES ES:", flag)
    return flag

def validacion_general(data):
    return (
        validacion_sector(data.get("sector")) and
        validacion_nombre(data.get("nombre")) and
        validacion_email(data.get("email")) and
        validacion_telefono(data.get("telefono")) and
        validacion_metodo_y_detalle_contacto(
            data.get("metodo_contacto", []),
            data.get("detalle_contacto", [])
        ) and
        validacion_tipo(data.get("tipo")) and
        validacion_cantidad(data.get("cantidad")) and
        validacion_edad(data.get("edad")) and
        validacion_unidad_medida(data.get("unidad_medida")) and
        validacion_fecha(data.get("fecha")) and
        validacion_imagenes(data.get("imagenes"))
    )

def validacion_comentario(nombre, comentario):
    return nombre and (len(nombre)>=3) and (len(nombre)<=80) and (len(comentario)>=5)