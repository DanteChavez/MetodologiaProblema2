from modelo.bd import *
from modelo.proxy import *
from controlador.gestionPedidosUsuarios import *
from controlador.gestionPedidosDueno import *
from controlador.gestionDescuentos import *
from modelo.inventario import *
from modelo.carrito import *

# NUEVOS IMPORTS - Sistemas avanzados sin modificar existentes
from controlador.gestor_central_pedidos import obtener_gestor_central
from controlador.sistema_beneficios import obtener_gestor_beneficios
from controlador.calculadora_descuentos_avanzada import crear_calculadora_descuentos_avanzada
from controlador.factory_tipos_pedido import obtener_factory_tipos_pedido

# FUNCIONES HELPER PARA INICIALIZACIÓN DE SINGLETONS
def inicializar_singleton_seguro(clase, *args):
    """Inicializa cualquier Singleton de forma segura"""
    # Resetear instancia existente
    if hasattr(clase, '_instancia') and clase._instancia is not None:
        clase._instancia = None
    
    # Crear nueva instancia manualmente
    instancia = object.__new__(clase)
    instancia.__init__(*args)
    clase._instancia = instancia
    return instancia

# INICIALIZACIÓN DEL SISTEMA
datos = bd()
inventario = inventario()
carro = carrito(inventario)
proxxy = proxy(datos)

# Inicializar todos los Singletons de forma segura
gestionDescuentosVariable = inicializar_singleton_seguro(gestionDescuentos, proxxy)
gestionUsuarios = inicializar_singleton_seguro(gestionPedidosUsuarios, proxxy, gestionDescuentosVariable)
gestionDueno = inicializar_singleton_seguro(gestionPedidosDueno, proxxy, gestionDescuentosVariable)

# INICIALIZAR SISTEMAS AVANZADOS
gestor_central = obtener_gestor_central()
gestor_beneficios = obtener_gestor_beneficios()
calculadora_descuentos = crear_calculadora_descuentos_avanzada(gestionDescuentosVariable)
factory_pedidos = obtener_factory_tipos_pedido()

# Registrar gestores en el sistema central
gestor_central.registrar_gestor_usuarios(gestionUsuarios)
gestor_central.registrar_gestor_dueno(gestionDueno)



def comprando(usuario):
    Nombre = ""

    while (Nombre != "comprar" and Nombre != "salir"):
        carro.mostrarStock()
        print("ingrese items al carrito, luego para pagar ingrese 'comprar' para salir ingrese 'salir'")
        Nombre = input("ingrese el nombre \n")
        Nombre = Nombre.strip()
        Cantidad = input("ingrese la cantidad \n")
        try:
            Cantidad = int(Cantidad)
        except ValueError:
            print("La cadena no representa un número entero válido")

        if (Nombre != "comprar" and Nombre != "salir") and carro.existe(Nombre,Cantidad):
            carro.agregarItem(Nombre,Cantidad)
        carro.mostrarCarrito()
    if(carro.mostrarCarrito() and Nombre == "comprar"):
        envio = input("Ingrese tipo de envio (internacional,programado,express,estandar)\n")
        envio2 = input("ingrese si es nacional o internacional\n")
        envio3 = input("ingrese region\n")
        calcularEnvio1 = calcularEnvio(envio2,envio3)
        print(f"precio de envio = {calcularEnvio1.getprecioEnvio()}")
        # USAR SISTEMA CENTRALIZADO para crear pedido
        idPedido = gestor_central.crear_pedido_centralizado(
            usuario.getidUsuario(),
            usuario.getDireccion(),
            carro.comprarCarrito(),
            calcularEnvio1,
            envio
        )
        
        # MOSTRAR INFORMACIÓN EXTENDIDA del tipo de pedido
        if idPedido != 0:
            pedido_creado = gestor_central.consultar_pedido_centralizado(idPedido)
            tipo_extendido = factory_pedidos.crear_pedido_extendido(envio, pedido_creado)
            
            print(f"\n🎯 INFORMACIÓN DEL PEDIDO:")
            print(f"📦 Tipo: {tipo_extendido.obtener_descripcion_tipo()}")
            
            fecha_info = tipo_extendido.calcular_fecha_estimada_entrega()
            print(f"📅 Entrega estimada: {fecha_info}")
            
            condiciones = tipo_extendido.aplicar_condiciones_especiales()
            print(f"📋 Condiciones especiales:")
            for i, condicion in enumerate(condiciones, 1):
                print(f"   {i}. {condicion}")


        print(f"idPedido = {idPedido}")
        return 1
    return 0


