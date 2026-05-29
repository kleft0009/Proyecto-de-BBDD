import requests

API_URL = "http://localhost:3000/catalogo"

catalogos = [
    # Roles
    {"nombre": "Cliente", "descripcion": "Usuario que realiza compras", "estado": "activo"},
    {"nombre": "Empleado", "descripcion": "Personal administrativo y de ventas", "estado": "activo"},
    # Categorías de productos
    {"nombre": "Alimentos", "descripcion": "Productos comestibles y de primera necesidad", "estado": "activo"},
    {"nombre": "Bebidas", "descripcion": "Bebidas alcohólicas y no alcohólicas", "estado": "activo"},
    {"nombre": "Limpieza", "descripcion": "Artículos de limpieza para el hogar", "estado": "activo"},
    {"nombre": "Tecnología", "descripcion": "Dispositivos electrónicos y accesorios", "estado": "activo"},
    {"nombre": "Ropa y Calzado", "descripcion": "Prendas de vestir para caballero, dama y niños", "estado": "activo"},
    {"nombre": "Hogar", "descripcion": "Muebles, decoración y utensilios domésticos", "estado": "activo"},
    {"nombre": "Salud y Belleza", "descripcion": "Medicamentos de venta libre y cosméticos", "estado": "activo"},
    {"nombre": "Ferretería", "descripcion": "Herramientas y materiales de construcción", "estado": "activo"},
    {"nombre": "Juguetería", "descripcion": "Juegos y juguetes infantiles", "estado": "activo"},
    {"nombre": "Automotriz", "descripcion": "Repuestos y accesorios para vehículos", "estado": "activo"},
    {"nombre": "Mascotas", "descripcion": "Alimentos y accesorios para animales domésticos", "estado": "activo"},
    {"nombre": "Librería", "descripcion": "Útiles escolares y libros", "estado": "activo"},
    {"nombre": "Deportes", "descripcion": "Artículos e implementos deportivos", "estado": "activo"},
]

def seed_catalogos():
    print("Iniciando la siembra de Catálogos (Categorías y Roles)...")
    success_count = 0
    for cat in catalogos:
        try:
            response = requests.post(API_URL, json=cat)
            if response.status_code in [200, 201]:
                print(f"Creado: {cat['nombre']}")
                success_count += 1
            else:
                print(f"Error al crear {cat['nombre']}: {response.text}")
        except Exception as e:
            print(f"Excepción al conectar con la API: {e}")
    print(f"Siembra finalizada. Creados exitosamente: {success_count}/{len(catalogos)}")

if __name__ == "__main__":
    seed_catalogos()
