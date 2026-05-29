import asyncio
import aiohttp
import random
import sys

API_URL = "http://localhost:3000/inventario"

async def send_inventario(session, semaphore, prod_id, suc_id, progress_state):
    async with semaphore:
        cantidad = random.randint(0, 350) # Stock aleatorio
        
        payload = {
            "cantidad": cantidad,
            "producto_id": prod_id,
            "sucursal_id": suc_id,
            "estado": "activo"
        }
        
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status_code in [200, 201]:
                    progress_state["success"] += 1
                else:
                    progress_state["errors"] += 1
        except Exception as e:
            progress_state["errors"] += 1
            
        progress_state["total_done"] += 1
        if progress_state["total_done"] % 10000 == 0:
            sys.stdout.write(f"\rProgreso: {progress_state['total_done']}/500000 stocks procesados. Exitosos: {progress_state['success']}")
            sys.stdout.flush()

async def main():
    print("Iniciando la siembra asíncrona de 500,000 registros de Inventario (25,000 productos x 20 sucursales)...")
    
    # 500 conexiones concurrentes
    semaphore = asyncio.Semaphore(500)
    
    connector = aiohttp.TCPConnector(limit=500, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=1800)
    
    progress_state = {"total_done": 0, "success": 0, "errors": 0}
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        # Mapeamos matemáticamente cada producto (1 a 25,000) a cada sucursal (1 a 20)
        # Esto genera exactamente 25,000 * 20 = 500,000 combinaciones
        for prod_id in range(1, 25001):
            for suc_id in range(1, 21):
                tasks.append(send_inventario(session, semaphore, prod_id, suc_id, progress_state))
                
        print("Registrando 500,000 tareas de inventario... Esto tomará unos segundos...")
        await asyncio.gather(*tasks)
        
        print(f"\nSiembra de Inventario finalizada.")
        print(f"Total procesados: {progress_state['total_done']}")
        print(f"Exitosos: {progress_state['success']}")
        print(f"Errores/Fallidos: {progress_state['errors']}")

if __name__ == "__main__":
    asyncio.run(main())
