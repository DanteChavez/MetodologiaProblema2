"""
FACTORY PARA TIPOS DE PEDIDO - Extensión del Sistema Existente
============================================================
Caso de Uso 2: Nuevos tipos de pedido con reglas específicas sin modificar código existente.
Extiende las clases de pedido existentes usando Factory Pattern.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from modelo.pedido import pedido, internacional, programado, express, estandar


class TipoPedidoExtendido(ABC):
    """
    Interfaz para tipos de pedido extendidos con reglas de negocio específicas.
    """
    
    @abstractmethod
    def calcular_fecha_estimada_entrega(self):
        """Calcula fecha estimada de entrega según reglas específicas"""
        pass
    
    @abstractmethod
    def aplicar_condiciones_especiales(self):
        """Aplica condiciones especiales del tipo de pedido"""
        pass
    
    @abstractmethod
    def obtener_descripcion_tipo(self):
        """Retorna descripción del tipo de pedido"""
        pass
    
    @abstractmethod
    def calcular_costo_adicional(self, precio_base):
        """Calcula costos adicionales específicos del tipo"""
        pass


class PedidoInternacionalExtendido(TipoPedidoExtendido):
    """Extiende pedido internacional con nuevas reglas de negocio"""
    
    def __init__(self, pedido_base):
        self.pedido = pedido_base
        self.tiempo_aduanas = 3  # días adicionales
        self.seguro_internacional = True
    
    def calcular_fecha_estimada_entrega(self):
        """Internacional: 7-15 días + tiempo aduanas"""
        fecha_base = datetime.now()
        dias_minimos = 7 + self.tiempo_aduanas
        dias_maximos = 15 + self.tiempo_aduanas
        
        fecha_minima = fecha_base + timedelta(days=dias_minimos)
        fecha_maxima = fecha_base + timedelta(days=dias_maximos)
        
        return {
            'fecha_minima': fecha_minima.strftime('%Y-%m-%d'),
            'fecha_maxima': fecha_maxima.strftime('%Y-%m-%d'),
            'dias_estimados': f"{dias_minimos}-{dias_maximos} días"
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para envío internacional"""
        condiciones = [
            "Requiere documentación aduanera",
            "Seguro internacional incluido",
            "Posibles demoras por inspección aduanera",
            "Impuestos locales aplicables según país destino"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Envío Internacional Premium"
    
    def calcular_costo_adicional(self, precio_base):
        """Costo adicional: seguro + trámites internacionales"""
        seguro = precio_base * 0.03  # 3% seguro
        tramites = 25.00  # Costo fijo trámites
        return {
            'seguro_internacional': seguro,
            'tramites_aduaneros': tramites,
            'total_adicional': seguro + tramites
        }


class PedidoExpressExtendido(TipoPedidoExtendido):
    """Extiende pedido express con nuevas reglas de negocio"""
    
    def __init__(self, pedido_base):
        self.pedido = pedido_base
        self.prioridad_maxima = True
        self.tracking_tiempo_real = True
    
    def calcular_fecha_estimada_entrega(self):
        """Express: 1-2 días laborables"""
        fecha_base = datetime.now()
        
        # Si es viernes, sábado o domingo, agregar días hasta lunes
        dias_a_agregar = 1
        fecha_entrega = fecha_base + timedelta(days=dias_a_agregar)
        
        # Evitar entrega en fin de semana
        while fecha_entrega.weekday() >= 5:  # 5=sábado, 6=domingo
            fecha_entrega += timedelta(days=1)
        
        return {
            'fecha_estimada': fecha_entrega.strftime('%Y-%m-%d'),
            'hora_estimada': '18:00',
            'dias_estimados': '1-2 días laborables'
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para envío express"""
        condiciones = [
            "Entrega en horario laboral (9:00-18:00)",
            "Tracking en tiempo real incluido",
            "Prioridad máxima en procesamiento",
            "Notificaciones SMS de seguimiento"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Envío Express con Tracking"
    
    def calcular_costo_adicional(self, precio_base):
        """Costo adicional: servicio premium"""
        servicio_premium = 15.00
        tracking_premium = 5.00
        return {
            'servicio_express': servicio_premium,
            'tracking_premium': tracking_premium,
            'total_adicional': servicio_premium + tracking_premium
        }


class PedidoProgramadoExtendido(TipoPedidoExtendido):
    """Extiende pedido programado con nuevas reglas de negocio"""
    
    def __init__(self, pedido_base, fecha_programada=None):
        self.pedido = pedido_base
        self.fecha_programada = fecha_programada
        self.flexibilidad_horario = True
    
    def calcular_fecha_estimada_entrega(self):
        """Programado: fecha específica seleccionada por cliente"""
        if self.fecha_programada:
            fecha_programada = datetime.strptime(self.fecha_programada, '%Y-%m-%d')
        else:
            # Default: 5 días desde hoy
            fecha_programada = datetime.now() + timedelta(days=5)
        
        return {
            'fecha_programada': fecha_programada.strftime('%Y-%m-%d'),
            'ventana_entrega': '09:00 - 17:00',
            'flexibilidad': 'Reprogramable hasta 24h antes'
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para envío programado"""
        condiciones = [
            "Entrega en fecha específica seleccionada",
            "Ventana de entrega de 8 horas",
            "Reprogramable con 24h de anticipación",
            "Confirmación por email 24h antes"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Envío Programado Flexible"
    
    def calcular_costo_adicional(self, precio_base):
        """Costo adicional: servicio de programación"""
        servicio_programacion = 8.00
        return {
            'servicio_programacion': servicio_programacion,
            'total_adicional': servicio_programacion
        }


class PedidoEstandarExtendido(TipoPedidoExtendido):
    """Extiende pedido estándar con nuevas reglas de negocio"""
    
    def __init__(self, pedido_base):
        self.pedido = pedido_base
        self.economia_maxima = True
    
    def calcular_fecha_estimada_entrega(self):
        """Estándar: 3-7 días laborables"""
        fecha_base = datetime.now()
        dias_minimos = 3
        dias_maximos = 7
        
        fecha_minima = fecha_base + timedelta(days=dias_minimos)
        fecha_maxima = fecha_base + timedelta(days=dias_maximos)
        
        return {
            'fecha_minima': fecha_minima.strftime('%Y-%m-%d'),
            'fecha_maxima': fecha_maxima.strftime('%Y-%m-%d'),
            'dias_estimados': f"{dias_minimos}-{dias_maximos} días laborables"
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para envío estándar"""
        condiciones = [
            "Opción más económica disponible",
            "Entrega en horario comercial",
            "Tracking básico incluido",
            "Consolidación con otros pedidos para optimizar costos"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Envío Estándar Económico"
    
    def calcular_costo_adicional(self, precio_base):
        """Sin costos adicionales para envío estándar"""
        return {
            'total_adicional': 0.00
        }


# NUEVOS TIPOS DE PEDIDO (sin modificar código existente)

class PedidoEcoFriendly(TipoPedidoExtendido):
    """NUEVO: Pedido con embalaje ecológico"""
    
    def __init__(self, pedido_base):
        self.pedido = pedido_base
        self.embalaje_biodegradable = True
        self.carbon_neutral = True
    
    def calcular_fecha_estimada_entrega(self):
        """Eco-friendly: 4-6 días (tiempo adicional para embalaje especial)"""
        fecha_base = datetime.now()
        dias_minimos = 4
        dias_maximos = 6
        
        fecha_minima = fecha_base + timedelta(days=dias_minimos)
        fecha_maxima = fecha_base + timedelta(days=dias_maximos)
        
        return {
            'fecha_minima': fecha_minima.strftime('%Y-%m-%d'),
            'fecha_maxima': fecha_maxima.strftime('%Y-%m-%d'),
            'dias_estimados': f"{dias_minimos}-{dias_maximos} días",
            'nota_especial': 'Tiempo adicional por embalaje ecológico'
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para envío eco-friendly"""
        condiciones = [
            "Embalaje 100% biodegradable",
            "Envío carbono neutral",
            "Materiales reciclados y reciclables",
            "Contribución a reforestación incluida"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Envío Eco-Friendly Sustentable"
    
    def calcular_costo_adicional(self, precio_base):
        """Costo adicional: embalaje ecológico"""
        embalaje_eco = 3.50
        compensacion_carbon = 2.00
        return {
            'embalaje_biodegradable': embalaje_eco,
            'compensacion_carbono': compensacion_carbon,
            'total_adicional': embalaje_eco + compensacion_carbon
        }


class PedidoSameDay(TipoPedidoExtendido):
    """NUEVO: Entrega el mismo día"""
    
    def __init__(self, pedido_base, hora_limite="14:00"):
        self.pedido = pedido_base
        self.hora_limite_pedido = hora_limite
        self.entrega_mismo_dia = True
    
    def calcular_fecha_estimada_entrega(self):
        """Same Day: Entrega el mismo día si se pide antes de hora límite"""
        ahora = datetime.now()
        hora_limite = datetime.strptime(self.hora_limite_pedido, "%H:%M").time()
        
        if ahora.time() <= hora_limite:
            fecha_entrega = ahora.date()
            ventana_entrega = "18:00 - 21:00"
        else:
            fecha_entrega = (ahora + timedelta(days=1)).date()
            ventana_entrega = "09:00 - 12:00"
        
        return {
            'fecha_entrega': fecha_entrega.strftime('%Y-%m-%d'),
            'ventana_entrega': ventana_entrega,
            'nota': f'Pedidos antes de {self.hora_limite_pedido} se entregan el mismo día'
        }
    
    def aplicar_condiciones_especiales(self):
        """Condiciones especiales para entrega mismo día"""
        condiciones = [
            f"Pedido debe realizarse antes de {self.hora_limite_pedido}",
            "Disponible solo en zona metropolitana",
            "Entrega con motociclista dedicado",
            "Tracking GPS en tiempo real"
        ]
        return condiciones
    
    def obtener_descripcion_tipo(self):
        return "Entrega Mismo Día"
    
    def calcular_costo_adicional(self, precio_base):
        """Costo adicional: servicio same day"""
        servicio_mismo_dia = 25.00
        motociclista_dedicado = 10.00
        return {
            'servicio_mismo_dia': servicio_mismo_dia,
            'motociclista_dedicado': motociclista_dedicado,
            'total_adicional': servicio_mismo_dia + motociclista_dedicado
        }


class FactoryTiposPedido:
    """
    Factory para crear tipos de pedido extendidos sin modificar código existente.
    Caso de Uso 2: Agregar nuevos tipos fácilmente.
    """
    
    _tipos_registrados = {
        'internacional': PedidoInternacionalExtendido,
        'express': PedidoExpressExtendido,
        'programado': PedidoProgramadoExtendido,
        'estandar': PedidoEstandarExtendido,
        # Nuevos tipos agregados sin modificar existentes
        'eco_friendly': PedidoEcoFriendly,
        'same_day': PedidoSameDay
    }
    
    @classmethod
    def crear_pedido_extendido(cls, tipo_envio, pedido_base, **kwargs):
        """
        Crea un tipo de pedido extendido sin modificar las clases existentes.
        
        Args:
            tipo_envio: Tipo de envío ('internacional', 'express', etc.)
            pedido_base: Instancia del pedido base existente
            **kwargs: Parámetros adicionales específicos del tipo
        
        Returns:
            TipoPedidoExtendido: Instancia del tipo de pedido extendido
        """
        tipo_clase = cls._tipos_registrados.get(tipo_envio.lower())
        
        if not tipo_clase:
            # Fallback a estándar si el tipo no existe
            print(f"⚠️ Tipo '{tipo_envio}' no reconocido, usando estándar")
            tipo_clase = PedidoEstandarExtendido
        
        # Crear instancia con parámetros específicos
        if tipo_envio.lower() == 'programado' and 'fecha_programada' in kwargs:
            return tipo_clase(pedido_base, kwargs['fecha_programada'])
        elif tipo_envio.lower() == 'same_day' and 'hora_limite' in kwargs:
            return tipo_clase(pedido_base, kwargs['hora_limite'])
        else:
            return tipo_clase(pedido_base)
    
    @classmethod
    def registrar_nuevo_tipo(cls, nombre_tipo, clase_tipo):
        """
        Registra un nuevo tipo de pedido sin modificar el código existente.
        
        Args:
            nombre_tipo: Nombre del nuevo tipo
            clase_tipo: Clase que implementa TipoPedidoExtendido
        """
        cls._tipos_registrados[nombre_tipo.lower()] = clase_tipo
        print(f"✅ Nuevo tipo de pedido registrado: {nombre_tipo}")
    
    @classmethod
    def obtener_tipos_disponibles(cls):
        """Retorna lista de tipos de pedido disponibles"""
        return list(cls._tipos_registrados.keys())
    
    @classmethod
    def mostrar_informacion_tipo(cls, tipo_envio):
        """Muestra información detallada de un tipo de pedido"""
        if tipo_envio.lower() not in cls._tipos_registrados:
            print(f"❌ Tipo '{tipo_envio}' no encontrado")
            return
        
        # Crear instancia temporal para mostrar info
        from modelo.pedido import pedido
        pedido_temp = pedido(1, "direccion_temp", 999, "pendiente", {}, None, None)
        tipo_extendido = cls.crear_pedido_extendido(tipo_envio, pedido_temp)
        
        print(f"\n📦 INFORMACIÓN: {tipo_extendido.obtener_descripcion_tipo()}")
        print("=" * 50)
        
        # Mostrar fecha estimada
        fecha_info = tipo_extendido.calcular_fecha_estimada_entrega()
        print("📅 Fecha de entrega estimada:")
        for key, value in fecha_info.items():
            print(f"   {key}: {value}")
        
        # Mostrar condiciones especiales
        print("\n📋 Condiciones especiales:")
        condiciones = tipo_extendido.aplicar_condiciones_especiales()
        for i, condicion in enumerate(condiciones, 1):
            print(f"   {i}. {condicion}")
        
        # Mostrar costos adicionales
        print("\n💰 Costos adicionales:")
        costos = tipo_extendido.calcular_costo_adicional(100)  # Ejemplo con $100
        for key, value in costos.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: ${value:.2f}")
        
        print("=" * 50)


def obtener_factory_tipos_pedido():
    """Función utilitaria para obtener la factory"""
    return FactoryTiposPedido
