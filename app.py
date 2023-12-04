# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow

# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)


# Configura la URI de la base de datos con el driver de MySQL, usuario, contraseña y nombre de la base de datos
# URI de la BD == Driver de la BD://user:password@UrlBD/nombreBD
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/proyecto"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ruta23@localhost/excursiones"
# Configura el seguimiento de modificaciones de SQLAlchemy a False para mejorar el rendimiento
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Crea una instancia de la clase SQLAlchemy y la asigna al objeto db para interactuar con la base de datos
db = SQLAlchemy(app)
# Crea una instancia de la clase Marshmallow y la asigna al objeto ma para trabajar con serialización y deserialización de datos
ma = Marshmallow(app)

class Proyecto(db.Model):  # Producto hereda de db.Model
    """
    Definición de la tabla Producto en la base de datos.
    La clase Producto hereda de db.Model.
    Esta clase representa la tabla "Producto" en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    foto = db.Column(db.String(400))
    descripcion = db.Column(db.String(400))
    
    def __init__(self, nombre, foto, descripcion):
        """
        Constructor de la clase Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (int): Precio del producto.
            stock (int): Cantidad en stock del producto.
            imagen (str): URL o ruta de la imagen del producto.
        """
        self.nombre = nombre
        self.foto = foto
        self.descripcion = descripcion

    # Se pueden agregar más clases para definir otras tablas en la base de datos

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Producto
class ProyectoSchema(ma.Schema):
    """
    Esquema de la clase Proyecto.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Proyecto.
    """
    class Meta:
        fields = ("id", "nombre", "foto", "descripcion")

proyecto_schema = ProyectoSchema()  # Objeto para serializar/deserializar un producto
proyectos_schema = ProyectoSchema(many=True)  # Objeto para serializar/deserializar múltiples productos


'''
Este código define un endpoint que permite obtener todos los productos de la base de datos y los devuelve como un JSON en respuesta a una solicitud GET a la ruta /productos.
@app.route("/productos", methods=["GET"]): Este decorador establece la ruta /productos para este endpoint y especifica que solo acepta solicitudes GET.
def get_Productos(): Esta es la función asociada al endpoint. Se ejecuta cuando se realiza una solicitud GET a la ruta /productos.
all_productos = Producto.query.all(): Se obtienen todos los registros de la tabla de productos mediante la consulta Producto.query.all(). Esto se realiza utilizando el modelo Producto que representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza para obtener todos los registros de la tabla.
result = productos_schema.dump(all_productos): Los registros obtenidos se serializan en formato JSON utilizando el método dump() del objeto productos_schema. El método dump() heredado de ma.Schema se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''
@app.route("/proyectos", methods=["GET"])
def get_Proyectos():
    """
    Endpoint para obtener todos los productos de la base de datos.

    Retorna un JSON con todos los registros de la tabla de productos.
    """
    all_proyectos = Proyecto.query.all()  # Obtiene todos los registros de la tabla de productos
    result = proyectos_schema.dump(all_proyectos)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

'''
El código que sigue a continuación termina de resolver la API de gestión de productos, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de productos:
get_producto(id):
    # Obtiene un producto específico de la base de datos
    # Retorna un JSON con la información del producto correspondiente al ID proporcionado
delete_producto(id):
    # Elimina un producto de la base de datos
    # Retorna un JSON con el registro eliminado del producto correspondiente al ID proporcionado
create_producto():
    # Crea un nuevo producto en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto
    # Retorna un JSON con el nuevo producto creado
update_producto(id):
    # Actualiza un producto existente en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado
    # Retorna un JSON con el producto actualizado

'''
@app.route("/proyectos/<id>", methods=["GET"])
def get_proyecto(id):
    """
    Endpoint para obtener un producto específico de la base de datos.

    Retorna un JSON con la información del producto correspondiente al ID proporcionado.
    """
    producto = Proyecto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    return proyecto_schema.jsonify(producto)  # Retorna el JSON del producto

@app.route("/proyectos/<id>", methods=["DELETE"])
def delete_proyecto(id):
    """
    Endpoint para eliminar un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    proyecto = Proyecto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    db.session.delete(proyecto)  # Elimina el producto de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return proyecto_schema.jsonify(proyecto)  # Retorna el JSON del producto eliminado

@app.route("/proyectos", methods=["POST"])  # Endpoint para crear un producto
def create_proyecto():
    """
    Endpoint para crear un nuevo producto en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto en la base de datos.
    Retorna un JSON con el nuevo producto creado.
    """
    nombre = request.json["nombre"]  # Obtiene el nombre del producto del JSON proporcionado
    foto = request.json["foto"]  # Obtiene el precio del producto del JSON proporcionado
    descripcion = request.json["descripcion"]  # Obtiene el stock del producto del JSON proporcionado
    new_proyecto = Proyecto(nombre, foto, descripcion)  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_proyecto)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return proyecto_schema.jsonify(new_proyecto)  # Retorna el JSON del nuevo producto creado

@app.route("/proyectos/<id>", methods=["PUT"])  # Endpoint para actualizar un producto
def update_proyecto(id):
    """
    Endpoint para actualizar un producto existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado.
    Retorna un JSON con el producto actualizado.
    """
    proyecto = Proyecto.query.get(id)  # Obtiene el producto existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    proyecto.nombre = request.json["nombre"]
    proyecto.foto = request.json["foto"]
    proyecto.descripcion = request.json["descripcion"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return proyecto_schema.jsonify(proyecto)  # Retorna el JSON del producto actualizado

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)