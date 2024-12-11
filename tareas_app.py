import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Función para conectar a la base de datos
def conectar_bd():
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='organizador_tareas'
    )
    return conexion

# Función para agregar una tarea
def agregar_tarea():
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()
    
    if not titulo:
        messagebox.showerror("Error", "El título es obligatorio")
        return
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (%s, %s)", (titulo, descripcion))
    conexion.commit()
    conexion.close()
    
    messagebox.showinfo("Éxito", "Tarea agregada exitosamente")
    actualizar_lista_tareas()

# Función para editar una tarea
def editar_tarea(id_tarea):
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()
    
    if not titulo:
        messagebox.showerror("Error", "El título es obligatorio")
        return
    
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("UPDATE tareas SET titulo = %s, descripcion = %s WHERE id = %s", (titulo, descripcion, id_tarea))
    conexion.commit()
    conexion.close()
    
    messagebox.showinfo("Éxito", "Tarea editada exitosamente")
    actualizar_lista_tareas()
    # Restablecer el botón de agregar tarea
    btn_agregar.config(text="Agregar Tarea", command=agregar_tarea)

# Función para seleccionar una tarea y cargar los datos en los campos de entrada
def seleccionar_tarea():
    seleccion = listbox_tareas.curselection()
    if seleccion:
        id_tarea = listbox_tareas.get(seleccion[0]).split(" - ")[0]
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id = %s", (id_tarea,))
        tarea = cursor.fetchone()
        conexion.close()
        
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, tarea[1])
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, tarea[2])
        
        # Cambiar el botón de agregar a editar
        btn_agregar.config(text="Editar Tarea", command=lambda: editar_tarea(tarea[0]))

# Función para actualizar la lista de tareas
def actualizar_lista_tareas():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    conexion.close()
    
    listbox_tareas.delete(0, tk.END)
    for tarea in tareas:
        listbox_tareas.insert(tk.END, f"{tarea[0]} - {tarea[1]} - {tarea[2]} - {tarea[3]}")  # ID - Título - Descripción - Estado

# Función para cambiar el estado de una tarea
def cambiar_estado():
    seleccion = listbox_tareas.curselection()
    if seleccion:
        id_tarea = listbox_tareas.get(seleccion[0]).split(" - ")[0]
        
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT estado FROM tareas WHERE id = %s", (id_tarea,))
        estado_actual = cursor.fetchone()[0]
        nuevo_estado = 'completada' if estado_actual == 'pendiente' else 'pendiente'
        
        cursor.execute("UPDATE tareas SET estado = %s WHERE id = %s", (nuevo_estado, id_tarea))
        conexion.commit()
        conexion.close()
        
        messagebox.showinfo("Éxito", f"Estado de la tarea cambiado a {nuevo_estado}")
        actualizar_lista_tareas()

# Función para eliminar una tarea
def eliminar_tarea():
    seleccion = listbox_tareas.curselection()
    if seleccion:
        id_tarea = listbox_tareas.get(seleccion[0]).split(" - ")[0]
        
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta tarea?")
        if respuesta:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM tareas WHERE id = %s", (id_tarea,))
            conexion.commit()
            conexion.close()
            
            messagebox.showinfo("Éxito", "Tarea eliminada")
            actualizar_lista_tareas()

# Crear la ventana principal
root = tk.Tk()
root.title("Organizador de Tareas")

# Campos de entrada
label_titulo = tk.Label(root, text="Título:")
label_titulo.pack()
entry_titulo = tk.Entry(root)
entry_titulo.pack()

label_descripcion = tk.Label(root, text="Descripción:")
label_descripcion.pack()
entry_descripcion = tk.Entry(root)
entry_descripcion.pack()

# Botón de agregar tarea
btn_agregar = tk.Button(root, text="Agregar Tarea", command=agregar_tarea)
btn_agregar.pack()

# Lista de tareas
listbox_tareas = tk.Listbox(root, selectmode=tk.SINGLE, width=50, height=10)
listbox_tareas.pack()

# Botones de editar, cambiar estado y eliminar
btn_editar = tk.Button(root, text="Editar Tarea", command=seleccionar_tarea)
btn_editar.pack()

btn_estado = tk.Button(root, text="Cambiar Estado", command=cambiar_estado)
btn_estado.pack()

btn_eliminar = tk.Button(root, text="Eliminar Tarea", command=eliminar_tarea)
btn_eliminar.pack()

# Actualizar tareas al iniciar
actualizar_lista_tareas()

root.mainloop()
