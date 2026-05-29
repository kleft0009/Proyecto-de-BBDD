import asyncio
import aiohttp
import random
import sys
from faker import Faker

fake = Faker('es_ES')

PEDIDOS_URL = "http://localhost:3000/pedidos"
DETALLES_URL = "http://localhost:3000/pedido-detalle"

async def send_order_and_detail(session, semaphore, index, progress_state):
    async with semaphore:
        # Generar un cliente aleatorio entre los 500,000 registrados
        cliente_id = random.randint(1, 500000)
        # Generar un empleado aleatorio entre los 500,000 registrados
        empleado_id = random.randint(1, 500000)
        
        forma_pago = random.choice(["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia Bancaria"])
        
        # Simular precio y cantidad para calcular el total
        precio_unitario = round(random.uniform(0.75, 180.00), 2)
        cantidad = random.randint(1, 5)
        total = round(precio_unitario * cantidad, 2)
        
        order_payload = {
            "fecha": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
            "total": total,
            "formaPago": forma_pago,
            "clienteId": cliente_id,
            "empleadoId": empleado_id,
            "estado": "activo"
        }
        
        try:
            # 1. Crear Pedido
            async with session.post(PEDIDOS_URL, json=order_payload) as order_response:
                if order_response.status in [200, 201]:
                    order_data = await order_response.json()
                    pedido_id = order_data["id"]
                    ret_cliente_id = order_data["clienteId"]
                    
                    # 2. Crear PedidoDetalle inmediatamente con los IDs correctos (clave compuesta)
                    detail_payload = {
                        "clienteId": ret_cliente_id,
                        "pedidoId": pedido_id,
                        "productoId": random.randint(1, 25000), # Producto entre 1 y 25,000
                        "cantidad": cantidad,
                        "precioUnitario": precio_unitario,
                        "estado": "activo"
                    }
                    
                    async with session.post(DETALLES_URL, json=detail_payload) as detail_response:
                        if detail_response.status in [200, 201]:
                            progress_state["success"] += 1
                        else:
                            progress_state["errors"] += 1
                else:
                    progress_state["errors"] += 1
        except Exception as e:
            progress_state["errors"] += 1
            
        progress_state["total_done"] += 1
        if progress_state["total_done"] % 10000 == 0:
            sys.stdout.write(f"\rProgreso: {progress_state['total_done']}/500000 pedidos y detalles procesados. Exitosos: {progress_state['success']}")
            sys.stdout.flush()

async def main():
    print("Iniciando la siembra asíncrona de 500,000 Pedidos y 500,000 Detalles de Pedido...")
    
    # 500 conexiones concurrentes
    semaphore = asyncio.Semaphore(500)
    
    connector = aiohttp.TCPConnector(limit=500, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=3600) # Timeout extendido para el mayor proceso
    
    progress_state = {"total_done": 0, "success": 0, "errors": 0}
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for idx in range(1, 500001):
            tasks.append(send_order_and_detail(session, semaphore, idx, progress_state))
            
        print("Registrando 500,000 tareas asíncronas dobles (1M de inserciones totales)...")
        await asyncio.gather(*tasks)
        
        print(f"\nSiembra de Pedidos y Detalles finalizada.")
        print(f"Total procesados: {progress_state['total_done']}")
        print(f"Exitosos (ambos creados): {progress_state['success']}")
        print(f"Errores/Fallidos: {progress_state['errors']}")

if __name__ == "__main__":
    asyncio.run(main())
