# services/products/project/tests/test_products.py


import json
import unittest

from project.tests.base import BaseTestCase

from project import db
from project.api.models import Product


def add_product(nombre, cantidad, precio, descripcion, categoria):
    product = Product(
        nombre=nombre,
        cantidad=cantidad,
        precio=precio,
        descripcion=descripcion,
        categoria=categoria
    )
    db.session.add(product)
    db.session.commit()
    return product


class TestProductService(BaseTestCase):
    """Pruebas para el Servicio de Productos """

    def test_products(self):
        """comprobado que la ruta /ping funcione correctamente."""
        response = self.client.get('/products/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Conectado exitosamente!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_product(self):
        """ Asegurando que se pueda agregar
         un nuevo producto a la base de datos"""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'soda',
                    'cantidad': 12,
                    'precio': 0.12,
                    'descripcion': 'esta rico',
                    'categoria': 'Galletas'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'soda fue agregado!!!',
                data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])

    def test_add_product_invalid_json(self):
        """Asegurando de que se lance un error
         cuando el objeto JSON esta vacío."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_product_invalid_json_keys(self):
        """Asegurando de que se produce un error si el
         objeto JSON no tiene una clave de nombre de
          producto."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({'nombre': 'soda'}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga inválida.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_add_product_duplicate_name(self):
        """Asegurando que se produce un error si
         el nombre ya existe."""
        with self.client:
            self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'soda',
                    'cantidad': 12,
                    'precio': 0.12,
                    'descripcion': 'esta rico',
                    'categoria': 'Galletas'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nombre': 'soda',
                    'cantidad': 12,
                    'precio': 0.12,
                    'descripcion': 'estado rico',
                    'categoria': 'Galletas'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento, ese nombre ya existe.', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_single_product(self):
        """Asegurando que el producto único se comporte
         correctamente."""
        product = add_product('soda', 12, 0.12, 'esta rico', 'Galletas')
        with self.client:
            response = self.client.get(f'/products/{product.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('soda', data['data']['nombre'])
            self.assertEqual(12, data['data']['cantidad'])
            self.assertEqual(0.12, data['data']['precio'])
            self.assertIn(
                'esta rico',
                data['data']['descripcion'])
            self.assertIn(
                'Galletas',
                data['data']['categoria']
                )
            self.assertIn('satisfactorio', data['estado'])

    def test_single_product_no_id(self):
        """Asegúrese de que se arroje un error si
         no se proporciona una identificación."""
        with self.client:
            response = self.client.get('/products/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn(
                'El producto no existe',
                data['mensaje']
                )
            self.assertIn('falló', data['estado'])

    def test_single_product_incorrect_id(self):
        """Asegurando de que se arroje un error si
         la identificación no existe."""
        with self.client:
            response = self.client.get('/products/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El producto no existe', data['mensaje'])
            self.assertIn('falló', data['estado'])

    def test_all_products(self):
        """Asegurando obtener todos los productos
         correctamente."""
        add_product('soda', 12, 0.12, 'esta rico', 'Galletas')
        add_product('soda field', 20, 0.7, 'esta buenaso', 'Galletas')
        with self.client:
            response = self.client.get('/products')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['products']), 2)
            self.assertIn(
                'soda',
                data['data']['products'][0]['nombre']
                )
            self.assertEqual(
                12,
                data['data']['products'][0]['cantidad']
                )
            self.assertEqual(
                0.12,
                data['data']['products'][0]['precio']
                )
            self.assertIn(
                'esta rico',
                data['data']['products'][0]['descripcion']
                )
            self.assertIn(
                'Galletas',
                data['data']['products'][0]['categoria']
                )
            self.assertIn(
                'soda field',
                data['data']['products'][1]['nombre']
                )
            self.assertEqual(
                20,
                data['data']['products'][1]['cantidad']
                )
            self.assertEqual(
                0.7,
                data['data']['products'][1]['precio']
                )
            self.assertIn(
                'esta buenaso',
                data['data']['products'][1]['descripcion']
                )
            self.assertIn(
                'Galletas',
                data['data']['products'][1]['categoria']
                )

    def test_main_no_products(self):
        """Asegura que la ruta principal actua
         correctamente cuando no hay productos en
          la base de datos"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Products', response.data)
        self.assertIn(
            b'<p>No hay productos!</p>',
            response.data
            )

    def test_main_with_products(self):
        """Asegura que la ruta principal actua
         correctamente cuando hay productos en la
          base de datos"""
        add_product('soda fresa', 16, 0.7, 'esta feo', 'Galletas')
        add_product('Tentacion', 30, 0.5, 'esta masomenos', 'Galletas')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Products', response.data)
            self.assertNotIn(
                b'<p>No hay productos!</p>',
                response.data
                )
            self.assertIn(b'soda fresa', response.data)
            self.assertIn(b'Tentacion', response.data)

    def test_main_add_product(self):
        """Asegura que un nuevo producto puede ser
         agregado a la db"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    nombre='Coca Cola personal de vidrio',
                    cantidad=35,
                    precio=2.5,
                    descripcion='esta refrescante',
                    categoria='Gaseosas'
                    ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Products', response.data)
            self.assertNotIn(
                b'<p>No hay productos!</p>',
                response.data
                )
            self.assertIn(b'Coca Cola personal de vidrio', response.data)


if __name__ == '__main__':
    unittest.main()
