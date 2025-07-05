from abc import abstractmethod
from modelo.pedido import *

class gestionPedidos(ABC):
    def __init__(self):
        print("gestionPedidos creado")

    @abstractmethod
    def modificarPedido(self, idPedido, operacion, cambio):
        pass
    #Por ahora es solo por id
    @abstractmethod
    def cancelarPedido(self, idPedido):
        pass

    #Se interpreta recuperar pedido como: Buscar pedidos
    @abstractmethod
    def recuperarPedido(self, idPedido):
        pass