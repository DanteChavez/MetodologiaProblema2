from controlador.gestionPedidos import gestionPedidos


class gestionPedidosDueno(gestionPedidos):
    def __init__(self,datos,descuentos):
        self.datos = datos
        self.descuentos = descuentos

    def recuperarPedido(self, idPedido):
        pedido = self.datos.recuperarPedido(idPedido)
        if(pedido != 0):
            return pedido
        else:
            print("Pedido no existe")
            return 0


    def modificarPedido(self, idPedido,operacion,cambio):
        retorno = self.recuperarPedido(idPedido)
        if(retorno != 0 and retorno.getestado() != "cancelado" and retorno.getestado() != "pendiente"):
            #1 cambiar estado
            match operacion:
                case 1:
                    retorno.setestado(cambio)
                case _:
                    print("modificacion NO valida")
                    return 0
            return 1

        else:
            print("No se encuentra el pedido, esta cancelado o pendiente")
            return 0

    def prepararEnvio(self, idPedido):
        retorno = self.recuperarPedido(idPedido)
        if(retorno.getestado() == "pagado"):
            retorno.setestado("preparacion")

        else:
            print("No se encuentra el pedido, esta cancelado o pendiente")
            return 0

    def enviarEnvio(self, idPedido):
        retorno = self.recuperarPedido(idPedido)
        if(retorno.getestado() == "preparacion"):
            retorno.setestado("enviado")
        else:
            print("No se encuentra el pedido, esta cancelado o pendiente")
            return 0
    def cancelarEnvio(self, idPedido):
        retorno = self.recuperarPedido(idPedido)
        if(retorno.getestado() != "cancelado"):
            retorno.setestado("cancelado")
        else:
            print("No se encuentra el pedido, esta cancelado o pendiente")
            return 0
    #es bastante redundante con la funcion anterior,pero asi es la vida
    def cancelarPedido(self, idPedido):
        retorno = self.recuperarPedido(idPedido)
        if (retorno != 0 and retorno.getestado() != "cancelado"):
            retorno.setestado("cancelado")
        else:
            print("No se encuentra el pedido o esta cancelado")
            return 0
    def mostrar(self):
        self.datos.mostrarPedidos()

    def agregardescuento(self,nombre, descuento,tipoCliente):
        self.descuentos.nuevoDescuento(nombre,descuento,tipoCliente)
        return 1