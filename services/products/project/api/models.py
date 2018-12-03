# services/products/project/api/models.py


from project import db


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    cantidad = db.Column(db.Integer(), nullable=False)
    precio = db.Column(db.Float(), nullable=False)
    descripcion = db.Column(db.String(128), nullable=False)
    categoria = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'active': self.active
        }

    def __init__(self, nombre, cantidad, precio, descripcion, categoria):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
