import paramiko
import time
#Aplicación en python
import tkinter as tk
#Estilos en Python
from tkinter import messagebox, scrolledtext


def enviar_comando(client, command):
    try:
        shell = client.invoke_shell()
        shell.send(f"{command}\n")
        time.sleep(2)
        output = ""
        while shell.recv_ready():
            output += shell.recv(1024).decode("utf-8")
        print(output)
        return output
    except Exception as e:
        print(f"Error ejecutando comando: {e}")
        return f"Error ejecutando comando: {e}"


def enviar_comandos(client, command_list):
    try:
        shell = client.invoke_shell()
        output = ""
        for command in command_list:
            shell.send(f"{command}\n")
            time.sleep(2)
            while shell.recv_ready():
                output += shell.recv(1024).decode("utf-8")
            output += "\n"
        print(output)
        return output
    except Exception as e:
        print(f"Error ejecutando comandos: {e}")
        return f"Error ejecutando comandos: {e}"


def conectar_y_ejecutar():
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    global client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("Intentando conectar con el servidor SSH...")
        client.connect(ip, port=22, username=username, password=password, timeout=10)
        print("Conexión establecida.")
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Conexión establecida.\n")
    except paramiko.SSHException as sshException:
        print(f"Error al conectar con el servidor SSH: {sshException}")
        messagebox.showerror("Error", f"Error al conectar con el servidor SSH: {sshException}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def ejecutar_comando():
    command = command_entry.get()
    if not command:
        messagebox.showwarning("Advertencia", "Debe ingresar un comando.")
        return

    output = enviar_comando(client, command)
    output_text.insert(tk.END, f"$ {command}\n{output}\n")


# Configuración de la interfaz gráfica con tkinter
root = tk.Tk()
root.title("SSH Connection")
root.configure(bg="#e0f7fa")

tk.Label(root, text="Dirección IP", bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Usuario", bg="#e0f7fa").grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="Contraseña", bg="#e0f7fa").grid(row=2, column=0, padx=10, pady=10)

ip_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")

ip_entry.grid(row=0, column=1, padx=10, pady=10)
username_entry.grid(row=1, column=1, padx=10, pady=10)
password_entry.grid(row=2, column=1, padx=10, pady=10)

connect_button = tk.Button(root, text="Conectar", command=conectar_y_ejecutar, bg="#00796b", fg="white")
connect_button.grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(root, text="Comando", bg="#e0f7fa").grid(row=4, column=0, padx=10, pady=10)
command_entry = tk.Entry(root)
command_entry.grid(row=4, column=1, padx=10, pady=10)

execute_button = tk.Button(root, text="Ejecutar Comando", command=ejecutar_comando, bg="#00796b", fg="white")
execute_button.grid(row=5, column=0, columnspan=2, pady=10)

output_text = scrolledtext.ScrolledText(root, width=50, height=20, bg="#f1f8e9", fg="#004d40")
output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()