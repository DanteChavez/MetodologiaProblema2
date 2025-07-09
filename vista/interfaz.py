from modelo.bd import *
from modelo.proxy import *
from controlador.gestionPedidosUsuarios import *
from controlador.gestionPedidosDueno import *
from controlador.gestionDescuentos import *
from modelo.inventario import *
from modelo.carrito import *
datos = bd()
inventario = inventario()
carro = carrito(inventario)
proxxy = proxy(datos)
gestionDescuentosVariable = gestionDescuentos(proxxy)
gestionUsuarios = gestionPedidosUsuarios(proxxy,gestionDescuentosVariable)
gestionDueno = gestionPedidosDueno(proxxy,gestionDescuentosVariable)


@app.request('/comprar/<idUsuario/<nombre>/<cantidad>')
def comprando(idUsuario, nombre, cantidad):
    while (Nombre != "comprar" and Nombre != "salir"):
        carro.mostrarStock()
        Nombre = nombre.strip()
        try:
            cantidad = int(cantidad)
        except ValueError:
            print("La cadena no representa un número entero válido")

        if (Nombre != "comprar" and Nombre != "salir") and carro.existe(Nombre,Cantidad):
            carro.agregarItem(Nombre,cantidad)
        carro.mostrarCarrito()
    if(carro.mostrarCarrito() and Nombre == "comprar"):
        envio = input("Ingrese tipo de envio (internacional,programado,express,estandar)\n")
        envio2 = input("ingrese si es nacional o internacional\n")
        envio3 = input("ingrese region\n")
        calcularEnvio1 = calcularEnvio(envio2,envio3)
        print(f"precio de envio = {calcularEnvio1.getprecioEnvio()}")
        user = proxxy.buscarUsuario(idUsuario)
        idPedido = gestionUsuarios.nuevoPedido(idUsuario,user.getDireccion(),carro.comprarCarrito(),calcularEnvio1,envio)

        return idPedido, 200
    return 400

@app.route('/pagar/<idPedido>/<pago>')
def pagar(idPedido, pago):
    pedido = proxxy.recuperarPedido(idPedido)
    idUsuario = pedido.getidUsuario()
    result = gestionUsuarios.pagarPedido(idPedido,idUsuario,pago)
    return result
@app.route('/cancelar/<idPedido>')
def cancelar(idPedido):
    result = gestionUsuarios.cancelarPedido(idPedido)
    return result

@app.route('/usuario/<operacion>/<eleccion>/<nombre>/<direccion>/<tipo>', methods=["POST"])
def inicializar(nombre, direccion, tipo, operacion):
    id = datos.nuevoUsuario(nombre,direccion,tipo)
    usuario = proxxy.buscarUsuario(id)
    #para pruebas
    #envio = "estandar"
    #calcularEnvio1 = calcularEnvio("nacional", "centro")
    #idPedido = gestionUsuarios.nuevoPedido(usuario.getidUsuario(), usuario.getDireccion(), carro.comprarCarrito(),calcularEnvio1, envio)
    entrada = "9"
    if operacion == "0": # Pago
        data = proxxy.mostrarPedidosUsuario(id)
        
    while(entrada != "2"):
        if operacion == "0":

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
        elif operacion == "1":
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








