"""
GESTOR CENTRAL DE PEDIDOS - Singleton
=====================================
Caso de Uso 1: Gestión centralizada de pedidos con patrón Singleton
Mantiene la estructura existente pero centraliza las operaciones críticas.
"""

from controlador.gestionPedidosUsuarios import gestionPedidosUsuarios
from controlador.gestionPedidosDueno import gestionPedidosDueno


class GestorCentralPedidos:
    """
    Singleton que centraliza TODAS las operaciones de pedidos.
    Garantiza integridad del sistema y acceso global único.
    """
    _instancia = None
    _inicializado = False

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def __init__(self):
        # Evitar reinicialización
        if not GestorCentralPedidos._inicializado:
            self._gestores_existentes = {}
            self._log_operaciones = []
            GestorCentralPedidos._inicializado = True
            print("✅ Gestor Central de Pedidos inicializado (Singleton)")
    
    def registrar_gestor_usuarios(self, gestor_usuarios):
        """Registra el gestor de usuarios existente"""
        self._gestores_existentes['usuarios'] = gestor_usuarios
        self._log_operacion("REGISTRO_GESTOR", "usuarios")
    
    def registrar_gestor_dueno(self, gestor_dueno):
        """Registra el gestor del dueño existente"""
        self._gestores_existentes['dueno'] = gestor_dueno
        self._log_operacion("REGISTRO_GESTOR", "dueno")
    
    # ===== OPERACIONES CENTRALIZADAS =====
    
    def crear_pedido_centralizado(self, id_usuario, direccion, carro, precio_envio, tipo_envio):
        """Operación crítica centralizada: Crear Pedido"""
        self._log_operacion("CREAR_PEDIDO", f"usuario_{id_usuario}")
        
        # Usar gestor existente sin modificarlo
        gestor = self._gestores_existentes.get('usuarios')
        if gestor:
            resultado = gestor.nuevoPedido(id_usuario, direccion, carro, precio_envio, tipo_envio)
            self._log_resultado("CREAR_PEDIDO", resultado)
            return resultado
        else:
            self._log_error("CREAR_PEDIDO", "Gestor usuarios no registrado")
            return 0
    
    def modificar_pedido_centralizado(self, id_pedido, operacion, cambio, es_dueno=False):
        """Operación crítica centralizada: Modificar Pedido"""
        tipo_gestor = "dueno" if es_dueno else "usuarios"
        self._log_operacion("MODIFICAR_PEDIDO", f"{tipo_gestor}_{id_pedido}")
        
        gestor = self._gestores_existentes.get(tipo_gestor)
        if gestor:
            resultado = gestor.modificarPedido(id_pedido, operacion, cambio)
            self._log_resultado("MODIFICAR_PEDIDO", resultado)
            return resultado
        else:
            self._log_error("MODIFICAR_PEDIDO", f"Gestor {tipo_gestor} no registrado")
            return 0
    
    def cancelar_pedido_centralizado(self, id_pedido, es_dueno=False):
        """Operación crítica centralizada: Cancelar Pedido"""
        tipo_gestor = "dueno" if es_dueno else "usuarios"
        self._log_operacion("CANCELAR_PEDIDO", f"{tipo_gestor}_{id_pedido}")
        
        gestor = self._gestores_existentes.get(tipo_gestor)
        if gestor:
            resultado = gestor.cancelarPedido(id_pedido)
            self._log_resultado("CANCELAR_PEDIDO", resultado)
            return resultado
        else:
            self._log_error("CANCELAR_PEDIDO", f"Gestor {tipo_gestor} no registrado")
            return 0
    
    def pagar_pedido_centralizado(self, id_pedido, id_usuario, tipo_pago):
        """Operación crítica centralizada: Pagar Pedido"""
        self._log_operacion("PAGAR_PEDIDO", f"usuario_{id_usuario}_pedido_{id_pedido}")
        
        gestor = self._gestores_existentes.get('usuarios')
        if gestor:
            resultado = gestor.pagarPedido(id_pedido, id_usuario, tipo_pago)
            self._log_resultado("PAGAR_PEDIDO", resultado)
            return resultado
        else:
            self._log_error("PAGAR_PEDIDO", "Gestor usuarios no registrado")
            return 0
    
    def consultar_pedido_centralizado(self, id_pedido, es_dueno=False):
        """Operación crítica centralizada: Consultar Pedido"""
        tipo_gestor = "dueno" if es_dueno else "usuarios"
        gestor = self._gestores_existentes.get(tipo_gestor)
        
        if gestor:
            resultado = gestor.recuperarPedido(id_pedido)
            self._log_operacion("CONSULTAR_PEDIDO", f"{tipo_gestor}_{id_pedido}")
            return resultado
        else:
            self._log_error("CONSULTAR_PEDIDO", f"Gestor {tipo_gestor} no registrado")
            return 0
    
    # ===== SISTEMA DE LOGGING Y CONTROL =====
    
    def _log_operacion(self, operacion, detalle):
        """Log de operaciones centralizadas"""
        from datetime import datetime
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] {operacion}: {detalle}"
        self._log_operaciones.append(log_entry)
        print(f"🔍 LOG CENTRAL: {log_entry}")
    
    def _log_resultado(self, operacion, resultado):
        """Log de resultados"""
        estado = "ÉXITO" if resultado != 0 else "FALLO"
        self._log_operacion(f"{operacion}_RESULTADO", f"{estado} ({resultado})")
    
    def _log_error(self, operacion, error):
        """Log de errores"""
        self._log_operacion(f"{operacion}_ERROR", error)
    
    def obtener_estadisticas_centralizadas(self):
        """Estadísticas del sistema centralizado"""
        total_ops = len(self._log_operaciones)
        errores = len([log for log in self._log_operaciones if 'ERROR' in log])
        exitos = len([log for log in self._log_operaciones if 'ÉXITO' in log])
        
        return {
            'total_operaciones': total_ops,
            'operaciones_exitosas': exitos,
            'operaciones_fallidas': errores,
            'gestores_registrados': list(self._gestores_existentes.keys()),
            'ultimas_operaciones': self._log_operaciones[-5:] if self._log_operaciones else []
        }
    
    def mostrar_resumen_sistema(self):
        """Muestra resumen del sistema centralizado"""
        stats = self.obtener_estadisticas_centralizadas()
        print("\n" + "="*60)
        print("📊 RESUMEN SISTEMA CENTRALIZADO DE PEDIDOS")
        print("="*60)
        print(f"📈 Total operaciones: {stats['total_operaciones']}")
        print(f"✅ Operaciones exitosas: {stats['operaciones_exitosas']}")
        print(f"❌ Operaciones fallidas: {stats['operaciones_fallidas']}")
        print(f"🎯 Gestores registrados: {', '.join(stats['gestores_registrados'])}")
        
        if stats['ultimas_operaciones']:
            print("\n📋 Últimas operaciones:")
            for op in stats['ultimas_operaciones']:
                print(f"   {op}")
        
        print("="*60)


# Función para obtener la instancia global
def obtener_gestor_central():
    """Función utilitaria para obtener la instancia única del gestor central"""
    return GestorCentralPedidos()
