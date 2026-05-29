import requests
import random
from faker import Faker

fake = Faker('es_ES')

API_URL = "http://localhost:3000/proveedores"

ciudades_ecuador = [
    "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala", 
    "Durán", "Manta", "Portoviejo", "Loja", "Ambato", "Esmeraldas",
    "Quevedo", "Riobamba", "Milagro", "Ibarra", "La Libertad", "Tena"
]

sectores = ["Alimentos", "Importaciones", "Distribuidora", "Consorcio", "Grupo", "Tecnología", "Textiles"]
sufijos = ["S.A.", "C.A.", "S.A.S.", "Ltda.", "Comercializadora"]

def generar_cedula_ecuatoriana():
    # Genera una cédula ecuatoriana válida usando el módulo 10
    provincia = random.randint(1, 24)
    provincia_str = f"{provincia:02d}"
    tercer_digito = random.randint(0, 5)
    digitos = [int(provincia_str[0]), int(provincia_str[1]), tercer_digito]
    for _ in range(6):
        digitos.append(random.randint(0, 9))
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for idx, d in enumerate(digitos):
        valor = d * coeficientes[idx]
        if valor >= 10:
            valor -= 9
        suma += valor
        
    verificador = (10 - (suma % 10)) % 10
    digitos.append(verificador)
    return "".join(map(str, digitos))

def generar_ruc_ecuatoriano():
    return generar_cedula_ecuatoriana() + "001"

def seed_proveedores():
    print("Iniciando la siembra de Proveedores...")
    success_count = 0
    for i in range(100):
        razon_social = f"{random.choice(sectores)} {fake.last_name()} {random.choice(sufijos)}"
        ruc = generar_ruc_ecuatoriano()
        direccion = f"Av. {fake.street_name()} y Calle {fake.street_name()}"
        ciudad = random.choice(ciudades_ecuador)
        
        payload = {
            "razonSocial": razon_social,
            "ruc": ruc,
            "direccion": direccion,
            "ciudad": ciudad,
            "estado": "activo"
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code in [200, 201]:
                success_count += 1
            else:
                print(f"Error al crear proveedor {razon_social}: {response.text}")
        except Exception as e:
            print(f"Excepción al conectar con la API: {e}")
            break
            
    print(f"Siembra de Proveedores finalizada. Creados: {success_count}/100")

if __name__ == "__main__":
    seed_proveedores()
