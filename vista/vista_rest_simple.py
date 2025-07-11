"""
VISTA REST SIMPLIFICADA - Sistema UVShop MVC
============================================
Vista REST que sigue el patrón MVC correctamente (versión simplificada)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Importar modelos base para inicialización
from modelo.bd import bd
from modelo.proxy import proxy
from modelo.inventario import inventario

class VistaRESTSimple:
    """Vista REST simplificada que sigue el patrón MVC"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Inicializar SOLO los modelos base
        self.inicializar_sistema()
        
        # Inicializar controladores de forma segura
        self.inicializar_controladores()
        
        # Registrar rutas
        self.registrar_rutas()
    
    def inicializar_sistema(self):
        """Inicializar componentes del sistema"""
        try:
            self.bd_instance = bd()
            self.proxy_instance = proxy(self.bd_instance)
            self.inventario_instance = inventario()
            print("✅ Sistema MVC base inicializado correctamente")
        except Exception as e:
            print(f"⚠️ Error al inicializar sistema: {e}")
            raise
    
    def inicializar_controladores(self):
        """Inicializar controladores de forma segura"""
        try:
            # Controlador principal (simplificado)
            from controlador.gestionPedidosUsuarios import gestionPedidosUsuarios
            self.gestor_usuarios = gestionPedidosUsuarios(self.proxy_instance, None)
            print("✅ Controlador principal inicializado")
        except Exception as e:
            print(f"⚠️ Error al inicializar controlador principal: {e}")
            self.gestor_usuarios = None
        
        # Controladores opcionales
        self.gestor_dueno = None
        self.factory_pedidos = None
    
    def registrar_rutas(self):
        """Registrar todas las rutas REST usando controladores"""
        
        # =================== INFORMACIÓN API ===================
        @self.app.route('/api', methods=['GET'])
        def api_info():
            return jsonify({
                'mensaje': 'API REST UVShop - Arquitectura MVC (Simplificada)',
                'version': '2.1',
                'arquitectura': 'Model-View-Controller (MVC)',
                'estado': 'Funcional y estable',
                'controladores_activos': {
                    'gestor_usuarios': self.gestor_usuarios is not None,
                    'proxy_instance': self.proxy_instance is not None,
                    'bd_instance': self.bd_instance is not None
                },
                'timestamp': datetime.now().isoformat(),
                'endpoints': self._obtener_endpoints_disponibles()
            })
        
        # =================== USUARIOS ===================
        @self.app.route('/api/usuarios', methods=['GET'])
        def obtener_usuarios():
            try:
                usuarios = []
                if self.bd_instance and hasattr(self.bd_instance, 'listaUsuarios'):
                    for user_id, usuario in self.bd_instance.listaUsuarios.items():
                        usuarios.append({
                            'id': user_id,
                            'nombre': getattr(usuario, 'nombre', 'Sin nombre'),
                            'direccion': getattr(usuario, 'direccion', 'Sin dirección'),
                            'tipo': getattr(usuario, 'tipoCliente', 'cliente')
                        })
                
                return jsonify({
                    'usuarios': usuarios,
                    'total': len(usuarios),
                    'arquitectura': 'MVC - Acceso via modelo controlado',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error al obtener usuarios: {str(e)}')
        
        @self.app.route('/api/usuarios', methods=['POST'])
        def crear_usuario():
            try:
                data = request.get_json()
                if not data:
                    return self._error_response('No se recibieron datos', 400)
                
                # Validar campos requeridos
                campos_requeridos = ['nombre', 'direccion', 'tipo']
                for campo in campos_requeridos:
                    if campo not in data:
                        return self._error_response(f'Campo requerido: {campo}', 400)
                
                # Usar proxy (controlador de acceso a datos) para crear usuario
                nuevo_id = self.proxy_instance.nuevoUsuario(
                    data['nombre'], 
                    data['direccion'], 
                    data['tipo']
                )
                
                return jsonify({
                    'mensaje': 'Usuario creado exitosamente via controlador MVC',
                    'usuario': {
                        'id': nuevo_id,
                        'nombre': data['nombre'],
                        'direccion': data['direccion'],
                        'tipo': data['tipo']
                    },
                    'controlador_usado': 'proxy->bd (MVC)',
                    'timestamp': datetime.now().isoformat()
                }), 201
                
            except Exception as e:
                return self._error_response(f'Error al crear usuario: {str(e)}')
        
        # =================== PRODUCTOS ===================
        @self.app.route('/api/productos', methods=['GET'])
        def obtener_productos():
            try:
                productos_list = []
                
                if self.inventario_instance and hasattr(self.inventario_instance, 'itemsPrimero'):
                    for producto in self.inventario_instance.itemsPrimero:
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
                    'modelo_usado': 'inventario (MVC)',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error al obtener productos: {str(e)}')
        
        @self.app.route('/api/productos', methods=['POST'])
        def crear_producto():
            try:
                data = request.get_json()
                if not data:
                    return self._error_response('No se recibieron datos', 400)
                
                # Validar campos requeridos  
                campos_requeridos = ['nombre', 'codigo', 'precio', 'stock']
                for campo in campos_requeridos:
                    if campo not in data:
                        return self._error_response(f'Campo requerido: {campo}', 400)
                
                # Crear producto usando modelo
                from modelo.productos import productos
                nuevo_producto = productos(
                    data['nombre'],
                    data['codigo'], 
                    data['precio'],
                    data['stock']
                )
                
                # Agregar al inventario (modelo)
                if self.inventario_instance:
                    if hasattr(self.inventario_instance, 'itemsPrimero'):
                        self.inventario_instance.itemsPrimero.append(nuevo_producto)
                    if hasattr(self.inventario_instance, 'items'):
                        self.inventario_instance.items[nuevo_producto.getnombre()] = nuevo_producto
                
                return jsonify({
                    'mensaje': 'Producto creado exitosamente via modelo MVC',
                    'producto': {
                        'codigo': nuevo_producto.getcodigo(),
                        'nombre': nuevo_producto.getnombre(),
                        'precio': nuevo_producto.getprecioUnitario(),
                        'stock': nuevo_producto.getstock()
                    },
                    'timestamp': datetime.now().isoformat()
                }), 201
                
            except Exception as e:
                return self._error_response(f'Error al crear producto: {str(e)}')
        
        # =================== PEDIDOS ===================
        @self.app.route('/api/pedidos', methods=['GET'])
        def obtener_pedidos():
            try:
                pedidos_list = []
                
                # A través del proxy (controlador de acceso a datos)
                if self.proxy_instance and hasattr(self.proxy_instance, 'listaPedidos'):
                    for pedido_id, pedido in self.proxy_instance.listaPedidos.items():
                        pedidos_list.append({
                            'idPedido': pedido.getidPedido(),
                            'idUsuario': pedido.getidUsuario(),
                            'direccion': pedido.getdireccion(),
                            'estado': pedido.getestado(),
                            'productos': pedido.getproductos()
                        })
                
                # Si no hay en proxy, usar bd (modelo)
                if not pedidos_list and self.bd_instance and hasattr(self.bd_instance, 'listaPedidos'):
                    for pedido_id, pedido in self.bd_instance.listaPedidos.items():
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
                    'controlador_usado': 'proxy->bd (MVC)',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error al obtener pedidos: {str(e)}')
        
        @self.app.route('/api/pedidos', methods=['POST'])
        def crear_pedido():
            try:
                data = request.get_json()
                if not data:
                    return self._error_response('No se recibieron datos', 400)
                
                # Usar controlador si está disponible, sino usar método directo
                if self.gestor_usuarios:
                    resultado = self.gestor_usuarios.crearPedido(
                        data.get('idUsuario'),
                        data.get('direccion'),
                        data.get('productos', []),
                        data.get('estado', 'pendiente')
                    )
                    
                    if resultado and resultado != 400:
                        return jsonify({
                            'mensaje': 'Pedido creado exitosamente via controlador MVC',
                            'pedido': resultado,
                            'controlador_usado': 'gestionPedidosUsuarios (MVC)',
                            'timestamp': datetime.now().isoformat()
                        }), 201
                    else:
                        return self._error_response('Error al crear pedido via controlador', 400)
                else:
                    # Método alternativo usando modelo directamente
                    from modelo.pedido import pedido
                    import random
                    
                    nuevo_id_pedido = random.randint(1000, 9999)
                    
                    nuevo_pedido = pedido(
                        data.get('idUsuario'),
                        data.get('direccion'),
                        nuevo_id_pedido,
                        data.get('estado', 'pendiente'),
                        data.get('productos', []),
                        None, None
                    )
                    
                    if self.proxy_instance:
                        self.proxy_instance.agregarPedido(nuevo_pedido)
                    
                    return jsonify({
                        'mensaje': 'Pedido creado exitosamente via modelo directo',
                        'pedido': {
                            'idPedido': nuevo_pedido.getidPedido(),
                            'idUsuario': nuevo_pedido.getidUsuario(),
                            'direccion': nuevo_pedido.getdireccion(),
                            'estado': nuevo_pedido.getestado(),
                            'productos': nuevo_pedido.getproductos()
                        },
                        'metodo_usado': 'modelo_directo (fallback)',
                        'timestamp': datetime.now().isoformat()
                    }), 201
                    
            except Exception as e:
                return self._error_response(f'Error al crear pedido: {str(e)}')
        
        # =================== MÉTODOS DISPONIBLES ===================
        @self.app.route('/api/metodos', methods=['GET'])
        def obtener_metodos_disponibles():
            """Obtener todos los métodos HTTP disponibles"""
            return jsonify({
                'metodos_http_soportados': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                'arquitectura': 'MVC (Model-View-Controller)',
                'endpoints_por_metodo': {
                    'GET': [
                        '/api - Información de la API MVC',
                        '/api/metodos - Lista de métodos disponibles',
                        '/api/usuarios - Lista de usuarios',
                        '/api/productos - Lista de productos',
                        '/api/pedidos - Lista de pedidos'
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
                    'PUT_producto': {
                        'url': '/api/productos/<codigo>',
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
        
        # =================== PUT - ACTUALIZAR COMPLETO ===================
        @self.app.route('/api/productos/<string:producto_codigo>', methods=['PUT'])
        def actualizar_producto(producto_codigo):
            """Actualizar un producto existente"""
            try:
                data = request.get_json()
                
                if not data:
                    return self._error_response('No se recibieron datos', 400)
                
                # Buscar producto en el inventario
                producto_encontrado = None
                if self.inventario_instance and hasattr(self.inventario_instance, 'itemsPrimero'):
                    for producto in self.inventario_instance.itemsPrimero:
                        if str(producto.getcodigo()) == str(producto_codigo):
                            producto_encontrado = producto
                            break
                
                if not producto_encontrado:
                    return self._error_response('Producto no encontrado', 404)
                
                # Actualizar campos
                if 'nombre' in data:
                    producto_encontrado.nombre = data['nombre']
                if 'precio' in data:
                    producto_encontrado.precioUnitario = data['precio']
                if 'stock' in data:
                    producto_encontrado.stock = data['stock']
                
                return jsonify({
                    'mensaje': 'Producto actualizado exitosamente via MVC',
                    'producto': {
                        'codigo': producto_encontrado.getcodigo(),
                        'nombre': producto_encontrado.getnombre(),
                        'precio': producto_encontrado.getprecioUnitario(),
                        'stock': producto_encontrado.getstock()
                    },
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return self._error_response(f'Error al actualizar producto: {str(e)}')
        
        @self.app.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
        def actualizar_pedido(pedido_id):
            """Actualizar un pedido existente"""
            try:
                data = request.get_json()
                
                if not data:
                    return self._error_response('No se recibieron datos', 400)
                
                # Buscar pedido en proxy y bd
                pedido_encontrado = None
                
                # Buscar en proxy primero
                if self.proxy_instance and hasattr(self.proxy_instance, 'listaPedidos'):
                    if pedido_id in self.proxy_instance.listaPedidos:
                        pedido_encontrado = self.proxy_instance.listaPedidos[pedido_id]
                    else:
                        for pedido_key, pedido in self.proxy_instance.listaPedidos.items():
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_encontrado = pedido
                                break
                
                # Si no se encontró en proxy, buscar en bd
                if not pedido_encontrado and self.bd_instance and hasattr(self.bd_instance, 'listaPedidos'):
                    if pedido_id in self.bd_instance.listaPedidos:
                        pedido_encontrado = self.bd_instance.listaPedidos[pedido_id]
                    else:
                        for pedido_key, pedido in self.bd_instance.listaPedidos.items():
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_encontrado = pedido
                                break
                
                if not pedido_encontrado:
                    return self._error_response('Pedido no encontrado', 404)
                
                # Actualizar campos
                if 'direccion' in data:
                    pedido_encontrado.setdireccion(data['direccion'])
                if 'estado' in data:
                    pedido_encontrado.setestado(data['estado'])
                if 'productos' in data:
                    pedido_encontrado.setproductos(data['productos'])
                
                return jsonify({
                    'mensaje': 'Pedido actualizado exitosamente via controlador MVC',
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
                return self._error_response(f'Error al actualizar pedido: {str(e)}')
        
        # =================== DELETE - ELIMINAR ===================
        @self.app.route('/api/productos/<string:producto_codigo>', methods=['DELETE'])
        def eliminar_producto(producto_codigo):
            """Eliminar un producto"""
            try:
                # Buscar y eliminar producto del inventario
                producto_eliminado = None
                if self.inventario_instance and hasattr(self.inventario_instance, 'itemsPrimero'):
                    for i, producto in enumerate(self.inventario_instance.itemsPrimero):
                        if str(producto.getcodigo()) == str(producto_codigo):
                            producto_eliminado = self.inventario_instance.itemsPrimero.pop(i)
                            # También eliminar del diccionario si existe
                            if hasattr(self.inventario_instance, 'items') and producto_eliminado.getnombre() in self.inventario_instance.items:
                                del self.inventario_instance.items[producto_eliminado.getnombre()]
                            break
                
                if not producto_eliminado:
                    return self._error_response('Producto no encontrado', 404)
                
                return jsonify({
                    'mensaje': 'Producto eliminado exitosamente via modelo MVC',
                    'producto_eliminado': {
                        'codigo': producto_eliminado.getcodigo(),
                        'nombre': producto_eliminado.getnombre()
                    },
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return self._error_response(f'Error al eliminar producto: {str(e)}')
        
        @self.app.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
        def eliminar_pedido(pedido_id):
            """Eliminar un pedido"""
            try:
                # Buscar y eliminar pedido
                pedido_eliminado = None
                
                # Buscar en proxy primero
                if self.proxy_instance and hasattr(self.proxy_instance, 'listaPedidos'):
                    if pedido_id in self.proxy_instance.listaPedidos:
                        pedido_eliminado = self.proxy_instance.listaPedidos.pop(pedido_id)
                    else:
                        for key, pedido in list(self.proxy_instance.listaPedidos.items()):
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_eliminado = self.proxy_instance.listaPedidos.pop(key)
                                break
                
                # Si no se encontró en proxy, buscar en bd
                if not pedido_eliminado and self.bd_instance and hasattr(self.bd_instance, 'listaPedidos'):
                    if pedido_id in self.bd_instance.listaPedidos:
                        pedido_eliminado = self.bd_instance.listaPedidos.pop(pedido_id)
                    else:
                        for key, pedido in list(self.bd_instance.listaPedidos.items()):
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_eliminado = self.bd_instance.listaPedidos.pop(key)
                                break
                
                if not pedido_eliminado:
                    return self._error_response('Pedido no encontrado', 404)
                
                return jsonify({
                    'mensaje': 'Pedido eliminado exitosamente via controlador MVC',
                    'pedido_eliminado': {
                        'idPedido': pedido_eliminado.getidPedido(),
                        'direccion': pedido_eliminado.getdireccion(),
                        'estado': pedido_eliminado.getestado()
                    },
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return self._error_response(f'Error al eliminar pedido: {str(e)}')
        
        # =================== PATCH - ACTUALIZACIÓN PARCIAL ===================
        @self.app.route('/api/pedidos/<int:pedido_id>/estado', methods=['PATCH'])
        def cambiar_estado_pedido(pedido_id):
            """Cambiar solo el estado de un pedido"""
            try:
                data = request.get_json()
                
                if not data or 'estado' not in data:
                    return self._error_response('Se requiere el campo estado', 400)
                
                # Buscar pedido
                pedido_encontrado = None
                
                # Buscar en proxy primero
                if self.proxy_instance and hasattr(self.proxy_instance, 'listaPedidos'):
                    if pedido_id in self.proxy_instance.listaPedidos:
                        pedido_encontrado = self.proxy_instance.listaPedidos[pedido_id]
                    else:
                        for pedido_id_key, pedido in self.proxy_instance.listaPedidos.items():
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_encontrado = pedido
                                break
                
                # Si no se encontró en proxy, buscar en bd
                if not pedido_encontrado and self.bd_instance and hasattr(self.bd_instance, 'listaPedidos'):
                    if pedido_id in self.bd_instance.listaPedidos:
                        pedido_encontrado = self.bd_instance.listaPedidos[pedido_id]
                    else:
                        for pedido_id_key, pedido in self.bd_instance.listaPedidos.items():
                            pedido_id_actual = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
                            if pedido_id_actual == pedido_id:
                                pedido_encontrado = pedido
                                break
                
                if not pedido_encontrado:
                    return self._error_response('Pedido no encontrado', 404)
                
                estado_anterior = pedido_encontrado.getestado()
                pedido_encontrado.setestado(data['estado'])
                
                return jsonify({
                    'mensaje': 'Estado del pedido actualizado via controlador MVC',
                    'pedido_id': pedido_id,
                    'estado_anterior': estado_anterior,
                    'estado_nuevo': data['estado'],
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return self._error_response(f'Error al cambiar estado: {str(e)}')

    def _obtener_endpoints_disponibles(self):
        """Obtener lista de endpoints disponibles"""
        return {
            'informacion': '/api - Información de la API MVC',
            'metodos': '/api/metodos - Lista de todos los métodos HTTP',
            'usuarios': {
                'GET': '/api/usuarios - Listar usuarios',
                'POST': '/api/usuarios - Crear usuario'
            },
            'productos': {
                'GET': '/api/productos - Listar productos',
                'POST': '/api/productos - Crear producto',
                'PUT': '/api/productos/<codigo> - Actualizar producto',
                'DELETE': '/api/productos/<codigo> - Eliminar producto'
            },
            'pedidos': {
                'GET': '/api/pedidos - Listar pedidos',
                'POST': '/api/pedidos - Crear pedido',
                'PUT': '/api/pedidos/<id> - Actualizar pedido',
                'DELETE': '/api/pedidos/<id> - Eliminar pedido',
                'PATCH': '/api/pedidos/<id>/estado - Cambiar estado'
            },
            'total_endpoints': 13,
            'metodos_http': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        }
    
    def _error_response(self, mensaje, codigo=500):
        """Generar respuesta de error estándar"""
        return jsonify({
            'error': mensaje,
            'arquitectura': 'MVC Simplificada',
            'timestamp': datetime.now().isoformat()
        }), codigo
    
    def ejecutar(self, host='0.0.0.0', port=5000, debug=False):
        """Ejecutar el servidor REST"""
        print("🚀 Iniciando servidor REST UVShop (Arquitectura MVC Simplificada)...")
        print("📡 API disponible en: http://localhost:5000/api")
        print("🏗️ Arquitectura: Model-View-Controller (estable)")
        self.app.run(host=host, port=port, debug=debug)


# Función para crear la vista REST
def crear_vista_rest_simple():
    """Factory function para crear la vista REST simplificada"""
    return VistaRESTSimple()


if __name__ == '__main__':
    vista_rest = crear_vista_rest_simple()
    vista_rest.ejecutar()
