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
    Fecha VARCHAR(512),
    -- Proveedor
    CodProveedor VARCHAR(512), --  1
    NombreProveedor VARCHAR(512), --  2
    DireccionProveedor VARCHAR(1024), --  3
    NumeroProveedor VARCHAR(512), --  4
    WebProveedor VARCHAR(512), --  5
    -- Producto
    CodProducto VARCHAR(512), -- 1
    NombreProducto VARCHAR(512), -- 2
    MarcaProducto VARCHAR(512), -- 3
    Categoria VARCHAR(512), -- 4
    -- Sucursal
    SodSuSursal VARCHAR(512), -- 1
    NombreSucursal VARCHAR(512), -- 2
    DireccionSucursal VARCHAR(1024), -- 3
    Region VARCHAR(512), -- 4
    Departamento VARCHAR(512), -- 5
    -- Compra
    Unidades VARCHAR(512),
    CostoU VARCHAR(512)
);

-- Tabla Temporal Venta
CREATE TABLE Temp2 (
    -- Venta
    Fecha VARCHAR(512),
    -- Cliente
    CodigoCliente VARCHAR(512), -- 1
    NombreCliente VARCHAR(512), -- 2
    TipoCliente VARCHAR(512), -- 3
    DireccionCliente VARCHAR(512), -- 4
    NumeroCliente VARCHAR(512), -- 5
    -- Vendedor
    CodVendedor VARCHAR(512), -- 1
    NombreVendedor VARCHAR(512), -- 2
    Vacacionista VARCHAR(512), -- 3
    -- Producto
    CodProducto VARCHAR(512), -- 1
    NombreProducto VARCHAR(512), -- 2
    MarcaProducto VARCHAR(512), -- 3
    Categoria VARCHAR(512), -- 4
    -- Sucursal
    SodSuSursal VARCHAR(512), -- 1
    NombreSucursal VARCHAR(512), -- 2
    DireccionSucursal VARCHAR(1024), -- 3
    Region VARCHAR(512), -- 4
    Departamento VARCHAR(512), -- 5
    -- Venta
    Unidades VARCHAR(512),
    PrecioUnitario VARCHAR(512)
);

SHOW TABLES;
SELECT * FROM temp1;