def pagar(usuario):
    id = int(input("Ingrese el id del pedido a pagar:\n"))
    pago = (input("Ingrese el tipo de pago (transferencia, tarjeta, entrega, cripto, qr):\n"))
    
    # USAR SISTEMA CENTRALIZADO para pagar
    resultado = gestor_central.pagar_pedido_centralizado(id, usuario.getidUsuario(), pago)
    
    if resultado != 0:
        print("✅ Pago procesado exitosamente")
    else:
        print("❌ Error al procesar el pago")
    
    return 0

def cancelar(usuario):
    id = int(input("Ingrese el id del pedido a cancelar:\n"))
    
    # USAR SISTEMA CENTRALIZADO para cancelar
    resultado = gestor_central.cancelar_pedido_centralizado(id, es_dueno=False)
    
    if resultado != 0:
        print("✅ Pedido cancelado exitosamente")
    else:
        print("❌ Error al cancelar el pedido")
    
    return 0



def inicializar():

    nombre = input("Ingrese su nombre:\n")
    direccion = input("Ingrese su direccion:\n")
    tipo = input("ingrese tipo de cliente (nuevo, frecuente, vip):\n")
    id = datos.nuevoUsuario(nombre,direccion,tipo)
    usuario = proxxy.buscarUsuario(id)
    #para pruebas
    #envio = "estandar"
    #calcularEnvio1 = calcularEnvio("nacional", "centro")
    #idPedido = gestionUsuarios.nuevoPedido(usuario.getidUsuario(), usuario.getDireccion(), carro.comprarCarrito(),calcularEnvio1, envio)
    entrada = "9"
    while(entrada != "2"):
        us = input("0 para usuario, 1 para dueño ,2 para salir:\n")
        if us == "0":

            entradaUsuario = "5"

            while(entradaUsuario != "4"):
                proxxy.mostrarPedidosUsuario(id)
                entradaUsuario = input("1) para realizar un pedido\n"
                                       "2) para pagar un pedido\n"
                                       "3) para cancelar un pedido\n"
                                       "4) para salir\n")
                match entradaUsuario:
                    case "1":
                        comprando(usuario)
                    case "2":
                        pagar(usuario)
                    case "3":
                        cancelar(usuario)
                    case "4":
                        break
                    case _:
                        print("entrada invalida")
        elif us == "1":
            entradaUsuario = "5"
            while(entradaUsuario != "4"):
                print("Pedidos en el sistema: ")
                gestionDueno.mostrar()
                entradaUsuario = input("1) para preparar un envio\n"
                                       "2) enviar un pedido\n"
                                       "3) para cancelar un pedido\n"
                                       "4) para agregar descuentos\n"
                                       "5) para salir\n")
                match entradaUsuario:
                    case "1":
                        id = int(input("Ingrese el id del pedido:\n"))
                        gestionDueno.prepararEnvio(id)
                    case "2":
                        id = int(input("Ingrese el id del pedido:\n"))
                        gestionDueno.enviarEnvio(id)
                    case "3":
                        id = int(input("Ingrese el id del pedido:\n"))
                        gestionDueno.cancelarEnvio(id)
                    case "4":
                        nombreDescuento = input("Ingrese el nombre del descuento:\n")
                        porcentaje = int(input("Ingrese el % a descontar del descuento:\n"))
                        tipo = input("Ingrese el tipo de cliente al cual se aplicara el descuento:\n")
                        gestionDueno.agregardescuento(nombreDescuento,porcentaje,tipo)
                        print("Descuento agregado satisfactoriamente\n")
                    case "5":
                        break
                    case _:
                        print("entrada invalida")








