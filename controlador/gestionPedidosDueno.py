from controlador.gestionPedidos import gestionPedidos

class gestionPedidosDueno(gestionPedidos):
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
        
    def __init__(self, datos=None, descuentos=None):
        # Importar aquí para evitar imports circulares
        if datos is None:
            from modelo.bd import bd
            from modelo.proxy import proxy
            bd_instance = bd()
            datos = proxy(bd_instance)
        
        if descuentos is None:
            try:
                from controlador.gestionDescuentos import gestionDescuentos
                descuentos = gestionDescuentos()
            except:
                descuentos = None
                
        self.datos = datos
        self.descuentos = descuentos
    
    def recuperarPedido(self, idPedido):
        """Recuperar un pedido específico (método del controlador, sin decorador Flask)"""
        try:
            pedido = self.datos.recuperarPedido(idPedido)
            if pedido != 404:
                pedido_data = {
                    'idUsuario': pedido.getidUsuario(),
                    'direccion': pedido.getdireccion(),
                    'idPedido': pedido.getidPedido(),
                    'estado': pedido.getestado(),
                    'productos': pedido.getproductos(),
                    'precioEnvio': getattr(pedido, 'precioEnvio', None)
                }
                return pedido_data, 200
            else:
                return {'error': 'Pedido no existe'}, 404
        except Exception as e:
            return {'error': f'Error al recuperar pedido: {str(e)}'}, 500


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