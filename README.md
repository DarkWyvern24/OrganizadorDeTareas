# Organizador de Tareas

Aplicación de escritorio para gestionar tareas utilizando una interfaz gráfica desarrollada con Tkinter y una base de datos MySQL para almacenar los datos de forma persistente.

## 🚀 Características

- **Agregar Tareas:** Permite ingresar un título y una descripción para registrar una nueva tarea.
- **Editar Tareas:** Selecciona una tarea existente y actualiza su información.
- **Eliminar Tareas:** Elimina tareas de forma permanente, con confirmación previa.
- **Cambiar Estado:** Cambia el estado de una tarea entre "pendiente" y "completada".
- **Persistencia:** Todas las operaciones CRUD están conectadas a una base de datos MySQL.

## 📋 Requisitos

Antes de ejecutar la aplicación, asegúrate de tener lo siguiente:

- **Python 3.x**: Instalado en tu sistema.
- **Tkinter**: Incluido por defecto en Python.
- **MySQL Server**: Instalado y configurado.
- **MySQL Connector para Python**: Instalarlo usando:
  ```bash
  pip install mysql-connector-python
