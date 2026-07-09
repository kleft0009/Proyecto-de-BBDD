CREATE EXTENSION IF NOT EXISTS citus;


SELECT * FROM citus_add_node('worker1', 5432);
SELECT * FROM citus_add_node('worker2', 5432);
SELECT * FROM citus_add_node('worker3', 5432);
SELECT * FROM citus_add_node('worker4', 5432);


CREATE TABLE Catalogo(
    id SERIAL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_catalogo_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE Persona (
    id SERIAL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    direccion TEXT,
    ciudad VARCHAR(50),
    id_rol INT NOT NULL,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_persona_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_rol) REFERENCES Catalogo(id) ON DELETE RESTRICT
);

CREATE TABLE Proveedor (
    id SERIAL,
    razon_social VARCHAR(150) NOT NULL,
    ruc VARCHAR(20) NOT NULL UNIQUE,
    direccion TEXT,
    id_ciudad INT NOT NULL,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_proveedor_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ciudad) REFERENCES Catalogo(id) ON DELETE RESTRICT
);

CREATE TABLE Producto (
    id SERIAL,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    id_categoria INT NOT NULL,
    proveedor_id INT,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_producto_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_categoria) REFERENCES Catalogo(id)  ON DELETE RESTRICT,
    FOREIGN KEY (proveedor_id) REFERENCES Proveedor(id) ON DELETE RESTRICT
);

CREATE TABLE Sucursal (
    id SERIAL,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT,
    id_ciudad INT NOT NULL,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_sucursal_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_ciudad) REFERENCES Catalogo(id) ON DELETE RESTRICT
);

CREATE TABLE Inventario (
    id SERIAL,
    cantidad INT NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    id_producto INT NOT NULL,
    id_sucursal INT NOT NULL,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_inventario_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_producto) REFERENCES Producto(id) ON DELETE RESTRICT,
    FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id) ON DELETE RESTRICT
);
CREATE TABLE Pedido (
    id SERIAL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(12,2) NOT NULL DEFAULT 0.00 CHECK (total >= 0),
    forma_pago VARCHAR(50),
    cliente_id INT NOT NULL,
    empleado_id INT NOT NULL,
    estado VARCHAR(20) NOT NULL CONSTRAINT estado_pedido_check CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, cliente_id),
    FOREIGN KEY (cliente_id) REFERENCES Persona(id) ON DELETE RESTRICT,
    FOREIGN KEY (empleado_id) REFERENCES Persona(id) ON DELETE RESTRICT
);

CREATE TABLE PedidoDetalle (
    id SERIAL,
    cliente_id INT NOT NULL,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL  CHECK (precio_unitario >= 0),
    estado VARCHAR(20) NOT NULL  CONSTRAINT estado_pedido_detalle_check  CHECK (estado IN ('activo', 'inactivo')),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, cliente_id),
    FOREIGN KEY (pedido_id, cliente_id)  REFERENCES Pedido(id, cliente_id)  ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES Producto(id)  ON DELETE RESTRICT
);


EXPLAIN ANALYZE
SELECT * FROM pedido_detalle 
JOIN pedido ON pedido_detalle.pedido_id = pedido.id AND pedido_detalle.cliente_id = pedido.cliente_id;
