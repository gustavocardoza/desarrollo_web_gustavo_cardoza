from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_cors import cross_origin
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import utils
from utils import validaciones as val

app = Flask(__name__)

app.secret_key = 'programacionweb'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "static", "uploads")

# Función extrae los datos del form y los añade a la base de datos si son válidos.
@app.route("/post_aviso", methods=["GET","POST"])
def post_aviso():
    if request.method == "POST":
        print("hola")

        # Obtenemos los datos del form.
        id_region = request.form.get("region")
        id_comuna = request.form.get("comuna")
        sector = request.form.get("sector")

        nombre = request.form.get("nombre")
        email = request.form.get("email")
        telefono = request.form.get("tel")

        metodo_contacto = request.form.getlist("metodo_contacto[]")
        detalle_contacto = request.form.getlist("contacto_detalle[]")

        tipo = request.form.get("tipo_mascota")
        cantidad = request.form.get("cantidad_mascota")
        edad = request.form.get("edad_mascota")
        unidad_medida = request.form.get("u_medida")
        fecha_entrega = request.form.get("fecha_disponible")
        descripcion = request.form.get("descripcion")

        fotos = request.files.getlist("foto_mascota[]")

        # Creamos un diccionario con los datos para pasarlo por las validaciones correspondientes.
        datos = {
                "id_region": id_region,
                "id_comuna": id_comuna,
                "sector": sector,

                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "metodo_contacto": metodo_contacto,
                "detalle_contacto": detalle_contacto,

                "tipo": tipo,
                "cantidad": cantidad,
                "edad": edad,
                "unidad_medida": unidad_medida,
                "fecha": fecha_entrega,
                "descripcion": descripcion,
                "imagenes": fotos
            }

        # Antes de añadir los datos proporcionados a la base de datos, se pasan por validación.
        if val.validacion_general(datos) and db.validacion_id_region(id_region) and db.validacion_id_comuna(id_comuna):

            # Validaciones correctas, entonces añadimos el nuevo aviso a la base de datos. Obtenemos el id del aviso 
            # para asociarlo a la base de datos de las fotos.
            id_nuevo_aviso = db.create_aviso_adopcion(id_comuna, sector, nombre, email, telefono, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion)

            # Procedimiento para añadir las fotos a la base de datos.
            for foto in fotos:
                # 1.- Generamos un nombre aleatorio para la imagen
                _filename = hashlib.sha256(secure_filename(foto.filename).encode("utf-8")).hexdigest()
                _extension = filetype.guess(foto).extension

                img_filename = f"{_filename}.{_extension}"

                # 2.- Guardamos la imagen
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

                # 3.- Agregamos a la base de datos
                db.create_foto(app.config["UPLOAD_FOLDER"], img_filename, id_nuevo_aviso)

            # Procedimiento para añadir los métodos y detalles del contacto a la base de datos.
            for i in range(len(metodo_contacto)):
                # 1.- Obtenemos el método de contacto con su respectivo detalle.
                metodo_i = metodo_contacto[i]
                detalle_i = detalle_contacto[i]

                # 2.- Agragamos a la base de datos.
                db.create_contactar_por(metodo_i, detalle_i, id_nuevo_aviso)

            # Refirigimos a la página principal.
            return redirect(url_for("avisos_recientes"))
    
    # Actualizar página.
    return render_template("agregar_aviso_adopcion/agregar_aviso.html")

# Función para publicar los 5 avisos mas recientes.
@app.route('/', methods=['GET'])
def avisos_recientes():
    # Pedimos los 5 avisos mas recientes.
    data = []
    # Se necesita: Fecha publicación, comuna, sector, cantidad, edad, tipo, foto
    for aviso in db.get_avisos_adopcion(n=5):

        foto = db.get_foto_by_id(aviso.id).first()

        # Caso para cuando no se especifica el sector
        sector = aviso.sector
        if sector == "":
            sector = "No se especifica"

        # Añadimos la info a data
        data.append({
            "fecha_publicacion": aviso.fecha_ingreso,
            "sector": sector,
            "cantidad": aviso.cantidad,
            "edad": aviso.edad,
            "tipo": aviso.tipo,
            "comuna": db.get_comuna_by_id(aviso.comuna_id).nombre,
            "foto": url_for('static', filename='uploads/' + foto.nombre_archivo)
        })
    
    # Actualizamos página.
    return render_template("portada/portada.html", data=data)

