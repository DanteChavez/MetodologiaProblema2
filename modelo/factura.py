class factura:
    def __init__(self, productos, totalProductos, totalEnvio, descuentosUsuario, descuentosEnvio, impuestos):
        self.productos = productos
        self.totalProductos = totalProductos
        self.totalEnvio = totalEnvio
        self.descuentosUsuario = descuentosUsuario
        self.descuentosEnvio = descuentosEnvio
        self.impuestos = impuestos
        self.estado = "pendiente"
        self.totalReal = self.calcularTotal()

    def pagado(self):
        self.estado = "pagado"

    def calcularTotal(self):
        suma = (self.totalProductos * self.descuentosUsuario + self.descuentosEnvio) * self.impuestos
        return suma
    def gettotalReal(self):
        return self.totalReal
