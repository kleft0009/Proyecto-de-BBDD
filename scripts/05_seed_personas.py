import asyncio
import aiohttp
import random
import sys
from faker import Faker

fake = Faker('es_ES')

API_URL = "http://localhost:3000/persona"

ciudades_ecuador = [
    "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala", 
    "Durán", "Manta", "Portoviejo", "Loja", "Ambato", "Esmeraldas",
    "Quevedo", "Riobamba", "Milagro", "Ibarra", "La Libertad", "Tena",
    "Latacunga", "Tulcán", "Babahoyo"
]

cedulas_generadas = set()

def generar_cedula_ecuatoriana_unica():
    while True:
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
        cedula = "".join(map(str, digitos))
        
        if cedula not in cedulas_generadas:
            cedulas_generadas.add(cedula)
            return cedula

async def send_persona(session, semaphore, index, progress_state):
    async with semaphore:
        # 98% son clientes (ID: 1), 2% son empleados (ID: 2)
        catalogo_id = 2 if random.random() < 0.02 else 1
        
        # Faker de España genera nombres en español perfectos
        nombre = fake.first_name()
        apellido = fake.last_name()
        cedula = generar_cedula_ecuatoriana_unica()
        direccion = f"Calle {fake.street_name()} #{random.randint(10, 999)}"
        ciudad = random.choice(ciudades_ecuador)
        
        payload = {
            "nombre": nombre,
            "apellido": apellido,
            "cedula": cedula,
            "direccion": direccion,
            "ciudad": ciudad,
            "catalogoId": catalogo_id,
            "estado": "activo"
        }
        
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status_code in [200, 201]:
                    progress_state["success"] += 1
                else:
                    text = await response.text()
                    # Solo imprimimos errores ocasionales para no colapsar la consola
                    if progress_state["errors"] < 20:
                        print(f"\nError {response.status_code} en persona: {text}")
                    progress_state["errors"] += 1
        except Exception as e:
            progress_state["errors"] += 1
            
        progress_state["total_done"] += 1
        if progress_state["total_done"] % 10000 == 0:
            sys.stdout.write(f"\rProgreso: {progress_state['total_done']}/500000 procesados. Exitosos: {progress_state['success']}")
            sys.stdout.flush()

async def main():
    print("Iniciando la siembra asíncrona de 500,000 Personas (Clientes y Empleados)...")
    
    # Control de concurrencia: 500 hilos de ejecución paralelos
    semaphore = asyncio.Semaphore(500)
    
    connector = aiohttp.TCPConnector(limit=500, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=1800) # Timeout amplio para gran volumen
    
    progress_state = {"total_done": 0, "success": 0, "errors": 0}
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for idx in range(1, 500001):
            tasks.append(send_persona(session, semaphore, idx, progress_state))
            
        print("Registrando 500,000 tareas... Esto puede tomar unos segundos...")
        await asyncio.gather(*tasks)
        
        print(f"\nSiembra de Personas finalizada.")
        print(f"Total procesados: {progress_state['total_done']}")
        print(f"Exitosos: {progress_state['success']}")
        print(f"Errores/Fallidos: {progress_state['errors']}")

if __name__ == "__main__":
    asyncio.run(main())
