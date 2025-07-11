"""
SISTEMA AVANZADO DE DESCUENTOS - Extensión del Sistema Existente
===============================================================
Caso de Uso 4: Cálculo automático de descuentos según tipo de cliente.
Extiende gestionDescuentos existente sin modificarlo.
"""

from controlador.sistema_beneficios import obtener_gestor_beneficios, ClienteBase


class CalculadorDescuentosAvanzado:
    """
    Calculadora avanzada que extiende el sistema de descuentos existente.
    Integra con el sistema de beneficios dinámicos.
    """
    
    def __init__(self, gestor_descuentos_existente):
        self.gestor_existente = gestor_descuentos_existente
        self.descuentos_automaticos = {
            'nuevo': {'porcentaje': 5, 'envio_gratis': False},
            'frecuente': {'porcentaje': 10, 'envio_gratis': False},
            'vip': {'porcentaje': 15, 'envio_gratis': True}
        }
    
    def calcular_descuentos_completos(self, usuario_original, beneficios_temporales=None):
        """
        Calcula descuentos completos combinando:
        1. Sistema existente (gestionDescuentos)
        2. Descuentos automáticos por tipo de cliente
        3. Beneficios temporales dinámicos
        
        Args:
            usuario_original: Instancia de usuario existente
            beneficios_temporales: Lista de beneficios adicionales
        
        Returns:
            dict: Información completa de descuentos
        """
        print(f"\n💰 CALCULANDO DESCUENTOS PARA: {usuario_original.getnombre()}")
        print("=" * 50)
        
        # 1. Descuentos del sistema existente
        descuentos_existentes = self.gestor_existente.calcularDescuentos(usuario_original.getidUsuario())
        print(f"📊 Sistema existente: {descuentos_existentes}")
        
        # 2. Crear cliente con beneficios dinámicos
        gestor_beneficios = obtener_gestor_beneficios()
        cliente_mejorado = ClienteBase(usuario_original)
        
        # Aplicar beneficios temporales si existen
        if beneficios_temporales:
            for beneficio in beneficios_temporales:
                cliente_mejorado = gestor_beneficios.aplicar_beneficio_temporal(
                    usuario_original, 
                    beneficio['tipo'], 
                    **beneficio.get('parametros', {})
                )
        
        # 3. Calcular descuentos automáticos por tipo
        tipo_cliente = usuario_original.getTipoCliente().lower()
        descuentos_auto = self.descuentos_automaticos.get(tipo_cliente, {'porcentaje': 0, 'envio_gratis': False})
        
        # 4. Combinar todos los descuentos
        descuento_total = max(
            cliente_mejorado.obtener_descuento(),  # Del sistema de beneficios
            descuentos_auto['porcentaje'],          # Automático por tipo
            (1 - descuentos_existentes[0]) * 100   # Del sistema existente
        )
        
        envio_gratis = (
            cliente_mejorado.tiene_envio_gratis() or 
            descuentos_auto['envio_gratis'] or 
            descuentos_existentes[1] == 1
        )
        
        cashback = cliente_mejorado.obtener_cashback()
        
        # 5. Preparar resultado
        resultado = {
            'descuento_porcentaje': descuento_total,
            'descuento_multiplicador': 1 - (descuento_total / 100),
            'envio_gratis': envio_gratis,
            'cashback_porcentaje': cashback,
            'descripcion_beneficios': cliente_mejorado.obtener_descripcion(),
            'descuentos_aplicados': [],
            'tipo_cliente': tipo_cliente.title()
        }
        
        # 6. Lista de descuentos aplicados
        if descuento_total > 0:
            resultado['descuentos_aplicados'].append(f"Descuento {tipo_cliente}: {descuento_total}%")
        
        if envio_gratis:
            resultado['descuentos_aplicados'].append("Envío gratis")
        
        if cashback > 0:
            resultado['descuentos_aplicados'].append(f"Cashback: {cashback}%")
        
        # Agregar descuentos del sistema existente
        if len(descuentos_existentes) > 2:
            for desc in descuentos_existentes[2]:
                resultado['descuentos_aplicados'].append(f"Descuento especial: {desc}")
        
        self._mostrar_resumen_descuentos(resultado)
        return resultado
    
    def _mostrar_resumen_descuentos(self, resultado):
        """Muestra resumen visual de descuentos"""
        print(f"\n🎯 RESUMEN DE DESCUENTOS")
        print(f"👤 Cliente: {resultado['tipo_cliente']}")
        print(f"💸 Descuento total: {resultado['descuento_porcentaje']}%")
        print(f"🚚 Envío gratis: {'✅ Sí' if resultado['envio_gratis'] else '❌ No'}")
        print(f"💰 Cashback: {resultado['cashback_porcentaje']}%")
        
        if resultado['descuentos_aplicados']:
            print(f"📋 Beneficios aplicados:")
            for desc in resultado['descuentos_aplicados']:
                print(f"   • {desc}")
        
        print("=" * 50)
    
    def calcular_precio_final(self, precio_base, precio_envio, usuario_original, beneficios_temporales=None):
        """
        Calcula el precio final aplicando todos los descuentos.
        
        Args:
            precio_base: Precio original del pedido
            precio_envio: Precio del envío
            usuario_original: Usuario que realiza la compra
            beneficios_temporales: Beneficios adicionales temporales
        
        Returns:
            dict: Desglose completo del precio final
        """
        descuentos = self.calcular_descuentos_completos(usuario_original, beneficios_temporales)
        
        # Aplicar descuento al precio base
        precio_con_descuento = precio_base * descuentos['descuento_multiplicador']
        descuento_aplicado = precio_base - precio_con_descuento
        
        # Aplicar envío gratis si corresponde
        precio_envio_final = 0 if descuentos['envio_gratis'] else precio_envio
        
        # Calcular cashback
        precio_total = precio_con_descuento + precio_envio_final
        cashback_cantidad = precio_total * (descuentos['cashback_porcentaje'] / 100)
        
        resultado_precio = {
            'precio_original': precio_base,
            'descuento_cantidad': descuento_aplicado,
            'precio_con_descuento': precio_con_descuento,
            'precio_envio_original': precio_envio,
            'precio_envio_final': precio_envio_final,
            'ahorro_envio': precio_envio - precio_envio_final,
            'precio_total': precio_total,
            'cashback_cantidad': cashback_cantidad,
            'precio_neto_final': precio_total - cashback_cantidad,
            'descuentos_info': descuentos
        }
        
        self._mostrar_desglose_precio(resultado_precio)
        return resultado_precio
    
    def _mostrar_desglose_precio(self, resultado):
        """Muestra desglose visual del precio"""
        print(f"\n💳 DESGLOSE DE PRECIO")
        print("=" * 40)
        print(f"💵 Precio original:     ${resultado['precio_original']:.2f}")
        print(f"💸 Descuento aplicado: -${resultado['descuento_cantidad']:.2f}")
        print(f"💰 Precio con descuento: ${resultado['precio_con_descuento']:.2f}")
        print(f"🚚 Envío original:      ${resultado['precio_envio_original']:.2f}")
        if resultado['ahorro_envio'] > 0:
            print(f"🎁 Ahorro envío gratis: -${resultado['ahorro_envio']:.2f}")
        print(f"🚚 Envío final:         ${resultado['precio_envio_final']:.2f}")
        print("─" * 40)
        print(f"💳 TOTAL A PAGAR:       ${resultado['precio_total']:.2f}")
        if resultado['cashback_cantidad'] > 0:
            print(f"💰 Cashback a recibir:   ${resultado['cashback_cantidad']:.2f}")
            print(f"🎯 Precio neto final:    ${resultado['precio_neto_final']:.2f}")
        print("=" * 40)


