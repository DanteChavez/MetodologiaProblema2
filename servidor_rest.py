"""
SERVIDOR REST - Sistema UVShop
==============================
API REST para el sistema de comercio electrónico UVShop
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)

# Importar componentes del sistema
try:
    from modelo.bd import bd
    from modelo.proxy import proxy
    from modelo.inventario import inventario
    
    bd_instance = bd()
    proxy_instance = proxy(bd_instance)
    inventario_instance = inventario()
    print("✅ Sistema inicializado correctamente")
except Exception as e:
    print(f"⚠️ Advertencia al inicializar: {e}")
    bd_instance = None
    proxy_instance = None
    inventario_instance = None


@app.route('/api', methods=['GET'])
def api_info():
    """Información general de la API"""
    return jsonify({
        'mensaje': 'API REST UVShop - Sistema de Comercio Electrónico',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints_disponibles': {
            'usuarios': '/api/usuarios',
            'productos': '/api/productos', 
            'inventario': '/api/inventario',
            'pedidos': '/api/pedidos',
            'facturas': '/api/facturas',
            'casos_uso': {
                'factory_pedidos': '/api/casos-uso/factory-pedidos',
                'descuentos_avanzados': '/api/casos-uso/descuentos-avanzados',
                'sistema_beneficios': '/api/casos-uso/sistema-beneficios',
                'gestor_central': '/api/casos-uso/gestor-central'
            }
        }
    })


@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    """Obtener todos los usuarios registrados"""
    try:
        usuarios = []
        
        if bd_instance and hasattr(bd_instance, 'listaUsuarios'):
            for user_id, usuario in bd_instance.listaUsuarios.items():
                usuarios.append({
                    'id': user_id,
                    'nombre': getattr(usuario, 'nombre', 'Sin nombre'),
                    'direccion': getattr(usuario, 'direccion', 'Sin dirección'),
                    'tipo': getattr(usuario, 'tipoCliente', 'cliente')
                })
        
        return jsonify({
            'usuarios': usuarios,
            'total': len(usuarios),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener usuarios: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    """Obtener todos los productos disponibles"""
    try:
        productos_list = []
        
        if inventario_instance and hasattr(inventario_instance, 'itemsPrimero'):
            for producto in inventario_instance.itemsPrimero:
                productos_list.append({
                    'codigo': producto.getcodigo(),
                    'nombre': producto.getnombre(),
                    'precio': producto.getprecioUnitario(),
                    'stock': producto.getstock(),
                    'descripcion': f"Producto: {producto.getnombre()}"
                })
        
        return jsonify({
            'productos': productos_list,
            'total': len(productos_list),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener productos: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    """Obtener todos los pedidos del sistema"""
    try:
        pedidos_list = []
        
        # Buscar pedidos en proxy_instance primero
        if proxy_instance and hasattr(proxy_instance, 'listaPedidos'):
            for pedido_id, pedido in proxy_instance.listaPedidos.items():
                pedidos_list.append({
                    'idPedido': pedido.getidPedido(),
                    'idUsuario': pedido.getidUsuario(),
                    'direccion': pedido.getdireccion(),
                    'estado': pedido.getestado(),
                    'productos': pedido.getproductos()
                })
        
        # Si no hay pedidos en proxy, buscar en bd_instance
        if not pedidos_list and bd_instance and hasattr(bd_instance, 'listaPedidos'):
            for pedido_id, pedido in bd_instance.listaPedidos.items():
                pedidos_list.append({
                    'idPedido': pedido.getidPedido(),
                    'idUsuario': pedido.getidUsuario(),
                    'direccion': pedido.getdireccion(),
                    'estado': pedido.getestado(),
                    'productos': pedido.getproductos()
                })
        
        return jsonify({
            'pedidos': pedidos_list,
            'total': len(pedidos_list),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener pedidos: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/casos-uso/factory-pedidos', methods=['GET'])
def obtener_tipos_pedido_factory():
    """Obtener tipos de pedido disponibles (Factory Pattern)"""
    try:
        from controlador.factory_tipos_pedido import FactoryTiposPedido
        
        tipos_disponibles = FactoryTiposPedido.obtener_tipos_disponibles()
        
        return jsonify({
            'tipos_pedido_disponibles': tipos_disponibles,
            'patron_utilizado': 'Factory Pattern',
            'descripcion': 'Tipos de pedido extendidos sin modificar código existente',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al obtener tipos de pedido: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


# =================== MÉTODOS POST ===================

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    """Crear un nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Validar campos requeridos
        campos_requeridos = ['nombre', 'direccion', 'tipo']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({'error': f'Campo requerido: {campo}'}), 400
        
        # Crear usuario usando el método del sistema original
        if proxy_instance:
            nuevo_id = proxy_instance.nuevoUsuario(
                data['nombre'], 
                data['direccion'], 
                data['tipo']
            )
            
            return jsonify({
                'mensaje': 'Usuario creado exitosamente',
                'usuario': {
                    'id': nuevo_id,
                    'nombre': data['nombre'],
                    'direccion': data['direccion'],
                    'tipo': data['tipo']
                },
                'timestamp': datetime.now().isoformat()
            }), 201
        else:
            return jsonify({'error': 'Sistema no disponible'}), 500
        
    except Exception as e:
        return jsonify({
            'error': f'Error al crear usuario: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/productos', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Validar campos requeridos  
        campos_requeridos = ['nombre', 'codigo', 'precio', 'stock']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({'error': f'Campo requerido: {campo}'}), 400
        
        # Crear producto usando la estructura original
        from modelo.productos import productos
        nuevo_producto = productos(
            data['nombre'],
            data['codigo'], 
            data['precio'],
            data['stock']
        )
        
        # Agregar al inventario
        if inventario_instance:
            # Agregar a la lista principal
            if hasattr(inventario_instance, 'itemsPrimero'):
                inventario_instance.itemsPrimero.append(nuevo_producto)
            # Agregar al diccionario por nombre
            if hasattr(inventario_instance, 'items'):
                inventario_instance.items[nuevo_producto.getnombre()] = nuevo_producto
        
        return jsonify({
            'mensaje': 'Producto creado exitosamente',
            'producto': {
                'codigo': nuevo_producto.getcodigo(),
                'nombre': nuevo_producto.getnombre(),
                'precio': nuevo_producto.getprecioUnitario(),
                'stock': nuevo_producto.getstock()
            },
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'Error al crear producto: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    """Crear un nuevo pedido"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Validar campos requeridos
        campos_requeridos = ['idUsuario', 'direccion', 'productos']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({'error': f'Campo requerido: {campo}'}), 400
        
        # Crear pedido
        from modelo.pedido import pedido
        import random
        
        nuevo_id_pedido = random.randint(1000, 9999)
        
        nuevo_pedido = pedido(
            data['idUsuario'],      # idUsuario
            data['direccion'],      # direccion
            nuevo_id_pedido,        # idPedido
            data.get('estado', 'pendiente'),  # estado
            data['productos'],      # productos
            data.get('precioEnvio', None),  # precioEnvio
            data.get('factura', None)       # factura
        )
        
        # Agregar a la base de datos
        if proxy_instance:
            proxy_instance.agregarPedido(nuevo_pedido)
        
        return jsonify({
            'mensaje': 'Pedido creado exitosamente',
            'pedido': {
                'idUsuario': nuevo_pedido.getidUsuario(),
                'direccion': nuevo_pedido.getdireccion(),
                'idPedido': nuevo_pedido.getidPedido(),
                'estado': nuevo_pedido.getestado(),
                'productos': nuevo_pedido.getproductos()
            },
            'timestamp': datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'Error al crear pedido: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


# =================== MÉTODOS PUT ===================

@app.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
def actualizar_pedido(pedido_id):
    """Actualizar un pedido existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Buscar pedido (primero en proxy, luego en bd)
        pedido_encontrado = None
        
        # Buscar en proxy primero (cache)
        if proxy_instance and hasattr(proxy_instance, 'listaPedidos'):
            if pedido_id in proxy_instance.listaPedidos:
                pedido_encontrado = proxy_instance.listaPedidos[pedido_id]
            else:
                for pedido_key, pedido in proxy_instance.listaPedidos.items():
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_encontrado = pedido
                        break
        
        # Si no se encontró en proxy, buscar en bd_instance
        if not pedido_encontrado and bd_instance and hasattr(bd_instance, 'listaPedidos'):
            if pedido_id in bd_instance.listaPedidos:
                pedido_encontrado = bd_instance.listaPedidos[pedido_id]
            else:
                for pedido_key, pedido in bd_instance.listaPedidos.items():
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_encontrado = pedido
                        break
        
        if not pedido_encontrado:
            return jsonify({'error': 'Pedido no encontrado'}), 404
        
        # Actualizar campos usando los métodos del objeto pedido
        if 'direccion' in data:
            pedido_encontrado.setdireccion(data['direccion'])
        if 'estado' in data:
            pedido_encontrado.setestado(data['estado'])
        if 'productos' in data:
            pedido_encontrado.setproductos(data['productos'])
        
        return jsonify({
            'mensaje': 'Pedido actualizado exitosamente',
            'pedido': {
                'idPedido': pedido_encontrado.getidPedido(),
                'idUsuario': pedido_encontrado.getidUsuario(),
                'direccion': pedido_encontrado.getdireccion(),
                'estado': pedido_encontrado.getestado(),
                'productos': pedido_encontrado.getproductos()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al actualizar pedido: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/productos/<string:producto_codigo>', methods=['PUT'])
def actualizar_producto(producto_codigo):
    """Actualizar un producto existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Buscar producto en el inventario
        producto_encontrado = None
        if inventario_instance and hasattr(inventario_instance, 'itemsPrimero'):
            for producto in inventario_instance.itemsPrimero:
                if str(producto.getcodigo()) == str(producto_codigo):
                    producto_encontrado = producto
                    break
        
        if not producto_encontrado:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        # Actualizar campos (usando los setters si existen, o directamente los atributos)
        if 'nombre' in data:
            producto_encontrado.nombre = data['nombre']
        if 'precio' in data:
            producto_encontrado.precioUnitario = data['precio']
        if 'stock' in data:
            producto_encontrado.stock = data['stock']
        
        return jsonify({
            'mensaje': 'Producto actualizado exitosamente',
            'producto': {
                'codigo': producto_encontrado.getcodigo(),
                'nombre': producto_encontrado.getnombre(),
                'precio': producto_encontrado.getprecioUnitario(),
                'stock': producto_encontrado.getstock()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al actualizar producto: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


# =================== MÉTODOS DELETE ===================

@app.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
def eliminar_pedido(pedido_id):
    """Eliminar un pedido"""
    try:
        # Buscar y eliminar pedido (primero en proxy, luego en bd)
        pedido_eliminado = None
        
        # Buscar en proxy primero
        if proxy_instance and hasattr(proxy_instance, 'listaPedidos'):
            if pedido_id in proxy_instance.listaPedidos:
                pedido_eliminado = proxy_instance.listaPedidos.pop(pedido_id)
            else:
                # Buscar por ID del pedido
                for key, pedido in list(proxy_instance.listaPedidos.items()):
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_eliminado = proxy_instance.listaPedidos.pop(key)
                        break
        
        # Si no se encontró en proxy, buscar en bd_instance
        if not pedido_eliminado and bd_instance and hasattr(bd_instance, 'listaPedidos'):
            if pedido_id in bd_instance.listaPedidos:
                pedido_eliminado = bd_instance.listaPedidos.pop(pedido_id)
            else:
                # Buscar por ID del pedido
                for key, pedido in list(bd_instance.listaPedidos.items()):
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_eliminado = bd_instance.listaPedidos.pop(key)
                        break
        
        if not pedido_eliminado:
            return jsonify({'error': 'Pedido no encontrado'}), 404
        
        return jsonify({
            'mensaje': 'Pedido eliminado exitosamente',
            'pedido_eliminado': {
                'idPedido': pedido_eliminado.getidPedido(),
                'direccion': pedido_eliminado.getdireccion(),
                'estado': pedido_eliminado.getestado()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al eliminar pedido: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/productos/<string:producto_codigo>', methods=['DELETE'])
def eliminar_producto(producto_codigo):
    """Eliminar un producto"""
    try:
        # Buscar y eliminar producto del inventario
        producto_eliminado = None
        if inventario_instance and hasattr(inventario_instance, 'itemsPrimero'):
            for i, producto in enumerate(inventario_instance.itemsPrimero):
                if str(producto.getcodigo()) == str(producto_codigo):
                    producto_eliminado = inventario_instance.itemsPrimero.pop(i)
                    # También eliminar del diccionario
                    if hasattr(inventario_instance, 'items') and producto_eliminado.getnombre() in inventario_instance.items:
                        del inventario_instance.items[producto_eliminado.getnombre()]
                    break
        
        if not producto_eliminado:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        return jsonify({
            'mensaje': 'Producto eliminado exitosamente',
            'producto_eliminado': {
                'codigo': producto_eliminado.getcodigo(),
                'nombre': producto_eliminado.getnombre()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al eliminar producto: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


# =================== MÉTODOS PATCH ===================

@app.route('/api/pedidos/<int:pedido_id>/estado', methods=['PATCH'])
def cambiar_estado_pedido(pedido_id):
    """Cambiar solo el estado de un pedido"""
    try:
        data = request.get_json()
        
        if not data or 'estado' not in data:
            return jsonify({'error': 'Se requiere el campo estado'}), 400
        
        # Buscar pedido (primero en proxy, luego en bd)
        pedido_encontrado = None
        
        # Buscar en proxy primero (cache)
        if proxy_instance and hasattr(proxy_instance, 'listaPedidos'):
            if pedido_id in proxy_instance.listaPedidos:
                pedido_encontrado = proxy_instance.listaPedidos[pedido_id]
            else:
                for pedido_id_key, pedido in proxy_instance.listaPedidos.items():
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_encontrado = pedido
                        break
        
        # Si no se encontró en proxy, buscar en bd_instance
        if not pedido_encontrado and bd_instance and hasattr(bd_instance, 'listaPedidos'):
            if pedido_id in bd_instance.listaPedidos:
                pedido_encontrado = bd_instance.listaPedidos[pedido_id]
            else:
                for pedido_id_key, pedido in bd_instance.listaPedidos.items():
                    # getidPedido() devuelve (valor, status_code), necesitamos solo el valor
                    pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                    if pedido_id_actual == pedido_id:
                        pedido_encontrado = pedido
                        break
        
        if not pedido_encontrado:
            return jsonify({'error': 'Pedido no encontrado'}), 404
        
        estado_anterior = pedido_encontrado.getestado()
        pedido_encontrado.setestado(data['estado'])
        
        return jsonify({
            'mensaje': 'Estado del pedido actualizado',
            'pedido_id': pedido_id,
            'estado_anterior': estado_anterior,
            'estado_nuevo': data['estado'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error al cambiar estado: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/metodos', methods=['GET'])
def obtener_metodos_disponibles():
    """Obtener todos los métodos HTTP disponibles"""
    return jsonify({
        'metodos_http_soportados': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        'endpoints_por_metodo': {
            'GET': [
                '/api - Información de la API',
                '/api/usuarios - Lista de usuarios',
                '/api/productos - Lista de productos',
                '/api/pedidos - Lista de pedidos',
                '/api/casos-uso/factory-pedidos - Factory Pattern'
            ],
            'POST': [
                '/api/usuarios - Crear nuevo usuario',
                '/api/productos - Crear nuevo producto',
                '/api/pedidos - Crear nuevo pedido'
            ],
            'PUT': [
                '/api/productos/<codigo> - Actualizar producto completo',
                '/api/pedidos/<id> - Actualizar pedido completo'
            ],
            'DELETE': [
                '/api/productos/<codigo> - Eliminar producto',
                '/api/pedidos/<id> - Eliminar pedido'
            ],
            'PATCH': [
                '/api/pedidos/<id>/estado - Cambiar solo el estado del pedido'
            ]
        },
        'ejemplos_uso': {
            'POST_usuario': {
                'url': '/api/usuarios',
                'method': 'POST',
                'body': {
                    'nombre': 'Juan Pérez',
                    'direccion': 'Calle 123',
                    'tipo': 'cliente'
                }
            },
            'POST_producto': {
                'url': '/api/productos',
                'method': 'POST',
                'body': {
                    'nombre': 'Laptop Gaming',
                    'codigo': 'LAP001',
                    'precio': 1299.99,
                    'stock': 10
                }
            },
            'PUT_producto': {
                'url': '/api/productos/LAP001',
                'method': 'PUT',
                'body': {
                    'nombre': 'Laptop Gaming Pro',
                    'precio': 1499.99,
                    'stock': 15
                }
            }
        },
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Manejador de errores 404"""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'mensaje': 'La URL solicitada no existe en esta API',
        'endpoints_disponibles': '/api',
        'timestamp': datetime.now().isoformat()
    }), 404


if __name__ == '__main__':
    print("🚀 Iniciando servidor REST UVShop...")
    print("📡 API disponible en: http://localhost:5000/api")
    app.run(host='0.0.0.0', port=5000, debug=False)