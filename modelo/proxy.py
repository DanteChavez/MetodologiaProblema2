import random

#La clase proxy lo que hace es almacenar en 'cache' los usuarios y pedidos que se van consultando por TO DO  el programa
#Si estan en cache no se accede a la base de datos y solo se retorna el dato del cache, pero si no estan se busca en la bd
#El cache tiene tamaño 5, si se sobrepasa, se elimina un usuario/pedido al azar del cache para hacer espacio a otro
class proxy():
    def __init__(self,datos):
        self.listaUsuarios = {}
        self.contadorUsuarios = 0
        self.listaPedidos = {}
        self.contadorPedidos = 0
        self.datos = datos

    def buscarUsuario(self, idUsuario):
        if idUsuario in self.listaUsuarios:
            return self.listaUsuarios[idUsuario], 200
        else:
            nuevo = None
            if(len(self.listaUsuarios) > 5):
                borrar = random.choice(list(self.listaUsuarios))
                self.listaUsuarios.pop(borrar)
        nuevo = self.datos.buscarUsuario(idUsuario)
        self.listaUsuarios[idUsuario] = nuevo
        return nuevo, 201

    def recuperarPedido(self, idUsuario):
        if idUsuario in self.listaPedidos:
            return self.listaPedidos[idUsuario], 200
        else:
            nuevo = None
            if(len(self.listaPedidos) > 5):
                borrar = random.choice(list(self.listaPedidos))
                self.listaPedidos.pop(borrar)
        nuevo = self.datos.recuperarPedido(idUsuario)
        self.listaPedidos[idUsuario] = nuevo
        return nuevo, 200

    def agregarPedido(self, pedido):
        r = self.datos.agregarPedido(pedido)
        return r
    def mostrarPedidos(self):
        r = self.datos.mostrarPedidos()
        return r
    def mostrarPedidosUsuario(self,idUsuario):
        r = self.datos.mostrarPedidosUsuario(idUsuario)
        return r
    def nuevoUsuario(self,nombre, direccion, tipoCliente):
        r = self.datos.nuevoUsuario(nombre, direccion, tipoCliente)
        return r
