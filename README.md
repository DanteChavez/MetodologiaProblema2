# UVShop - Sistema de Comercio Electrónico

Sistema completo de e-commerce con API REST, implementando 3 patrones de diseño para la gestión de usuarios, productos, pedidos y pagos.

## 👥 Integrantes


### API REST (Puerto 5000)
- **Gestión de Usuarios**: Crear, consultar usuarios (GET, POST)
- **Catálogo de Productos**: CRUD completo con inventario (GET, POST, PUT, DELETE)
- **Gestión de Pedidos**: CRUD completo de pedidos (GET, POST, PUT, DELETE, PATCH)
- **13 Endpoints** con operaciones CRUD completas
- **5 Métodos HTTP**: GET, POST, PUT, DELETE, PATCH
- **Arquitectura MVC**: Implementación correcta del patrón Model-View-Controller
- **Documentación**: `/api` y `/api/metodos` para información completa

## 📋 Casos de Uso

### 1. Gestión de Pedidos
- **Requisito**: Todos los pedidos deben ser registrados, modificados o consultados desde un componente único que garantice la integridad del sistema
- **Implementación**: Clase `bd` como Singleton que garantiza una única instancia compartida
- **Beneficios**: Acceso global desde distintos puntos de la aplicación sin crear múltiples instancias

### 2. Tipos de Pedido
- **Requisito**: Cada tipo de pedido tiene reglas de negocio particulares (cálculo de fecha estimada, condiciones especiales)
- **Implementación**: Factory pattern para crear tipos de pedido (estándar, express, internacional)
- **Beneficios**: Permite agregar nuevos tipos de pedido sin modificar el código existente

### 3. Clientes
- **Requisito**: Los beneficios pueden cambiar con el tiempo y deben poder agregarse o quitarse sin alterar la estructura
- **Ejemplo**: VIP: 15% + envío gratis + cashback por tiempo limitado
- **Implementación**: Sistema flexible de tipos de cliente con beneficios dinámicos

### 4. Descuentos
- **Requisito**: Los descuentos deben calcularse automáticamente según el tipo de cliente
- **Tipos implementados**:
  - Nuevo: 5% de descuento
  - Frecuente: 10%
  - VIP: 15% + envío gratis
- **Implementación**: Cálculo automático en sistema de pedidos

### 5. Gestión de Pagos
- **Métodos disponibles**:
  - Tarjeta de crédito/débito
  - Transferencia bancaria
  - Criptomonedas
  - Pago contra entrega
  - **🆕 Código QR** (nueva pasarela fintech)

- **Validaciones implementadas**:
  - Verificación de datos del cliente
  - Control de fraudes o límites
  - Registro en sistema de auditoría
  - **QR**: Geolocalización, IP segura, tokens temporales

## 🎯 Patrones de Diseño Implementados

1. **Singleton**: Base de datos centralizada (`bd`) - garantiza única instancia para gestión de pedidos
2. **Factory**: Creación de tipos de pedido y métodos de pago - extensibilidad sin modificar código existente
3. **Proxy**: Cache de usuarios y pedidos - optimización de acceso a datos

## 📁 Estructura del Proyecto

```
MetodologiaProblema2/
├── main.py                         # Punto de entrada principal (MVC)
├── test_todos_metodos.py           # Tests de la API
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Documentación del proyecto
├── ARQUITECTURA_MVC.md             # Documentación de arquitectura MVC
├── vista/                          # Capa de Vista (MVC)
│   ├── vista_rest.py               # API REST completa (MVC)
│   ├── vista_rest_simple.py        # API REST simplificada (MVC)
│   └── interfaz.py                 # Interfaz original de consola
├── modelo/                         # Capa de Modelo (MVC)
│   ├── bd.py                       # Base de datos (Singleton)
│   ├── carrito.py                  # Gestión del carrito
│   ├── factura.py                  # Sistema de facturación
│   ├── inventario.py               # Control de inventario
│   ├── pedido.py                   # Gestión de pedidos
│   ├── productos.py                # Catálogo de productos
│   ├── proxy.py                    # Cache de datos (Proxy Pattern)
│   └── usuario.py                  # Gestión de usuarios
├── controlador/                    # Capa de Controlador (MVC)
│   ├── gestionDescuentos.py        # Cálculo de descuentos
│   ├── gestionPedidos.py           # Procesamiento de pedidos (abstracta)
│   ├── gestionPedidosDueno.py      # Gestión para dueños
│   ├── gestionPedidosUsuarios.py   # Gestión para usuarios
│   ├── gestor_central_pedidos.py   # Gestor central (Singleton)
│   ├── factory_tipos_pedido.py     # Factory de tipos (Factory Pattern)
│   ├── sistema_beneficios.py       # Sistema de beneficios
│   └── pagar.py                    # Métodos de pago
└── archivos_test/                  # Archivos JSON para testing
    ├── usuario_test.json
    ├── producto_test.json
    ├── pedido_test.json
    ├── producto_update.json
    ├── pedido_update.json
    └── estado_patch.json
```

