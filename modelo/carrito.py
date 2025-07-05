from modelo.inventario import *
class carrito:
    def __init__(self,inventario):
        self.productosDisponibles = inventario
        self.lista = {}
        self.totalPrecio = 0

    def agregarItem(self, item,cantidad):
        agregar = self.productosDisponibles.getitem(item,cantidad)
        if(agregar is not None):
            print(f"\nSe agregaron {cantidad} {item} al carrito")
            self.lista[agregar] = self.lista.get(agregar, 0) + cantidad
            self.totalPrecio += agregar.getprecioUnitario() * cantidad
        else:
            print("el item no se pudo agregar")

    def mostrarCarrito(self):
        if (len(self.lista) == 0):
            print("No hay items en el carrito")
            return False
        else:
            print("\nItems en el carrito:")
            print("************************************")
            for clave, valor in self.lista.items():
                print(f"Item: {clave.nombre} con la cantidad {valor} (cada uno a ${clave.getprecioUnitario()})")

            print(f"Precio total: ${self.totalPrecio} ")
            print("************************************")
            return True


    def mostrarStock(self):
        self.productosDisponibles.mostrarInventario()
    def quitarItem(self, item, cantidad):
        agregar = self.productosDisponibles.getitem(item,cantidad)
        if(agregar is not None and agregar in self.lista.keys()):
            if(self.lista[agregar] >= cantidad):
                print(f"\nSe descontaron {cantidad} {agregar.getnombre()}  ")
                self.totalPrecio -= agregar.getprecioUnitario() * cantidad
                self.lista[agregar] -= cantidad
                if self.lista[agregar] <= 0:
                    del self.lista[agregar]
            else:
                print(f"\nSe desconto {self.lista[agregar]} en vez de {cantidad}")
                self.lista[agregar] -= self.lista[agregar]

        else:
            print("el item no se pudo agregar")
    #se usa copy() para no pasarle el original/carro del sistema
    def comprarCarrito(self):
        copia = {}
        for clave, valor in self.lista.items():
            if self.productosDisponibles.descontar(clave.getnombre(),valor):
                copia[clave] = valor
        self.lista.clear()
        return copia
    def existe(self, entrada,cantidad):
        a = self.productosDisponibles.getitem(entrada,cantidad)
        if(a != None):
            return True
        return False

"""USO
carro = carrito()
carro.mostrarStock()
carro.agregarItem("altavoces2",3)
carro.agregarItem("altavoces",6)
carro.mostrarCarrito()

carro.quitarItem("altavoces",2)
carro.mostrarCarrito()



"""