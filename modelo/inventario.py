from modelo.productos import *
class inventario:
    def __init__(self):
        #En esta clase y en carrito se va a manejar el inventario por "punteros"
        #Se pasa el objeto entero al carrito cuando el usuario seleccione alguno
        #luego se busca ese mismo objeto para descontar del stock
        #esta clase (por ahora) es solo para mostrar, ver si existe y borrar
        self.itemsPrimero = [
            productos("computadores", 1, 1000, 20),
            productos("celulares", 2, 1200, 30),
            productos("televisores", 3, 800, 15),
            productos("tablet", 4, 600, 25),
            productos("audifonos", 5, 150, 50),
            productos("impresoras", 6, 300, 10),
            productos("consolas", 7, 500, 18),
            productos("smartwatch", 8, 250, 35),
            productos("camaras", 9, 700, 12),
            productos("altavoces", 10, 200, 40)
            ]
        #para manejar por nombres la lista, mas comodo
        self.items = {producto.nombre: producto for producto in self.itemsPrimero}

    def mostrarInventario(self): #NOTA: las cosas raras son para imprimir el texto de forma bonita
        print("\nItems disponibles en el catálogo")
        print("************************************")
        for nombre in sorted(self.items.keys()):
            producto = self.items[nombre]
            print(f"Nombre: {nombre.ljust(15)} Precio: ${str(producto.precioUnitario).ljust(6)} Stock: {producto.stock}")
        print("************************************")

    #tomar un item de acuerdo a un nombre proporcionado y un stock
    #si el stock es valido se verifica en carrito o en descontar (al borrar)
    def getitem(self,entrada,cantidad):
        if entrada in self.items:
            if 0 < self.items[entrada].stock and  self.items[entrada].stock >= cantidad:
                return self.items[entrada]
            else:
                print("No existe stock disponible")
                return None
        else:
            print(f"'{entrada}' no es un producto valido ")
            return None
    #descotnar del stock, la entrada es el objeto producto
    def descontar(self, entrada, cantidad):
        if entrada in self.items: #por si acaso 2 veces
            if 0 < self.items[entrada].stock and self.items[entrada].stock >= cantidad:
                self.items[entrada].stock -= cantidad
                return True
            else:
                print(f"Error al descontar {entrada} con la cantidad {cantidad}")
                return False

        else:
            print(f"El siguiente producto no existe: {entrada} ")
            return False
    def agregar(self, entrada, cantidad):
        if entrada in self.items: #por si acaso 2 veces
            if 0 < self.items[entrada].stock and self.items[entrada].stock >= cantidad:
                self.items[entrada].stock += cantidad
                return True
            else:
                print(f"Error al agregar {entrada} con la cantidad {cantidad}")
                return False

        else:
            print(f"El siguiente producto no existe: {entrada} ")
            return False


"""USO DE INVENTARIO
tienda = inventario()
tienda.mostrarInventario()
print(tienda.getitem("consolas",5))
tienda.descontar("consolas",5)
tienda.mostrarInventario()

"""