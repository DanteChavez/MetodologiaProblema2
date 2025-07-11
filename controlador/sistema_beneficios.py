"""
SISTEMA DE BENEFICIOS DINÁMICOS PARA CLIENTES - Patrón Decorator
================================================================
Caso de Uso 3: Beneficios que pueden agregarse/quitarse sin alterar las clases cliente.
Mantiene la clase usuario existente intacta.
"""

from abc import ABC, abstractmethod
from modelo.usuario import usuario


class ComponenteCliente(ABC):
    """Interfaz base para el patrón Decorator"""
    
    @abstractmethod
    def obtener_descuento(self):
        pass
    
    @abstractmethod
    def tiene_envio_gratis(self):
        pass
    
    @abstractmethod
    def obtener_cashback(self):
        pass
    
    @abstractmethod
    def obtener_descripcion(self):
        pass
    
    @abstractmethod
    def obtener_usuario_base(self):
        pass


class ClienteBase(ComponenteCliente):
    """Wrapper para la clase usuario existente (sin modificarla)"""
    
    def __init__(self, usuario_existente):
        self.usuario = usuario_existente
    
    def obtener_descuento(self):
        """Descuento base según tipo de cliente original"""
        tipo = self.usuario.getTipoCliente().lower()
        descuentos_base = {
            'nuevo': 5,
            'frecuente': 10, 
            'vip': 15
        }
        return descuentos_base.get(tipo, 0)
    
    def tiene_envio_gratis(self):
        """Solo VIP tiene envío gratis por defecto"""
        return self.usuario.getTipoCliente().lower() == 'vip'
    
    def obtener_cashback(self):
        """Sin cashback por defecto"""
        return 0
    
    def obtener_descripcion(self):
        """Descripción del cliente base"""
        return f"Cliente {self.usuario.getTipoCliente()}"
    
    def obtener_usuario_base(self):
        """Retorna el usuario original"""
        return self.usuario


class DecoradorBeneficio(ComponenteCliente):
    """Decorator base para beneficios adicionales"""
    
    def __init__(self, componente_cliente):
        self._componente = componente_cliente
    
    def obtener_descuento(self):
        return self._componente.obtener_descuento()
    
    def tiene_envio_gratis(self):
        return self._componente.tiene_envio_gratis()
    
    def obtener_cashback(self):
        return self._componente.obtener_cashback()
    
    def obtener_descripcion(self):
        return self._componente.obtener_descripcion()
    
    def obtener_usuario_base(self):
        return self._componente.obtener_usuario_base()


class BeneficioDescuentoExtra(DecoradorBeneficio):
    """Decorator: Descuento adicional temporal"""
    
    def __init__(self, componente_cliente, descuento_extra):
        super().__init__(componente_cliente)
        self.descuento_extra = descuento_extra
    
    def obtener_descuento(self):
        return self._componente.obtener_descuento() + self.descuento_extra
    
    def obtener_descripcion(self):
        return f"{self._componente.obtener_descripcion()} + Descuento Extra {self.descuento_extra}%"


class BeneficioEnvioGratis(DecoradorBeneficio):
    """Decorator: Envío gratis temporal"""
    
    def tiene_envio_gratis(self):
        return True  # Fuerza envío gratis
    
    def obtener_descripcion(self):
        return f"{self._componente.obtener_descripcion()} + Envío Gratis"


class BeneficioCashback(DecoradorBeneficio):
    """Decorator: Cashback temporal"""
    
    def __init__(self, componente_cliente, porcentaje_cashback):
        super().__init__(componente_cliente)
        self.cashback = porcentaje_cashback
    
    def obtener_cashback(self):
        return self._componente.obtener_cashback() + self.cashback
    
    def obtener_descripcion(self):
        return f"{self._componente.obtener_descripcion()} + Cashback {self.cashback}%"


class BeneficioVIPMejorado(DecoradorBeneficio):
    """Decorator: Beneficio VIP temporal mejorado (ejemplo del caso de uso)"""
    
    def obtener_descuento(self):
        return max(self._componente.obtener_descuento(), 15)  # Mínimo 15%
    
    def tiene_envio_gratis(self):
        return True
    
    def obtener_cashback(self):
        return self._componente.obtener_cashback() + 3  # +3% cashback
    
    def obtener_descripcion(self):
        return f"{self._componente.obtener_descripcion()} + VIP Mejorado Temporal"


