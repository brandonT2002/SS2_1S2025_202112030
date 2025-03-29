SHOW DATABASES;
DROP DATABASE SGFood_temp1;
CREATE DATABASE SGFood_Temp1;
USE SGFood_Temp1;

DROP TABLE temp1;
DROP TABLE temp2;

SELECT * FROM Temp1;
SELECT * FROM Temp2;

-- Tabla Temporal Compra
CREATE TABLE Temp1 (
    -- Compra
    Fecha VARCHAR(64),
    -- Proveedor
    CodProveedor VARCHAR(64), --  1
    NombreProveedor VARCHAR(512), --  2
    DireccionProveedor VARCHAR(1024), --  3
    NumeroProveedor VARCHAR(32), --  4
    WebProveedor VARCHAR(16), --  5
    -- Producto
    CodProducto VARCHAR(64), -- 1
    NombreProducto VARCHAR(256), -- 2
    MarcaProducto VARCHAR(256), -- 3
    Categoria VARCHAR(32), -- 4
    -- Sucursal
    SodSuSursal VARCHAR(64), -- 1
    NombreSucursal VARCHAR(32), -- 2
    DireccionSucursal VARCHAR(1024), -- 3
    Region VARCHAR(32), -- 4
    Departamento VARCHAR(32), -- 5
    -- Compra
    Unidades VARCHAR(16),
    CostoU VARCHAR(16)
);

-- Tabla Temporal Venta
CREATE TABLE Temp2 (
    -- Venta
    Fecha VARCHAR(16),
    -- Cliente
    CodigoCliente VARCHAR(64), -- 1
    NombreCliente VARCHAR(128), -- 2
    TipoCliente VARCHAR(16), -- 3
    DireccionCliente VARCHAR(1024), -- 4
    NumeroCliente VARCHAR(32), -- 5
    -- Vendedor
    CodVendedor VARCHAR(64), -- 1
    NombreVendedor VARCHAR(128), -- 2
    Vacacionista VARCHAR(8), -- 3
    -- Producto
    CodProducto VARCHAR(64), -- 1
    NombreProducto VARCHAR(256), -- 2
    MarcaProducto VARCHAR(256), -- 3
    Categoria VARCHAR(32), -- 4
    -- Sucursal
    SodSuSursal VARCHAR(64), -- 1
    NombreSucursal VARCHAR(32), -- 2
    DireccionSucursal VARCHAR(1024), -- 3
    Region VARCHAR(32), -- 4
    Departamento VARCHAR(32), -- 5
    -- Venta
    Unidades VARCHAR(16),
    PrecioUnitario VARCHAR(16)
);

SHOW TABLES;
SELECT * FROM temp1;
SELECT * FROM temp2;