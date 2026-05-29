import requests
import random
from faker import Faker

fake = Faker('es_ES')

API_URL = "http://localhost:3000/sucursal"

ciudades_ecuador = [
    "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala", 
    "Durán", "Manta", "Portoviejo", "Loja", "Ambato", "Esmeraldas",
    "Quevedo", "Riobamba", "Milagro", "Ibarra", "La Libertad", "Tena",
    "Latacunga", "Tulcán", "Babahoyo"
]

tipos_sucursal = ["Norte", "Sur", "Centro", "Express", "Premium", "Mayorista"]

def seed_sucursales():
    print("Iniciando la siembra de Sucursales...")
    success_count = 0
    # Generaremos 20 sucursales, una para cada una de las 20 ciudades de la lista
    for ciudad in ciudades_ecuador:
        nombre = f"Sucursal {ciudad} {random.choice(tipos_sucursal)}"
        direccion = f"Calle {fake.street_name()} y Av. {fake.street_name()}"
        
        payload = {
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "estado": "activo"
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code in [200, 201]:
                success_count += 1
            else:
                print(f"Error al crear sucursal {nombre}: {response.text}")
        except Exception as e:
            print(f"Excepción al conectar con la API: {e}")
            break
            
    print(f"Siembra de Sucursales finalizada. Creadas: {success_count}/{len(ciudades_ecuador)}")

if __name__ == "__main__":
    seed_sucursales()