class GestorBeneficios:
    """Gestor para aplicar beneficios dinámicos a clientes"""
    
    def __init__(self):
        self.beneficios_activos = {}  # {usuario_id: [lista_beneficios]}
    
    def aplicar_beneficio_temporal(self, usuario_original, tipo_beneficio, **kwargs):
        """
        Aplica beneficios temporales a un cliente sin modificar la clase usuario.
        
        Args:
            usuario_original: Instancia de la clase usuario existente
            tipo_beneficio: 'descuento_extra', 'envio_gratis', 'cashback', 'vip_mejorado'
            **kwargs: Parámetros adicionales (ej: descuento_extra=5)
        """
        # Crear wrapper del usuario existente
        cliente = ClienteBase(usuario_original)
        
        # Aplicar decorators según el tipo
        if tipo_beneficio == 'descuento_extra':
            descuento = kwargs.get('descuento_extra', 5)
            cliente = BeneficioDescuentoExtra(cliente, descuento)
        
        elif tipo_beneficio == 'envio_gratis':
            cliente = BeneficioEnvioGratis(cliente)
        
        elif tipo_beneficio == 'cashback':
            cashback = kwargs.get('cashback', 2)
            cliente = BeneficioCashback(cliente, cashback)
        
        elif tipo_beneficio == 'vip_mejorado':
            cliente = BeneficioVIPMejorado(cliente)
        
        # Registrar beneficio activo
        user_id = usuario_original.getidUsuario()
        if user_id not in self.beneficios_activos:
            self.beneficios_activos[user_id] = []
        self.beneficios_activos[user_id].append(tipo_beneficio)
        
        print(f"✅ Beneficio '{tipo_beneficio}' aplicado a {usuario_original.getnombre()}")
        return cliente
    
    def aplicar_promocion_especial(self, usuario_original, nombre_promocion):
        """
        Aplica promociones predefinidas combinando múltiples beneficios.
        Ejemplo del caso de uso: VIP mejorado con 15% + envío gratis + cashback
        """
        cliente = ClienteBase(usuario_original)
        
        if nombre_promocion == 'vip_premium_temporal':
            # Ejemplo del caso de uso: VIP: 15% + envío gratis + cashback
            cliente = BeneficioDescuentoExtra(cliente, 5)  # Asegurar mínimo 15%
            cliente = BeneficioEnvioGratis(cliente)
            cliente = BeneficioCashback(cliente, 3)
            
        elif nombre_promocion == 'black_friday':
            cliente = BeneficioDescuentoExtra(cliente, 10)
            cliente = BeneficioEnvioGratis(cliente)
            cliente = BeneficioCashback(cliente, 5)
        
        elif nombre_promocion == 'cliente_nuevo_plus':
            cliente = BeneficioDescuentoExtra(cliente, 3)
            cliente = BeneficioEnvioGratis(cliente)
        
        user_id = usuario_original.getidUsuario()
        if user_id not in self.beneficios_activos:
            self.beneficios_activos[user_id] = []
        self.beneficios_activos[user_id].append(f"promocion_{nombre_promocion}")
        
        print(f"🎉 Promoción '{nombre_promocion}' aplicada a {usuario_original.getnombre()}")
        print(f"📋 Beneficios: {cliente.obtener_descripcion()}")
        
        return cliente
    
    def remover_beneficios(self, usuario_id):
        """Remueve todos los beneficios temporales de un cliente"""
        if usuario_id in self.beneficios_activos:
            del self.beneficios_activos[usuario_id]
            print(f"🗑️ Beneficios removidos para usuario {usuario_id}")
    
    def listar_beneficios_activos(self, usuario_id):
        """Lista los beneficios activos de un cliente"""
        return self.beneficios_activos.get(usuario_id, [])
    
    def mostrar_estado_beneficios(self):
        """Muestra el estado de todos los beneficios activos"""
        print("\n" + "="*50)
        print("🎁 ESTADO DE BENEFICIOS DINÁMICOS")
        print("="*50)
        
        if not self.beneficios_activos:
            print("📋 No hay beneficios activos")
        else:
            for user_id, beneficios in self.beneficios_activos.items():
                print(f"👤 Usuario {user_id}: {', '.join(beneficios)}")
        
        print("="*50)


# Instancia global del gestor de beneficios
gestor_beneficios_global = GestorBeneficios()


def obtener_gestor_beneficios():
    """Función utilitaria para obtener la instancia del gestor de beneficios"""
    return gestor_beneficios_global


def aplicar_beneficios_a_usuario(usuario_original, beneficios_temporales):
    """
    Función utilitaria para aplicar múltiples beneficios a un usuario.
    
    Args:
        usuario_original: Instancia de usuario existente
        beneficios_temporales: Lista de beneficios a aplicar
    
    Returns:
        ComponenteCliente con todos los beneficios aplicados
    """
    gestor = obtener_gestor_beneficios()
    cliente = ClienteBase(usuario_original)
    
    for beneficio in beneficios_temporales:
        if beneficio['tipo'] == 'descuento_extra':
            cliente = BeneficioDescuentoExtra(cliente, beneficio.get('valor', 5))
        elif beneficio['tipo'] == 'envio_gratis':
            cliente = BeneficioEnvioGratis(cliente)
        elif beneficio['tipo'] == 'cashback':
            cliente = BeneficioCashback(cliente, beneficio.get('valor', 2))
        elif beneficio['tipo'] == 'vip_mejorado':
            cliente = BeneficioVIPMejorado(cliente)
    
    return cliente
