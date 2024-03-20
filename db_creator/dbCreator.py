import mysql.connector
from faker import Faker
import random
from dbconfig import DB_CONFIG

# Lista de modelos de productos tecnológicos
modelos = [
    "iPhone 13 Pro Max",
    "Samsung Galaxy S21 Ultra",
    "Google Pixel 6 Pro",
    "OnePlus 9 Pro",
    "Xiaomi Mi 11 Ultra",
    "Sony WH-1000XM4",
    "Bose QuietComfort 45",
    "Sennheiser Momentum 3",
    "Apple MacBook Pro 16",
    "Dell XPS 15",
    "Microsoft Surface Laptop 4",
    "Lenovo ThinkPad X1 Carbon"
]

# Crear una instancia de Faker para generar datos ficticios
faker = Faker()

# Establecer la conexión a la base de datos
connection = mysql.connector.connect(**DB_CONFIG)

# Crear un cursor para ejecutar comandos SQL
cursor = connection.cursor()

# Crear las tablas en el orden correcto

# TABLA CATEGORÍA
cursor.execute("CREATE TABLE IF NOT EXISTS Categoria ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "NombreCategoria VARCHAR(255))"
               )

# Insertar datos en la tabla CATEGORÍA
categorias = ['computacion', 'celulares y teléfonos', 'consolas y videojuegos', 'electrónica, audio y video']
for categoria in categorias:
    cursor.execute("INSERT INTO Categoria (NombreCategoria) VALUES (%s)", (categoria,))

# TABLA SUCURSAL
cursor.execute("CREATE TABLE IF NOT EXISTS Sucursal ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "Nombre VARCHAR(255),"
               "Ubicacion VARCHAR(255))"
               )

# Insertar datos en la tabla SUCURSAL
sucursales = [('Luján', 'Luján'), ('Chivilcoy', 'Chivilcoy'), ('Mercedes', 'Mercedes')]
for sucursal in sucursales:
    cursor.execute("INSERT INTO Sucursal (Nombre, Ubicacion) VALUES (%s, %s)", sucursal)

# TABLA PRODUCTO
cursor.execute("CREATE TABLE IF NOT EXISTS Producto ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "Nombre VARCHAR(255),"
               "Descripcion VARCHAR(255),"
               "Stock INT,"
               "Precio_Compra DOUBLE,"
               "Precio_Venta DOUBLE,"
               "ID_Categoria INT,"
               "ID_Sucursal INT,"
               "FOREIGN KEY (ID_Categoria) REFERENCES Categoria(ID),"
               "FOREIGN KEY (ID_Sucursal) REFERENCES Sucursal(ID))"
               )

# Insertar datos ficticios en la tabla PRODUCTO
for _ in range(20):
    nombre_producto = random.choice(modelos)
    descripcion_producto = "Descripción de {}".format(nombre_producto)
    stock_producto = random.randint(1, 100)
    precio_compra = round(random.uniform(10, 1000), 2)
    precio_venta = round(precio_compra * random.uniform(1.1, 2), 2)
    id_categoria = random.randint(1, len(categorias))
    id_sucursal = random.randint(1, len(sucursales))
    cursor.execute("INSERT INTO Producto (Nombre, Descripcion, Stock, Precio_Compra, Precio_Venta, ID_Categoria, ID_Sucursal) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (nombre_producto, descripcion_producto, stock_producto, precio_compra, precio_venta, id_categoria, id_sucursal))

# TABLA PROMOCIÓN
cursor.execute("CREATE TABLE IF NOT EXISTS Promocion ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "ID_Producto INT,"
               "Fecha_inicio DATETIME,"
               "Fecha_fin DATETIME,"
               "Porcentaje DOUBLE DEFAULT 0.0,"
               "FOREIGN KEY (ID_Producto) REFERENCES Producto(ID))"
               )

# Insertar datos ficticios en la tabla PROMOCIÓN
for _ in range(10):
    id_producto = random.randint(1, 20)
    fecha_inicio = faker.date_time_this_year()
    fecha_fin = faker.date_time_between(start_date=fecha_inicio)
    porcentaje = round(random.uniform(0, 50), 2)
    cursor.execute("INSERT INTO Promocion (ID_Producto, Fecha_inicio, Fecha_fin, Porcentaje) VALUES (%s, %s, %s, %s)",
                   (id_producto, fecha_inicio, fecha_fin, porcentaje))
    
# TABLA VENTA
cursor.execute("CREATE TABLE IF NOT EXISTS Venta ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "ID_Sucursal INT,"
               "Fecha_Hora DATETIME,"
               "ID_Detalle INT,"
               "Total DOUBLE,"
               "FOREIGN KEY (ID_Sucursal) REFERENCES Sucursal(ID))"
               )

# Insertar datos ficticios en la tabla VENTA
for _ in range(1000):  # Generamos 50 ventas ficticias
    id_sucursal = random.randint(1, len(sucursales))
    fecha_hora = faker.date_time_this_year()
    id_detalle = random.randint(1, 100)  # Asumiendo que hay 100 registros en Detalle
    total = round(random.uniform(100, 10000), 2)  # Total aleatorio entre 100 y 10000
    cursor.execute("INSERT INTO Venta (ID_Sucursal, Fecha_Hora, ID_Detalle, Total) VALUES (%s, %s, %s, %s)",
                   (id_sucursal, fecha_hora, id_detalle, total))
    
# TABLA DETALLE
cursor.execute("CREATE TABLE IF NOT EXISTS Detalle ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "ID_Venta INT,"
               "ID_Producto INT,"
               "ID_Promocion INT,"
               "Cantidad INT,"
               "Subtotal DOUBLE,"
               "FOREIGN KEY (ID_Venta) REFERENCES Venta(ID),"
               "FOREIGN KEY (ID_Producto) REFERENCES Producto(ID),"
               "FOREIGN KEY (ID_Promocion) REFERENCES Promocion(ID))"
               )

# Insertar datos ficticios en la tabla DETALLE
for _ in range(100):
    id_venta = random.randint(1, 50)  # Asumiendo que habrá un máximo de 50 ventas
    id_producto = random.randint(1, 20)  # Asumiendo que hay 20 productos
    id_promocion = random.randint(1, 10)  # Asumiendo que hay 10 promociones
    cantidad = random.randint(1, 5)
    subtotal = round(random.uniform(10, 1000), 2)
    cursor.execute("INSERT INTO Detalle (ID_Venta, ID_Producto, ID_Promocion, Cantidad, Subtotal) VALUES (%s, %s, %s, %s, %s)",
                   (id_venta, id_producto, id_promocion, cantidad, subtotal))


# Confirmar los cambios y cerrar el cursor y la conexión
connection.commit()
cursor.close()
connection.close()