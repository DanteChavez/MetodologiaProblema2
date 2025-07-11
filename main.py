"""
MAIN - Sistema UVShop
====================
Punto de entrada principal que utiliza la Vista REST simplificada con arquitectura MVC
"""

from vista.vista_rest_simple import crear_vista_rest_simple

if __name__ == "__main__":
    print("🎉 BIENVENIDO A UVSHOP")
    print("🎯 SISTEMA DE COMERCIO ELECTRÓNICO - ARQUITECTURA MVC")
    print("="*80)
    print("🏗️ Iniciando con patrón Model-View-Controller (Simplificado)...")
    print("📡 API disponible en: http://localhost:5000/api")
    print("\n🌐 ARQUITECTURA MVC ESTABLE:")
    print("\n� VISTA (VIEW):")
    print("   • vista_rest_simple.py - API REST endpoints estables")
    print("   • Manejo seguro de HTTP requests/responses")
    print("   • Serialización JSON robusta")
    print("\n🎛️ CONTROLADOR (CONTROLLER):")
    print("   • gestionPedidosUsuarios - Lógica de usuarios (activo)")
    print("   • proxy - Controlador de acceso a datos (activo)")
    print("   • Inicialización segura de controladores opcionales")
    print("\n🗄️ MODELO (MODEL):")
    print("   • bd.py - Base de datos (Singleton activo)")
    print("   • proxy.py - Proxy de acceso a datos (activo)")
    print("   • pedido.py, usuario.py, productos.py - Entidades")
    print("   • inventario.py - Gestión de inventario (activo)")
    print("="*80)
    print("💡 SEPARACIÓN DE RESPONSABILIDADES CORRECTA")
    print("🔥 ¡ARQUITECTURA MVC ESTABLE Y FUNCIONAL!")
    print("="*80)
    
    try:
        # Crear e inicializar la vista REST simplificada
        vista_rest = crear_vista_rest_simple()
        
        # Ejecutar el servidor
        vista_rest.ejecutar(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Error al inicializar el sistema: {e}")
        print("💡 Verifica que todos los módulos estén correctamente instalados")
        print("📋 Usa: pip install flask flask-cors")