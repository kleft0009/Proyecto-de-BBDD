
CREATE EXTENSION IF NOT EXISTS citus;

SELECT * FROM citus_add_node('worker1', 5432);
SELECT * FROM citus_add_node('worker2', 5432);
SELECT * FROM citus_add_node('worker3', 5432);
SELECT * FROM citus_add_node('worker4', 5432);

CREATE TABLE Persona (
    id SERIAL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL,
    direccion TEXT,
    ciudad VARCHAR(50),
    rol VARCHAR(20) NOT NULL, -- 'Cliente', 'Empleado', 'Ambos'
    puesto VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE Proveedor (
    id SERIAL,
    razon_social VARCHAR(150) NOT NULL,
    ruc VARCHAR(20) NOT NULL,
    direccion TEXT,
    ciudad VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE Producto (
    id SERIAL,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    categoria VARCHAR(50),
    proveedor_id INT,
    PRIMARY KEY (id)
);

CREATE TABLE Inventario (
    id SERIAL,
    cantidad INT NOT NULL DEFAULT 0,
    producto_id INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Pedido (
    id SERIAL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    forma_pago VARCHAR(50),
    cliente_id INT NOT NULL,
    empleado_id INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE PedidoDetalle (
    id SERIAL,
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(10, 2) NOT NULL,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    PRIMARY KEY (id, pedido_id) -- Clave compuesta vital para que Citus almacene el detalle junto al pedido
);

ALTER TABLE Producto 
ADD CONSTRAINT fk_producto_proveedor 
FOREIGN KEY (proveedor_id) REFERENCES Proveedor(id) ON DELETE SET NULL;

ALTER TABLE Inventario 
ADD CONSTRAINT fk_inventario_producto 
FOREIGN KEY (producto_id) REFERENCES Producto(id) ON DELETE CASCADE;

ALTER TABLE PedidoDetalle 
ADD CONSTRAINT fk_detalle_pedido 
FOREIGN KEY (pedido_id) REFERENCES Pedido(id) ON DELETE CASCADE;

ALTER TABLE PedidoDetalle 
ADD CONSTRAINT fk_detalle_producto 
FOREIGN KEY (producto_id) REFERENCES Producto(id);