@app.route('/listado_avisos', methods=['GET'])
def listado_avisos():
    # Pagina actual, por defecto 1
    pagina = request.args.get('page', 1, type=int)

    # Obtenemos todos los avisos disponibles en la base de datos
    datos = []

    # Se necesita: Fecha publicion, fecha entrega, comuna, sector, cantidad, especie, edad, nombre, contacto, total fotos
    avisos_adopcion = db.get_slices_avisos_adopcion(comienzo=(pagina-1)*5, final=(pagina-1)*5+5)

    # Vemos todos los avisos
    for aviso in avisos_adopcion:
        # Obtenemos las fotos de cada aviso para contarlas
        foto = list(db.get_foto_by_id(aviso.id))

        # Caso para cuando no se especifica el sector
        sector = aviso.sector
        if sector == "":
            sector = "No se especifica"

        # Caso cuando telefono no se especifica
        fono = aviso.celular
        if fono == "":
            fono = "No se especifica"

        # Añadimos los datos
        datos.append({
            "id": aviso.id,
            "fecha_publicacion": aviso.fecha_ingreso,
            "fecha_entrega": aviso.fecha_entrega,
            "comuna": db.get_comuna_by_id(aviso.comuna_id).nombre,
            "sector": sector,
            "cantidad": aviso.cantidad,
            "tipo": aviso.tipo,
            "edad": aviso.edad,
            "nombre": aviso.nombre,
            "contacto": fono,
            "total_fotos": len(foto)
        })

    # Calculamos en cual página vamos y si debemos hacer un boton siguiente o anterior.
    total_avisos = db.get_total_avisos()
    pag_sig = pagina + 1 if pagina * 5 < total_avisos else None
    pag_ant = pagina - 1 if pagina > 1 else None

    return render_template('listado_aviso_adopcion/listado_aviso.html', datos=datos, pagina=pagina, pag_sig=pag_sig, pag_ant=pag_ant) 

# Detalle de cada aviso.
@app.route('/detalle_aviso', methods=['GET'])
def detalle_aviso():
    # Primero obtenemos el ID del aviso usando un request a la url
    id_aviso = request.args.get('ID', 0, type=int)

    # Reunimos los datos de las fotos.
    fotos = db.get_foto_by_id(id_aviso)
    datos_fotos = []
    for foto in fotos:
        datos_fotos.append({
            "url": url_for('static', filename='uploads/' + foto.nombre_archivo)
        })

    # Reunimos los datos de los contactos
    contactos = db.get_contacto_by_id(id_aviso)
    datos_contacto = []
    for contacto in contactos:
        datos_contacto.append({
            "plataforma": contacto.nombre,
            "contacto": contacto.identificador
        })

    # Finalmente los datos del aviso
    aviso = db.get_aviso_by_id(id_aviso)
    datos = []
    datos.append({
        "fecha_publicacion": aviso.fecha_ingreso,
        "fecha_entrega": aviso.fecha_entrega,
        "comuna": db.get_comuna_by_id(aviso.comuna_id).nombre,
        "sector": aviso.sector,
        "cantidad": aviso.cantidad,
        "tipo": aviso.tipo,
        "edad": aviso.edad,
        "nombre": aviso.nombre,
        "contacto": aviso.celular,
        "descripcion": aviso.descripcion,
        "region": db.get_region_by_id(db.get_comuna_by_id(aviso.comuna_id).region_id).nombre,
        "telefono": aviso.celular,
        "correo": aviso.email
    })

    # Mandamos todo al template para presentar la información.
    return render_template('detalle_aviso_adopcion/detalle_aviso.html', datos_fotos=datos_fotos, datos_contacto=datos_contacto, datos=datos, id_aviso=id_aviso)

# Agrega comentario a la base de datos
@app.route('/agregar_comentario', methods=["POST"])
@cross_origin(origin='127.0.0.1', supports_credentials=True)
def agregar_comentario():
    id_aviso = request.form.get("id_aviso", type=int)
    nombre = request.form.get("nombre_coment")
    texto = request.form.get("texto_coment")

    if not val.validacion_comentario(nombre, texto):
        return jsonify({"error": "Datos inválidos"}), 400

    fecha = db.create_comentario(id_aviso, nombre, texto)

    return jsonify({
        "comentario": {
            "nombre": nombre,
            "texto": texto,
            "fecha": fecha
        }
    })

@app.route('/get-comentarios-data', methods=["GET"])
@cross_origin(origin='127.0.0.1', supports_credentials=True)
def obtener_comentarios():
    id_aviso = request.args.get('id_aviso', type=int)

    comentarios = db.get_comentarios_by_id(id_aviso)

    print(comentarios)

    data = [
        {
            "nombre": comentario.nombre,
            "texto": comentario.texto,
            "fecha": comentario.fecha
        } 
        for comentario in comentarios
    ]

    return jsonify(data)
    

@app.route('/stats', methods=["GET"])
def estadisticas():
    return render_template('estadisticas_aviso_adopcion/estadisticas.html')

@app.route('/get-stats-data', methods=["GET"])
@cross_origin(origin='127.0.0.1', supports_credentials=True)
def obtener_datos_estadistica():
    # Obtenemos los datos de la BD
    avisos_diarios, total_perros_gatos, perros_gatos_mensual = db.get_estadisticas()

    # Datos 1er gráfico
    data_avisos_diarios = [
        {'fecha': str(fecha), 'cantidad': cantidad}
        for fecha, cantidad in avisos_diarios
    ]

    # Datos 2do gráfico
    data_total_perros_gatos = [
        {
            'cantidad_total_perros': total_perros_gatos.cantidad_perros,
            'cantidad_total_gatos': total_perros_gatos.cantidad_gatos
        }
    ]

    # Datos 3er gráfico
    data_perros_gatos_mensual = [
        {
            'fecha': str(fecha),
            'cantidad_gatos': cantidad,
            'cantidad_perros': tipo
        }
        for fecha, tipo, cantidad in perros_gatos_mensual
    ]

    # Comprimimos a un solo coso
    data = {
        'data_avisos_diarios': data_avisos_diarios,
        'data_total_perros_gatos': data_total_perros_gatos,
        'data_perros_gatos_mensual': data_perros_gatos_mensual
    }

    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)

    
    
