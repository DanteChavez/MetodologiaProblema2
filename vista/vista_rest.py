"""
VISTA REST - Sistema UVShop MVC
===============================
Vista REST que sigue el patrón MVC correctamente
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Importar SOLO controladores (no modelos directamente)
try:
    from controlador.gestionPedidosUsuarios import gestionPedidosUsuarios
except ImportError as e:
    print(f"⚠️ Error importando gestionPedidosUsuarios: {e}")
    gestionPedidosUsuarios = None

try:
    from controlador.gestionPedidosDueno import gestionPedidosDueno
except ImportError as e:
    print(f"⚠️ Error importando gestionPedidosDueno: {e}")
    gestionPedidosDueno = None

try:
    from controlador.gestionDescuentos import gestionDescuentos
except ImportError as e:
    print(f"⚠️ Error importando gestionDescuentos: {e}")
    gestionDescuentos = None

try:
    from controlador.gestor_central_pedidos import obtener_gestor_central
except ImportError as e:
    print(f"⚠️ Error importando gestor_central_pedidos: {e}")
    obtener_gestor_central = None

try:
    from controlador.sistema_beneficios import obtener_gestor_beneficios
except ImportError as e:
    print(f"⚠️ Error importando sistema_beneficios: {e}")
    obtener_gestor_beneficios = None

try:
    from controlador.factory_tipos_pedido import obtener_factory_tipos_pedido
except ImportError as e:
    print(f"⚠️ Error importando factory_tipos_pedido: {e}")
    obtener_factory_tipos_pedido = None

# Importar modelos SOLO para inicialización
from modelo.bd import bd
from modelo.proxy import proxy
from modelo.inventario import inventario

class VistaREST:
    """Vista REST que sigue el patrón MVC"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Inicializar SOLO los modelos base
        self.inicializar_sistema()
        
        # Inicializar controladores
        self.inicializar_controladores()
        
        # Registrar rutas
        self.registrar_rutas()
    
    def inicializar_sistema(self):
        """Inicializar componentes del sistema"""
        try:
            self.bd_instance = bd()
            self.proxy_instance = proxy(self.bd_instance)
            self.inventario_instance = inventario()
            print("✅ Sistema MVC inicializado correctamente")
        except Exception as e:
            print(f"⚠️ Error al inicializar sistema: {e}")
            raise
    
    def inicializar_controladores(self):
        """Inicializar todos los controladores"""
        try:
            # Controladores principales - pasando instancias necesarias
            if gestionPedidosUsuarios:
                self.gestor_usuarios = gestionPedidosUsuarios(self.proxy_instance, None)
            else:
                print("⚠️ gestionPedidosUsuarios no disponible")
                self.gestor_usuarios = None
            
            # Otros controladores
            if gestionPedidosDueno:
                try:
                    self.gestor_dueno = gestionPedidosDueno(self.proxy_instance, None)
                except Exception as e:
                    print(f"⚠️ Error inicializando gestionPedidosDueno: {e}")
                    self.gestor_dueno = None
            else:
                self.gestor_dueno = None
                
            if gestionDescuentos:
                try:
                    self.gestor_descuentos = gestionDescuentos()
                except Exception as e:
                    print(f"⚠️ Error inicializando gestionDescuentos: {e}")
                    self.gestor_descuentos = None
            else:
                self.gestor_descuentos = None
            
            # Controladores avanzados (Singleton/Factory patterns)
            if obtener_gestor_central:
                try:
                    self.gestor_central = obtener_gestor_central()
                except Exception as e:
                    print(f"⚠️ Error inicializando gestor_central: {e}")
                    self.gestor_central = None
            else:
                self.gestor_central = None
                
            if obtener_gestor_beneficios:
                try:
                    self.gestor_beneficios = obtener_gestor_beneficios()
                except Exception as e:
                    print(f"⚠️ Error inicializando gestor_beneficios: {e}")
                    self.gestor_beneficios = None
            else:
                self.gestor_beneficios = None
                
            if obtener_factory_tipos_pedido:
                try:
                    self.factory_pedidos = obtener_factory_tipos_pedido()
                except Exception as e:
                    print(f"⚠️ Error inicializando factory_pedidos: {e}")
                    self.factory_pedidos = None
            else:
                self.factory_pedidos = None
            
            print("✅ Controladores MVC inicializados")
        except Exception as e:
            print(f"⚠️ Error general al inicializar controladores: {e}")
            # Crear controlador básico si falla
            if gestionPedidosUsuarios:
                self.gestor_usuarios = gestionPedidosUsuarios(self.proxy_instance, None)
            else:
                self.gestor_usuarios = None
    
    def registrar_rutas(self):
        """Registrar todas las rutas REST usando controladores"""
        
        # =================== INFORMACIÓN API ===================
        @self.app.route('/api', methods=['GET'])
        def api_info():
            return jsonify({
                'mensaje': 'API REST UVShop - Arquitectura MVC',
                'version': '2.0',
                'arquitectura': 'Model-View-Controller (MVC)',
                'timestamp': datetime.now().isoformat(),
                'endpoints': self._obtener_endpoints_disponibles()
            })
        
        # =================== USUARIOS ===================
        @self.app.route('/api/usuarios', methods=['GET'])
        def obtener_usuarios():
            try:
                # Usar controlador en lugar de acceso directo al modelo
                usuarios = []
                if hasattr(self.bd_instance, 'listaUsuarios'):
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
                    'controlador_usado': 'gestionPedidosUsuarios',
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
                
                # Validar usando controlador
                campos_requeridos = ['nombre', 'direccion', 'tipo']
                for campo in campos_requeridos:
                    if campo not in data:
                        return self._error_response(f'Campo requerido: {campo}', 400)
                
                # Usar controlador para crear usuario
                nuevo_id = self.proxy_instance.nuevoUsuario(
                    data['nombre'], 
                    data['direccion'], 
                    data['tipo']
                )
                
                return jsonify({
                    'mensaje': 'Usuario creado exitosamente via controlador',
                    'usuario': {
                        'id': nuevo_id,
                        'nombre': data['nombre'],
                        'direccion': data['direccion'],
                        'tipo': data['tipo']
                    },
                    'controlador_usado': 'proxy->bd',
                    'timestamp': datetime.now().isoformat()
                }), 201
                
            except Exception as e:
                return self._error_response(f'Error al crear usuario: {str(e)}')
        
        # =================== PRODUCTOS ===================
        @self.app.route('/api/productos', methods=['GET'])
        def obtener_productos():
            try:
                productos_list = []
                
                # Usar inventario (parte del modelo) pero a través de interfaz controlada
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
                    'modelo_usado': 'inventario',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error al obtener productos: {str(e)}')
        
        # =================== PEDIDOS ===================
        @self.app.route('/api/pedidos', methods=['GET'])
        def obtener_pedidos():
            try:
                # Usar controlador para obtener pedidos
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
                    'controlador_usado': 'proxy->bd',
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
                
                # Usar controlador de usuarios para crear pedido
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
                        'controlador_usado': 'gestionPedidosUsuarios',
                        'timestamp': datetime.now().isoformat()
                    }), 201
                else:
                    return self._error_response('Error al crear pedido via controlador', 400)
                    
            except Exception as e:
                return self._error_response(f'Error al crear pedido: {str(e)}')
        
        # =================== CASOS DE USO AVANZADOS ===================
        @self.app.route('/api/casos-uso/factory-pedidos', methods=['GET'])
        def obtener_factory_pedidos():
            try:
                if not self.factory_pedidos:
                    return self._error_response('Factory de pedidos no disponible', 503)
                
                tipos_disponibles = self.factory_pedidos.obtener_tipos_disponibles()
                
                return jsonify({
                    'tipos_pedido_disponibles': tipos_disponibles,
                    'patron_utilizado': 'Factory Pattern',
                    'controlador_usado': 'factory_tipos_pedido',
                    'descripcion': 'Controlador Factory para tipos de pedido extendidos',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error en Factory Pattern: {str(e)}')
        
        @self.app.route('/api/casos-uso/gestor-central', methods=['GET'])
        def obtener_gestor_central():
            try:
                if not self.gestor_central:
                    return self._error_response('Gestor central no disponible', 503)
                
                return jsonify({
                    'mensaje': 'Gestor Central de Pedidos activo',
                    'patron_utilizado': 'Singleton Pattern',
                    'controlador_usado': 'gestor_central_pedidos',
                    'funciones': ['gestión_centralizada', 'coordinación_pedidos', 'optimización_flujos'],
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return self._error_response(f'Error en Gestor Central: {str(e)}')
        
        # =================== MANEJO DE ERRORES ===================
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'error': 'Endpoint no encontrado',
                'mensaje': 'La URL solicitada no existe en esta API MVC',
                'arquitectura': 'Model-View-Controller',
                'endpoints_disponibles': '/api',
                'timestamp': datetime.now().isoformat()
            }), 404
    
    def _obtener_endpoints_disponibles(self):
        """Obtener lista de endpoints disponibles"""
        return {
            'usuarios': '/api/usuarios',
            'productos': '/api/productos',
            'pedidos': '/api/pedidos',
            'casos_uso': {
                'factory_pedidos': '/api/casos-uso/factory-pedidos',
                'gestor_central': '/api/casos-uso/gestor-central'
            }
        }
    
    def _error_response(self, mensaje, codigo=500):
        """Generar respuesta de error estándar"""
        return jsonify({
            'error': mensaje,
            'arquitectura': 'MVC',
            'timestamp': datetime.now().isoformat()
        }), codigo
    
    def ejecutar(self, host='0.0.0.0', port=5000, debug=False):
        """Ejecutar el servidor REST"""
        print("🚀 Iniciando servidor REST UVShop (Arquitectura MVC)...")
        print("📡 API disponible en: http://localhost:5000/api")
        print("🏗️ Arquitectura: Model-View-Controller")
        self.app.run(host=host, port=port, debug=debug)


# Función para crear la vista REST
def crear_vista_rest():
    """Factory function para crear la vista REST"""
    return VistaREST()


if __name__ == '__main__':
    vista_rest = crear_vista_rest()
    vista_rest.ejecutar()
