# Database Creator

Pasos:

1) Crea una base de datos utilizando MySQL

2) Dentro de este proyecto crea un archivo dbconfig.py
   El mismo debe tener la siguiente información:

   ```bash
    DB_CONFIG = {
    'host': 'hostname',
    'user': 'username',
    'password': 'your_password',
    'database': 'database_name'
    }
    ```

3) Ejecuta el código con el siguiente comando

   ```bash
    python dbCreator.py
    ```

Una vez finalizado, la base de datos estará cargada con las tablas correspondientes
