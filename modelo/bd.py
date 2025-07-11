from modelo.usuario import *
class bd():
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def __init__(self):
        self.listaPedidos = {}
        self.listaUsuarios = {}
        self.idContadorUsuarios = 1



    def agregarPedido(self, pedido):
        if not hasattr(pedido, 'getidPedido'):
            #raise ValueError("El objeto no parece ser un Pedido válido")
            return 400
        # getidPedido() devuelve (id, status_code), necesitamos solo el id
        pedido_id = pedido.getidPedido()[0] if isinstance(pedido.getidPedido(), tuple) else pedido.getidPedido()
        self.listaPedidos[pedido_id] = pedido
        return 200
    def recuperarPedido(self, idPedido):
        if idPedido not in self.listaPedidos:
            return 404
        return jsonify(self.listaPedidos[idPedido]), 200

    def mostrarPedidos(self):
        retorno = {}
        if not self.listaPedidos:
            return 404

        for id_pedido in self.listaPedidos:
            retorno.update({"ID":id_pedido,"estado" :self.listaPedidos[id_pedido].estado})
            return jsonify(retorno), 200
    def mostrarPedidosUsuario(self,idUsuario):
        if not self.listaPedidos:
            return 404

        for id_pedido in self.listaPedidos:
            rec = self.listaPedidos[id_pedido]
            if(idUsuario == rec.getidUsuario()):
                retorno = {"ID:":id_pedido,"estado:":self.listaPedidos[id_pedido].estado,"precio":self.listaPedidos[id_pedido].gettotalReal()}
                return jsonify(retorno), 200 
    #esto es como para simular guardar usuarios en la "base de datos"
    #es mas que nada para que sea global
    def nuevoUsuario(self,nombre, direccion, tipoCliente):
        nuevo = usuario(self.idContadorUsuarios,nombre,direccion, tipoCliente)
        self.idContadorUsuarios = self.idContadorUsuarios + 1
        self.listaUsuarios[nuevo.getidUsuario()] = nuevo
        return self.idContadorUsuarios-1, 201

    def buscarUsuario(self,idUsuario):
        if idUsuario in self.listaUsuarios:
            return jsonify(self.listaUsuarios[idUsuario]), 200
        else:
            print(f"No hay usuario registrado en la base de datos con la id: {idUsuario} ")
            return 404
