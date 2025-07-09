from controlador.gestionPedidos import *
from modelo.factura import *
from modelo.pedido import *
from controlador.pagar import *


class gestionPedidosUsuarios(gestionPedidos):
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    def __init__(self,datos,descuentos):
        self.datos = datos #la bd
        self.idConteo = 1
        self.descuentos = descuentos
    #recuperar pedido por id
    def recuperarPedido(self, idPedido):
        pedido = self.datos.recuperarPedido(idPedido)
        if(pedido != 0):
            return pedido
        else:
            print("Pedido no existe")
            return 0

    #Ingresa los datos para un nuevo pedido, si el retorno es 0 se produjo un error
    #de lo contrario se retorna el idPedido
    def nuevoPedido(self,idUsuario, direccion, carro, precioEnvio, tipoEnvio):
        if(self.datos.buscarUsuario(idUsuario) == 0):
            print("Usuario no existe")
            return 0
        nuevaCompra = ""
        precioCarro = self.mostrarPrecioCarrito(carro)
        precioEnvio2 = precioEnvio.getprecioEnvio()
        precioDescuentos = self.descuentos.calcularDescuentos(idUsuario)
        if(precioDescuentos[1] == 1):
            precioEnvio2 = 0
        print("***** Descuentos *****")
        for i in precioDescuentos[2]:
            print(f"Descuento '{i}' aplicado")
        print("*****            *****\n")
        descuento = precioDescuentos[0]
        match tipoEnvio:
            case "internacional":
                impuestos = 1.3
                boleta = factura(carro, precioCarro, precioEnvio2, precioDescuentos[0], precioEnvio2, impuestos)
                nuevaCompra = internacional(idUsuario, direccion,self.idConteo, "pendiente", carro, precioEnvio, boleta)
            case "programado":
                impuestos = 1
                boleta = factura(carro, precioCarro, precioEnvio2, precioDescuentos[0], precioEnvio2, impuestos)
                nuevaCompra = programado(idUsuario, direccion, self.idConteo, "pendiente", carro, precioEnvio, boleta)
            case "express":
                impuestos = 1.15
                boleta = factura(carro, precioCarro, precioEnvio2, precioDescuentos[0], precioEnvio2, impuestos)
                nuevaCompra = express(idUsuario, direccion, self.idConteo, "pendiente", carro, precioEnvio, boleta)
            case "estandar":
                impuestos = 1
                boleta = factura(carro, precioCarro, precioEnvio2, precioDescuentos[0], precioEnvio2, impuestos)
                nuevaCompra = estandar(idUsuario, direccion, self.idConteo, "pendiente", carro, precioEnvio, boleta)
            case _:
                print("wtf?")#TODO devolver items al carrito
                return 0
        self.idConteo += 1
        print("Pedido agregado de manera satisfactoria :D")
        self.datos.agregarPedido(nuevaCompra)
        return self.idConteo-1
    def modificarPedido(self, idPedido,operacion,cambio):
        retorno = self.recuperarPedido(idPedido)
        if(retorno != 0 and retorno.getestado() != "cancelado"):
            #1 cambiar direccion
            #2 cambiar estado
            #3 cambiar productos
            #4 cambiar precioEnvio
            match operacion:
                case 1:
                    retorno.setdireccion(cambio)
                case 2:
                    retorno.setestado(cambio)
                case 3:
                    if(retorno.getestado() == "pendiente"):
                        retorno.setproductos(cambio)
                    else:
                        print("Pedido solo se puede cambiar si esta pendiente")
                case 4:
                    if(retorno.getestado() == "pendiente"):
                        retorno.setprecioEnvioPedido2(cambio) #todo ver que onda
                    else:
                        print("Pedido solo se puede cambiar si esta pendiente")

                case _:
                    print("modificacion NO valida")
                    return 0
            return 1

        else:
            print("No se encuentra el pedido o esta cancelado")
            return 0
    #es bastante redundante con la funcion anterior,pero asi es la vida
    def cancelarPedido(self, idPedido):
        retorno = self.recuperarPedido(idPedido)
        if (retorno != 0 and retorno.getestado() != "cancelado"):
            retorno.setestado("cancelado")
            return 200
        else:
            print("No se encuentra el pedido o ya esta cancelado")
            return 404

#gestionPedidosUsuarios realiza muchas acciones: gestionar pedidos, calcular descuentos, manejar pagos, etc.
    def pagarPedido(self, idPedido, idUsuario,tipoPago):
        usuario = self.datos.buscarUsuario(idUsuario)
        pedido = self.datos.recuperarPedido(idPedido)
        if(pedido != 0 and usuario != 0 and pedido.getestado() == "pendiente" ):
            res = 0
            fabrica = None
            match tipoPago:
                case "transferencia":
                    fabrica = Fabricatransferencia()
                case "tarjeta":
                    fabrica = FabricaTarjeta()
                case "entrega":
                    fabrica = FabricaEntrega()
                case "cripto":
                    fabrica = FabricaCripto()
                case "qr":
                    fabrica = FabricaQR()
            res = procesarPago(fabrica, pedido.gettotalReal(), usuario.getnombre())
            if (res == 400):
                print("Pago no completado")
            elif(res == 200 ):
                print("Pago completado")
                pedido.setestado("pagado")
            return 201
        else:
            print("No se pudo completar el pago")
            return 400

    def mostrarPrecioCarrito(self, carrito):
        resultado = [0,0,0,0,0]
        #es para que nada para que esta funcion solo haga lo que debe hacer, ya otra imprimira los resultados
        #[0] precio normal
        #[1] precio envio normal
        #[2] precio con descuentos
        #[3] precio envio con descuentos
        #[4] precio total
        precio = 0
        for clave in carrito:
            precio += carrito[clave] * clave.getprecioUnitario()
        return precio

"""
    def pagarPedido(self, idPedido, idUsuario,tipoPago):
        usuario = self.datos.buscarUsuario(idUsuario)
        pedido = self.datos.recuperarPedido(idPedido)
        if(pedido != 0 and usuario != 0 and pedido.getestado() == "pendiente" ):
            res = 0
            match tipoPago:
                case "transferencia":
                    fabricaTransferencia = Fabricatransferencia()
                    res = procesarPago(fabricaTransferencia, pedido.gettotalReal(), usuario.getnombre())
                case "tarjeta":
                    fabrica_tarjeta = FabricaTarjeta()
                    res = procesarPago(fabrica_tarjeta, pedido.gettotalReal(), usuario.getnombre())
                case "entrega":
                    fabrica_cripto = FabricaEntrega()
                    res = procesarPago(fabrica_cripto, pedido.gettotalReal(), usuario.getnombre())
                case "cripto":
                    fabrica_entrega = FabricaCripto()
                    res = procesarPago(fabrica_entrega, pedido.gettotalReal(), usuario.getnombre())
                
            if (res == 0):
                print("Pago no completado")
            elif(res == 1):
                print("Pago completado")
                pedido.setestado("pagado")
            return 1
        else:
            print("No se pudo completar el pago")
            return 0
"""