class productos:
    def __init__(self,nombre, codigo, precioUnitario, stock):
        self.nombre = nombre
        self.codigo = codigo
        self.precioUnitario = precioUnitario
        self.stock = stock

    def getnombre(self):
        return self.nombre
    def getcodigo(self):
        return self.codigo
    def getprecioUnitario(self):
        return self.precioUnitario
    def getstock(self):
        return self.stock