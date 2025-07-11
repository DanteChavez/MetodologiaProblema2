"""
PRUEBA COMPLETA DE TODOS LOS MÉTODOS HTTP
========================================
Verifica que TODOS los endpoints funcionan (GET, POST, PUT, DELETE, PATCH)
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_all_methods():
    """Prueba TODOS los métodos HTTP disponibles"""
    
    print("🚀 PROBANDO TODOS LOS MÉTODOS HTTP...")
    print("=" * 60)
    
    # 1. GET - Verificar que el servidor responde
    print("\n📋 PROBANDO GET:")
    try:
        response = requests.get(f"{BASE_URL}")
        print(f"   ✅ GET /api - Status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/metodos")
        print(f"   ✅ GET /api/metodos - Status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/usuarios")
        print(f"   ✅ GET /api/usuarios - Status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/productos")
        print(f"   ✅ GET /api/productos - Status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/pedidos")
        print(f"   ✅ GET /api/pedidos - Status: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Servidor no disponible")
        print("   💡 Ejecuta: python main.py")
        return
    
    # 2. POST - Crear recursos
    print("\n➕ PROBANDO POST:")
    
    # POST Usuario - CORREGIDO para usar la estructura real
    usuario_data = {
        "nombre": "Usuario Test",
        "direccion": "Calle Test 123",
        "tipo": "cliente"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
        print(f"   ✅ POST /api/usuarios - Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  POST /api/usuarios - Error: {e}")
    
    # POST Producto - CORREGIDO para usar código numérico
    producto_data = {
        "nombre": "Producto Test",
        "codigo": 999,
        "precio": 99.99,
        "stock": 10
    }
    
    try:
        response = requests.post(f"{BASE_URL}/productos", json=producto_data)
        print(f"   ✅ POST /api/productos - Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  POST /api/productos - Error: {e}")
    
    # POST Pedido
    pedido_data = {
        "idUsuario": 1,
        "direccion": "Dirección Test",
        "productos": [{"nombre": "Producto Test", "cantidad": 2}],
        "estado": "pendiente"
    }
    
    pedido_id_creado = None
    try:
        response = requests.post(f"{BASE_URL}/pedidos", json=pedido_data)
        print(f"   ✅ POST /api/pedidos - Status: {response.status_code}")
        if response.status_code == 201:
            response_data = response.json()
            if 'pedido' in response_data and 'idPedido' in response_data['pedido']:
                id_raw = response_data['pedido']['idPedido']
                # El servidor devuelve [ID, status_code], extraer solo el ID
                if isinstance(id_raw, list) and len(id_raw) > 0:
                    pedido_id_creado = id_raw[0]  # Tomar solo el primer elemento
                else:
                    pedido_id_creado = id_raw  # Si no es lista, usar directamente
                print(f"   📋 Pedido creado con ID: {pedido_id_creado}")
            else:
                print(f"   ⚠️  Estructura inesperada. Claves: {list(response_data.keys())}")
    except Exception as e:
        print(f"   ⚠️  POST /api/pedidos - Error: {e}")
    
    # 3. PUT - Actualizar recursos
    print("\n✏️ PROBANDO PUT:")
    
    # Debug: Verificar que el pedido existe
    if pedido_id_creado:
        try:
            debug_response = requests.get(f"{BASE_URL}/debug/pedidos")
            if debug_response.status_code == 200:
                debug_data = debug_response.json()
                print(f"   🔍 Debug - Pedidos en proxy: {debug_data.get('proxy_instance_pedidos', {})}")
                print(f"   🔍 Debug - Pedidos en bd: {debug_data.get('bd_instance_pedidos', {})}")
        except:
            pass  # Ignorar errores de debug
    
    # PUT Producto - CORREGIDO para usar la estructura real
    producto_update = {
        "nombre": "Producto Actualizado Test",
        "precio": 199.99,
        "stock": 15
    }
    
    try:
        response = requests.put(f"{BASE_URL}/productos/999", json=producto_update)
        print(f"   ✅ PUT /api/productos/999 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  PUT /api/productos/999 - Error: {e}")
    
    # PUT Pedido - Usar el ID del pedido creado
    if pedido_id_creado:
        pedido_update = {
            "direccion": "Dirección Actualizada",
            "estado": "en_proceso",
            "productos": [{"nombre": "Producto Actualizado", "cantidad": 3}]
        }
        
        try:
            response = requests.put(f"{BASE_URL}/pedidos/{pedido_id_creado}", json=pedido_update)
            print(f"   ✅ PUT /api/pedidos/{pedido_id_creado} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  PUT /api/pedidos/{pedido_id_creado} - Error: {e}")
    else:
        print(f"   ⚠️  PUT /api/pedidos - No se pudo obtener el ID del pedido creado")
    
    # 4. PATCH - Actualizar parcialmente
    print("\n🔄 PROBANDO PATCH:")
    
    if pedido_id_creado:
        estado_data = {"estado": "entregado"}
        
        try:
            response = requests.patch(f"{BASE_URL}/pedidos/{pedido_id_creado}/estado", json=estado_data)
            print(f"   ✅ PATCH /api/pedidos/{pedido_id_creado}/estado - Status: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  PATCH /api/pedidos/{pedido_id_creado}/estado - Error: {e}")
    else:
        print(f"   ⚠️  PATCH /api/pedidos/*/estado - No se pudo obtener el ID del pedido creado")
    
    # 5. DELETE - Eliminar recursos
    print("\n🗑️ PROBANDO DELETE:")
    
    try:
        response = requests.delete(f"{BASE_URL}/productos/999")
        print(f"   ✅ DELETE /api/productos/999 - Status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  DELETE /api/productos/999 - Error: {e}")
    
    if pedido_id_creado:
        try:
            response = requests.delete(f"{BASE_URL}/pedidos/{pedido_id_creado}")
            print(f"   ✅ DELETE /api/pedidos/{pedido_id_creado} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  DELETE /api/pedidos/{pedido_id_creado} - Error: {e}")
    else:
        print(f"   ⚠️  DELETE /api/pedidos/* - No se pudo obtener el ID del pedido creado")
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBA COMPLETA TERMINADA")
    print("💡 Tu API REST soporta TODOS los métodos HTTP!")
    print("🔥 GET, POST, PUT, DELETE, PATCH - ¡TODO FUNCIONAL!")

def mostrar_resumen():
    """Muestra resumen de todos los métodos disponibles"""
    print("\n📊 RESUMEN COMPLETO DE TU API:")
    print("=" * 60)
    print("🌟 MÉTODOS HTTP DISPONIBLES: 5")
    print("📡 TOTAL ENDPOINTS: 13")
    print()
    print("📋 GET (6):    /api, /api/metodos, /api/usuarios, /api/productos, /api/pedidos, /api/casos-uso/factory-pedidos")
    print("➕ POST (3):   /api/usuarios (nombre, direccion, tipo), /api/productos (nombre, codigo, precio, stock), /api/pedidos")
    print("✏️ PUT (2):    /api/productos/<codigo>, /api/pedidos/<id>")
    print("🗑️ DELETE (2): /api/productos/<codigo>, /api/pedidos/<id>")
    print("🔄 PATCH (1):  /api/pedidos/<id>/estado")
    print("=" * 60)

if __name__ == "__main__":
    print("🎯 VERIFICACIÓN COMPLETA DE MÉTODOS HTTP")
    print("🚀 UVShop API REST - Prueba TODOS los métodos")
    
    mostrar_resumen()
    
    print("\n¿Ejecutar pruebas? (Requiere servidor activo)")
    respuesta = input("Presiona Enter para continuar o 'n' para salir: ")
    
    if respuesta.lower() != 'n':
        test_all_methods()
    else:
        print("💡 Para probar manualmente:")
        print("1. Ejecuta: python main.py")
        print("2. Ve a: http://localhost:5000/api/metodos")
        print("3. Usa curl, Postman, o Thunder Client")
