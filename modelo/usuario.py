class usuario():
    def __init__(self,idUsuario,nombre,direccion,tipoCliente):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.direccion = direccion
        self.tipoCliente = tipoCliente
#todo restringir a los 3 tipos de cliente solamente
#
#Este no es tan importante, hacer al final
        self.compras = {}

    #nuevo frecuente vip

    def getidUsuario(self):
        return self.idUsuario
    def getnombre(self):
        return self.nombre
    def getDireccion(self):
        return self.direccion
    def getTipoCliente(self):
        return self.tipoCliente



    def setDireccion(self,direccion):
        self.direccion = direccion
    def setTipoCliente(self,tipoCliente):
        self.tipoCliente = tipoCliente
    def setCompra(self,compra):
        self.compras = compra
    def anadircompra(self,idcompra,compra):
        self.compras[idcompra] = compra