class PromotorDescuentosAutomatico:
    """
    Promociona descuentos automáticamente según reglas de negocio.
    """
    
    def __init__(self, calculadora_descuentos):
        self.calculadora = calculadora_descuentos
        self.reglas_promocion = {
            'upgrade_a_frecuente': {'compras_minimas': 3, 'beneficio': 'descuento_extra'},
            'upgrade_a_vip': {'compras_minimas': 10, 'beneficio': 'vip_mejorado'},
            'promocion_temporal': {'activa': True, 'beneficio': 'envio_gratis'}
        }
    
    def evaluar_promociones_automaticas(self, usuario_original):
        """
        Evalúa si el usuario califica para promociones automáticas.
        
        Args:
            usuario_original: Usuario a evaluar
        
        Returns:
            list: Lista de beneficios temporales que se pueden aplicar
        """
        beneficios_sugeridos = []
        tipo_cliente = usuario_original.getTipoCliente().lower()
        
        # Simulación de reglas de negocio
        print(f"\n🔍 EVALUANDO PROMOCIONES PARA: {usuario_original.getnombre()}")
        
        # Regla 1: Cliente nuevo con primera compra grande
        if tipo_cliente == 'nuevo':
            beneficios_sugeridos.append({
                'tipo': 'descuento_extra',
                'parametros': {'descuento_extra': 3},
                'razon': 'Bienvenida cliente nuevo'
            })
            beneficios_sugeridos.append({
                'tipo': 'envio_gratis',
                'parametros': {},
                'razon': 'Primera compra'
            })
        
        # Regla 2: Cliente frecuente - cashback especial
        elif tipo_cliente == 'frecuente':
            beneficios_sugeridos.append({
                'tipo': 'cashback',
                'parametros': {'cashback': 2},
                'razon': 'Lealtad cliente frecuente'
            })
        
        # Regla 3: Cliente VIP - beneficio mejorado temporal
        elif tipo_cliente == 'vip':
            beneficios_sugeridos.append({
                'tipo': 'vip_mejorado',
                'parametros': {},
                'razon': 'VIP Premium temporal'
            })
        
        # Mostrar promociones encontradas
        if beneficios_sugeridos:
            print("🎉 PROMOCIONES DISPONIBLES:")
            for i, beneficio in enumerate(beneficios_sugeridos, 1):
                print(f"   {i}. {beneficio['razon']} - {beneficio['tipo']}")
        else:
            print("📋 No hay promociones adicionales disponibles")
        
        return beneficios_sugeridos


def crear_calculadora_descuentos_avanzada(gestor_descuentos_existente):
    """
    Factory function para crear la calculadora avanzada de descuentos.
    
    Args:
        gestor_descuentos_existente: Instancia del gestionDescuentos actual
    
    Returns:
        CalculadorDescuentosAvanzado: Instancia configurada
    """
    return CalculadorDescuentosAvanzado(gestor_descuentos_existente)