## 🏗️ Arquitectura MVC

**UVShop implementa correctamente el patrón Model-View-Controller:**

- **📱 Vista (View)**: `vista_rest.py` - API REST endpoints, manejo HTTP, serialización JSON
- **🎛️ Controlador (Controller)**: Lógica de negocio, validaciones, patrones de diseño
- **🗄️ Modelo (Model)**: Entidades, acceso a datos, persistencia

Ver `ARQUITECTURA_MVC.md` para documentación detallada.

## 🚀 Ejecución del Sistema

### Iniciar Servidor REST (Arquitectura MVC)
```bash
# Ejecutar el servidor con arquitectura MVC
python main.py

# El servidor estará disponible en:
# http://localhost:5000/api
```

### Verificar Funcionamiento
```bash
# Opción 1: Test automatizado (recomendado)
python test_todos_metodos.py

# Opción 2: Verificar manualmente
curl http://localhost:5000/api
curl http://localhost:5000/api/metodos
```

## 🌐 API REST - Ejemplos de Uso

### Opción 1: Ejecutar Test Automatizado
```bash
# Ejecuta todos los métodos HTTP con datos de prueba
python test_todos_metodos.py
```

### Opción 2: Comandos curl Manuales

#### GET - Consultar datos
```bash
# Ver todos los productos
curl http://localhost:5000/api/productos

# Ver todos los usuarios
curl http://localhost:5000/api/usuarios

# Ver todos los pedidos
curl http://localhost:5000/api/pedidos
```

#### POST - Crear nuevos registros
```bash
# Crear usuario
curl.exe -X POST http://localhost:5000/api/usuarios -H "Content-Type: application/json" --data-binary "@archivos_test/usuario_test.json"

# Crear producto
curl.exe -X POST http://localhost:5000/api/productos -H "Content-Type: application/json" --data-binary "@archivos_test/producto_test.json"

# Crear pedido
curl.exe -X POST http://localhost:5000/api/pedidos -H "Content-Type: application/json" --data-binary "@archivos_test/pedido_test.json"
```

#### PUT - Actualizar registros completos
```bash
# Actualizar producto (cambiar <codigo> por el código real)
curl.exe -X PUT http://localhost:5000/api/productos/<codigo> -H "Content-Type: application/json" --data-binary "@archivos_test/producto_update.json"

# Actualizar pedido (cambiar <idpedido> por el ID real)
curl.exe -X PUT http://localhost:5000/api/pedidos/<idpedido> -H "Content-Type: application/json" --data-binary "@archivos_test/pedido_update.json"
```

#### DELETE - Eliminar registros
```bash
# Eliminar producto (cambiar <codigo> por el código real)
curl.exe -X DELETE http://localhost:5000/api/productos/<codigo>

# Eliminar pedido (cambiar <idpedido> por el ID real)
curl.exe -X DELETE http://localhost:5000/api/pedidos/<idpedido>
```

#### PATCH - Actualización parcial
```bash
# Cambiar estado de pedido (cambiar <idpedido> por el ID real)
curl.exe -X PATCH http://localhost:5000/api/pedidos/<idpedido>/estado -H "Content-Type: application/json" --data-binary "@archivos_test/estado_patch.json"
```

## 📦 Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt

# O instalar manualmente
pip install flask flask-cors requests
```

**Tecnologías**: Python, Flask, REST API  
**Arquitectura**: MVC, Patrones de Diseño  
**Estado**: ✅ Funcional completo


![Imagen de WhatsApp 2025-07-05 a las 16 50 31_de009a2b](https://github.com/user-attachments/assets/bf7144cf-ab7c-428b-90cc-7f5a126ff9a0)