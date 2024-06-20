from flask import Flask, render_template, redirect, url_for
import subprocess
import platform
import logging

app = Flask(__name__)

@app.route('/')
def index():
    username = "usuario"  # Aquí deberías obtener el nombre de usuario de la sesión de Flask
    return render_template('dashboard.html', username=username)

@app.route('/view_logs')
def view_logs():
    username = "usuario"  # Aquí deberías obtener el nombre de usuario de la sesión de Flask
    logging.info(f"User {username} opened the logs viewer.")
    return redirect(url_for('logs'))

@app.route('/open_terminal')
def open_terminal():
    username = "usuario"  # Aquí deberías obtener el nombre de usuario de la sesión de Flask
    logging.info(f"User {username} opened the terminal.")
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(['start', 'cmd'], shell=True)
    elif system == 'Darwin':  # macOS
        subprocess.Popen(['open', '-a', 'Terminal'])
    elif system == 'Linux':
        subprocess.Popen(['x-terminal-emulator'])
    else:
        return "Unsupported OS"
    return redirect(url_for('index'))


