USE SGFood; 

DELETE FROM Venta;
DELETE FROM Compra;
DELETE FROM Vendedor;
DELETE FROM Sucursal;
DELETE FROM Proveedor;
DELETE FROM Producto;
DELETE FROM Cliente;

-- Tabla Cliente
CREATE TABLE Cliente (
    Codigo VARCHAR(64) PRIMARY KEY,
    Nombre VARCHAR(128),
    Direccion VARCHAR(1024),
    Numero INT,
    Tipo VARCHAR(16)
);

-- Tabla Producto
CREATE TABLE Producto (
    Codigo VARCHAR(64) PRIMARY KEY,
    Nombre VARCHAR(256),
    Marca VARCHAR(256),
    Categoria VARCHAR(32)
);

-- Tabla Proveedor
CREATE TABLE Proveedor (
    Codigo VARCHAR(64) PRIMARY KEY,
    Nombre VARCHAR(512),
    Direccion VARCHAR(1024),
    Numero INT,
    Web VARCHAR(16)
);

-- Tabla Sucursal
CREATE TABLE Sucursal (
    Codigo VARCHAR(64) PRIMARY KEY,
    Nombre VARCHAR(32),
    Direccion VARCHAR(1024),
    Region VARCHAR(32),
    Departamento VARCHAR(32)
);

-- Tabla Vendedor
CREATE TABLE Vendedor (
    Codigo VARCHAR(64) PRIMARY KEY,
    Nombre VARCHAR(128),
    Vacacionista INT
);

-- Tabla Compra
CREATE TABLE Compra (
    Fecha DATE,
    Unidades INT,
    CostoUnitario FLOAT,
    CodProveedor VARCHAR(64) FOREIGN KEY REFERENCES Proveedor(Codigo),
    CodProducto VARCHAR(64) FOREIGN KEY REFERENCES Producto(Codigo),
    CodSucursal VARCHAR(64) FOREIGN KEY REFERENCES Sucursal(Codigo)
);

-- Tabla Venta
CREATE TABLE Venta (
    Fecha DATE,
    Unidades INT,
    PrecioUnitario FLOAT,
    CodCliente VARCHAR(64) FOREIGN KEY REFERENCES Cliente(Codigo),
    CodVendedor VARCHAR(64) FOREIGN KEY REFERENCES Vendedor(Codigo),
    CodProducto VARCHAR(64) FOREIGN KEY REFERENCES Producto(Codigo),
    CodSucursal VARCHAR(64) FOREIGN KEY REFERENCES Sucursal(Codigo)
);