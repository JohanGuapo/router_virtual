from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import logging
import os
import pandas as pd
import time
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#ms prueba
# Crear el archivo de log de actividad
def get_next_log_filename(directory, prefix):
    existing_logs = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith('.log')]
    if not existing_logs:
        return os.path.join(directory, f'{prefix}_1.log')
    existing_logs.sort()
    last_log = existing_logs[-1]
    last_num = int(last_log.split('_')[-1].split('.')[0])
    return os.path.join(directory, f'{prefix}_{last_num + 1}.log')


log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
activity_log_file = get_next_log_filename(log_directory, 'user_activity')

# Agregar encabezados si el archivo es nuevo
if not os.path.exists(activity_log_file):
    with open(activity_log_file, 'w') as f:
        f.write('timestamp,level,message\n')

# Crear el archivo application.log si no existe
application_log_file = 'logs/application.log'
if not os.path.exists(application_log_file):
    df = pd.DataFrame({
        'timestamp': ['2024-06-01 12:00:00', '2024-06-01 12:05:00', '2024-06-01 12:10:00'],
        'level': ['INFO', 'WARN', 'ERROR'],
        'message': ['Application started', 'Low disk space', 'Failed to connect to database']
    })
    df.to_csv(application_log_file, index=False)

# Configuración del logger
logging.basicConfig(
    filename=activity_log_file,
    level=logging.INFO,
    format='%(asctime)s,INFO,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Función para la autenticación del usuario
def authenticate(username, password):
    with open('users/users.json', 'r') as f:
        users = json.load(f)
    return users.get(username) == password


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            logging.info(f'User {username} logged in successfully')
            return redirect(url_for('dashboard'))
        else:
            logging.warning(f'Failed login attempt for user {username}')
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    logging.info(f'User {username} opened the dashboard.')
    return render_template('dashboard.html', username=username)

@app.route('/logs')
def logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    log_level = request.args.get('log_level', 'INFO')

    logging.info(f'User {username} is viewing {log_level} logs')
    try:
        if os.path.exists('logs/application.log'):
            df_app = pd.read_csv('logs/application.log', on_bad_lines='skip')
        else:
            return "Error: 'application.log' file not found."

        activity_log_files = [f for f in os.listdir('logs') if f.startswith('user_activity') and f.endswith('.log')]
        if not activity_log_files:
            return "Error: No user activity log files found."

        df_user_list = []
        for f in activity_log_files:
            df_user_list.append(pd.read_csv(os.path.join('logs', f), on_bad_lines='skip'))
        df_user = pd.concat(df_user_list)

        if 'level' not in df_app.columns or 'level' not in df_user.columns:
            return "Error: 'level' column not found in one of the log files."

        combined_df = pd.concat([df_app, df_user])
        filtered_logs = combined_df[combined_df['level'] == log_level]

        logs = filtered_logs.to_dict(orient='records')
        return render_template('logs.html', logs=logs, log_level=log_level)
    except Exception as e:
        logging.error(f"Error loading logs: {e}")
        return f"Error loading logs: {e}"

@app.route('/open_terminal')
def open_terminal():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    logging.info(f'User {username} opened the terminal.')

    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/K', 'echo Welcome'], shell=True)
        elif os.name == 'posix':  # macOS and Linux
            if subprocess.call(['which', 'gnome-terminal']) == 0:  # Linux with GNOME Terminal
                subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'echo Welcome; exec bash'])
            elif subprocess.call(['which', 'xterm']) == 0:  # Linux with xterm
                subprocess.Popen(['xterm', '-hold', '-e', 'echo Welcome'])
            elif subprocess.call(['which', 'open']) == 0:  # macOS
                subprocess.Popen(['open', '-a', 'Terminal', '.'])
            else:
                raise EnvironmentError("No compatible terminal found.")

        logging.info(f'Terminal opened successfully for user {username}.')
        flash('Terminal opened successfully!')
    except Exception as e:
        logging.error(f"Error opening terminal: {e}")
        flash(f"Error opening terminal: {e}")

    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    print("Starting Flask application")
    app.run(debug=True)
