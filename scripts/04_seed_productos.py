import asyncio
import aiohttp
import random
from faker import Faker

fake = Faker('es_ES')

API_URL = "http://localhost:3000/productos"

# Productos típicos de Ecuador por categoría (Catálogos 3 al 15)
productos_por_categoria = {
    3: ["Arroz Flor Especial", "Atún Real en Aceite", "Galletas Amor", "Fideos Snob", "Chifles de Sal", "Salsa de Tomate Los Andes", "Mermelada Gustadina", "Aceite La Favorita", "Harina Ya", "Avena Polaca"], # Alimentos
    4: ["Agua Güitig con Gas", "Cerveza Pilsener 600ml", "Cerveza Club Premium", "Fioravanti Fresa 2L", "Jugo Del Valle", "Gaseosa Manzana", "Té Hornimans"], # Bebidas
    5: ["Detergente Deja Multiuso", "Jabón Macho Azul", "Desinfectante Poett", "Cloro Eléctrico", "Lavatodo Limón", "Esponja Scotch-Brite"], # Limpieza
    6: ["Cargador USB-C Rápido", "Audífonos MaxSound", "Mouse Óptico Gamer", "Teclado Mecánico", "Memoria USB 64GB", "Cable HDMI 4K"], # Tecnología
    7: ["Camiseta Deportiva La Tri", "Pantalón Jean Clásico", "Medias Deportivas", "Zapatos Casuales", "Gorra Tricolor", "Chompa Térmica"], # Ropa
    8: ["Sartén Antiadherente", "Juego de Vasos Plásticos", "Cuchillo de Cocina", "Toalla de Baño", "Sábana de Algodón", "Almohada Ortopédica"], # Hogar
    9: ["Shampoo Sedal 340ml", "Crema Dental Colgate", "Jabón Palmolive", "Desodorante Rexona", "Protector Solar Umbrela", "Alcohol Antiséptico"], # Salud/Belleza
    10: ["Martillo de Acero 16oz", "Destornillador Phillips", "Cinta Métrica 5m", "Pernos de Anclaje 1/2", "Playo de Presión", "Caja de Herramientas"], # Ferretería
    11: ["Pelota de Fútbol Golty", "Muñeca de Trapo Linda", "Carro de Juguete a Fricción", "Rompecabezas 1000 pzs", "Lego Construcción"], # Juguetería
    12: ["Aceite de Motor Castrol 20W50", "Plumas Limpiaparabrisas", "Líquido de Frenos Bosch", "Llanta Radial R14", "Refrigerante Auto"], # Automotriz
    13: ["Comida para Perro Mimados 2kg", "Comida para Gato CatChow", "Shampoo para Perros", "Collar Ajustable", "Juguete Hueso Goma"], # Mascotas
    14: ["Cuaderno Universitario Estilo", "Caja de Lápices de Colores", "Esfero Bic Azul", "Carpeta Plástica A4", "Mochila Escolar Porta"], # Librería
    15: ["Balón de Baloncesto Spalding", "Raqueta de Tenis Pro", "Cuerda para Saltar", "Mancuernas de Neopreno 5kg", "Gafas de Natación Speedo"] # Deportes
}

async def send_product(session, semaphore, index):
    async with semaphore:
        # Seleccionar categoría aleatoria de 3 a 15
        cat_id = random.randint(3, 15)
        nombre_base = random.choice(productos_por_categoria[cat_id])
        # Asegurar unicidad combinando con palabra y un código numérico
        nombre = f"{nombre_base} {fake.word().capitalize()} #{index}"
        
        precio = round(random.uniform(0.50, 120.00), 2)
        proveedor_id = random.randint(1, 100) # Proveedores del 1 al 100
        
        payload = {
            "nombre": nombre,
            "precio": precio,
            "proveedorId": proveedor_id,
            "catalogo": cat_id,
            "estado": "activo"
        }
        
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status_code in [200, 201]:
                    return True
                else:
                    text = await response.text()
                    print(f"Error {response.status_code} al crear {nombre}: {text}")
                    return False
        except Exception as e:
            # Silenciar excepciones individuales de red para no llenar la consola
            return False

async def main():
    print("Iniciando la siembra asíncrona de 25,000 Productos...")
    
    # 500 conexiones concurrentes para velocidad máxima sin tumbar NestJS
    semaphore = asyncio.Semaphore(500)
    
    # Configurar timeout y límites de conexión para el cliente aiohttp
    connector = aiohttp.TCPConnector(limit=500, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=300)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for idx in range(1, 25001):
            tasks.append(send_product(session, semaphore, idx))
            
        print("Registrando tareas asíncronas... Espera por favor...")
        results = await asyncio.gather(*tasks)
        
        success = sum(1 for r in results if r)
        print(f"Siembra de Productos finalizada. Creados exitosamente: {success}/25000")

if __name__ == "__main__":
    asyncio.run(main())
