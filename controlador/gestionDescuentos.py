#Clase creada gracias al feedback realizado por el profesor
#Comentario:
#gestionPedidosUsuarios realiza muchas acciones: gestionar pedidos, calcular descuentos, manejar pagos, etc.
#Ahora esta clase maneja totalmente los descuentos
"""
Clientes
● Los beneficios pueden cambiar con el tiempo y deben poder agregarse o quitarse sin alterar la estructura de las clases cliente.
● Imagine que hay un beneficio o descuento que por un tiempo limitado mejora sus características base. Por ejemplo: VIP: 15% + envío gratis + cashback
4. Descuentos
● Los descuentos deben calcularse automáticamente según el tipo de cliente.
● Por ejemplo:
○ Nuevo: 5% de descuento.
○ Frecuente: 10%.
○ VIP: 15% + envío gratis.
"""


class gestionDescuentos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    def __init__(self, datos):
        self.datos = datos
        #una lista para cada tipo de descuento, podria estar mejor implementado
        #pero asi es mas rapido
        self.listaN = {}
        self.listaF = {}
        self.listaV = {}
    def calcularDescuentosTipoCliente(self, idUsuario):
        usuario = self.datos.buscarUsuario(idUsuario)
        descuento = [1, 0, 0]
        print(f"tipo : {usuario.getTipoCliente()}")
        match usuario.getTipoCliente():
            case "nuevo":
                descuento[0] = 0.95
            case "frecuente":
                descuento[0] = 0.90
            case "vip":
                descuento[0] = 0.85
                descuento[1] = 1
        return descuento
    def nuevoDescuento(self, nombre, descuento,tipoCliente):
        match tipoCliente:
            case "nuevo":
                self.listaN[nombre] = descuento
            case "frecuente":
                self.listaF[nombre] = descuento
            case "vip":
                self.listaV[nombre] = descuento
    def quitarDescuento(self, nombre,tipoCliente):
        match tipoCliente:
            case "nuevo":
                del self.listaN[nombre]
            case "frecuente":
                del self.listaF[nombre]
            case "vip":
                del self.listaV[nombre]
    def calcularLista(self,lista):
        variable = 1
        aplicados = []
        for llave in lista:
            variable = variable * lista[llave]
            aplicados.append(llave)
        return [variable, aplicados]

    def calcularDescuentos(self, idUsuario):
        usuario = self.datos.buscarUsuario(idUsuario)
        descuentos = [0,0,0]
        descuentos = self.calcularDescuentosTipoCliente(idUsuario)
        match usuario.getTipoCliente():
            # todo implementar bien
            #funciona con el codigo ya existente pero xd
            case "nuevo":
                calcularlista = self.calcularLista(self.listaN)
                descuentos[0]= descuentos[0] * calcularlista[0]
                descuentos[2] = calcularlista[1]
                descuentos[2].append("cliente nuevo")
            case "frecuente":
                calcularlista = self.calcularLista(self.listaF)
                descuentos[0]= descuentos[0] * calcularlista[0]
                descuentos[2] = calcularlista[1]
                descuentos[2].append("cliente frecuente")
            case "vip":
                calcularlista = self.calcularLista(self.listaV)
                descuentos[0]= descuentos[0] * calcularlista[0]
                descuentos[2] = calcularlista[1]
                descuentos[2].append("cliente vip")
        return descuentos
"""
datos = bd()
# = usuario("1","Dante","micasa","nuevo")
usuario = datos.nuevoUsuario("Dante","Micasa","vip")
precio = gestionDescuentos(datos)
precio.nuevoDescuento("Cash Back", 1,"vip")
var = (precio.calcularDescuentos(1))
for i in var[2]:
    print(f"descuentos : {i}")
"""
