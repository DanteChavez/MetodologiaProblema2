from abc import ABC


class pedido:
    def __init__(self,idUsuario,direccion ,idPedido, estado, productos,precioEnvio, factura):
        self.idUsuario = idUsuario #numero
        self.direccion = direccion #string
        self.idPedido = idPedido #int
        self.estado = estado    #string
        self.productos = productos  #lista de productos
        self.productosPagados = None    #lista de productos
        self.tipoEnvio = None   #string
        self.precioEnvio = precioEnvio  #clase calcularEnvio
        self.factura = factura

    def saludar(self):
        print("funcionaaaaa!!!!")

    def getidUsuario(self):
        return self.idUsuario

    def getdireccion(self):
        return self.direccion

    def getidPedido(self):
        return self.idPedido
    #pendiente, pagado, preparacion, enviado, entregado, cancelado.
    def getestado(self):
        return self.estado

    def getproductos(self):
        return self.productos


    def getproductosPagados(self):
        return self.productosPagados


    def setproductosPagados(self,productos):
        self.productos = productos
    def setdireccion(self,direccion):
        self.direccion = direccion

    def setestado(self,estado):
        self.estado = estado

    def setproductos(self,productos):
        self.productos = productos

    def gettotalReal(self):
        return self.factura.gettotalReal()

    def getprecioEnvioPedido(self): #Para diferenciar de la otra funcion
        return self.precioEnvio.getprecioEnvio()

    def setprecioEnvioPedido(self,precioEnvio):
        self.precioEnvio.setprecioEnvio(precioEnvio)

    def setprecioEnvioPedido2(self,precioEnvio):
        self.precioEnvio = precioEnvio
    
#son la misma funcion, pero en el enunciado decia que eran distintas
#por lo que son distintas xd
#de este modo no se rompe el "Principio de Substitución de Liskov"
class pedidointernacional(ABC, pedido):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = None
class pedidoprogramado(ABC, pedido):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = None
class pedidoexpress(ABC, pedido):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = None
class pedidoestandar(ABC, pedido):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = None


class internacional(pedidointernacional):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = internacional

class programado(pedidoprogramado):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = programado

class express(pedidoexpress):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = express

class estandar(pedidoestandar):
    def __init__(self, idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura):
        super().__init__(idUsuario, direccion, idPedido, estado, productos, precioEnvio, factura)
        self.tipoEnvio = estandar


PRECIOS = {
    "nacional": {
        "norte": 7000,
        "centro": 2000,
        "sur": 6500
    },
    "internacional": {
        "america": 15000,
        "europa": 12000,
        "africa": 25000,
        "asia": 8000,
        "oceania": 7000
    }
}





class calcularEnvio():
    def __init__(self,tipo,region):
        self.tipo = tipo #internacional o nacional
        self.region = region
        self.precioEnvio = self.calcularPrecio(tipo,region)

    def calcularPrecio(self, tipo, region):
        try:
            return PRECIOS[tipo.lower()][region.lower()]
        except KeyError:
            #raise ValueError(f"Combinación no válida: tipo={tipo}, región={region}")
            print(f"Combinación no válida: tipo={tipo}, región={region}")
            return 999999999

    def modificarPrecio(self,tipo,region):
        self.tipo = tipo
        self.region = region
        self.precioEnvio = self.calcularPrecio(tipo, region)

    def getprecioEnvio(self):
        return self.precioEnvio

    def gettipo(self):
        return self.tipo
    def getregion(self):
        return self.region
    def setprecioEnvio(self,precioEnvio):
        self.precioEnvio = precioEnvio


