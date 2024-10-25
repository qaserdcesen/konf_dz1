import os
import tarfile
import json
import yaml
import datetime
import subprocess

# Функция для загрузки конфигурационного файла
def load_config():
    print("Trying to load config.yaml...")

    if not os.path.isfile('config.yaml'):
        print("Config file does not exist.")
        exit(1)

    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            print(f"Loaded config: {config}")  # Печать загруженной конфигурации
            
            if config is None:
                print("Config is None. Please check the content of config.yaml.")
                exit(1)

            if not isinstance(config, dict):
                print("Loaded config is not a dictionary.")
                exit(1)

            return config
    except FileNotFoundError:
        print("Config file not found. Please make sure config.yaml exists.")
        exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}")
        exit(1)

# Функция для записи логов
def log_action(action):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {"timestamp": timestamp, "action": action}

    # Сохранение логов в формате JSON
    if os.path.exists('log.json'):
        with open('log.json', 'r') as logfile:
            log_data = json.load(logfile)
    else:
        log_data = []

    log_data.append(log_entry)

    with open('log.json', 'w') as logfile:
        json.dump(log_data, logfile, indent=4)

# Функция для работы с tar-архивом
def extract_tar(tar_path):
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall()
        log_action(f'Extracted {tar_path}')

# Команды
def ls():
    entries = os.listdir()
    print(" ".join(entries))
    log_action('Executed ls command')

def cd(directory):
    os.chdir(directory)
    log_action(f'Changed directory to {directory}')

def exit_shell():
    log_action('Exited shell')
    print("Exiting...")
    exit()

def chown(user, file):
    # Простой пример, без проверки прав пользователя
    print(f"Changed owner of {file} to {user}")
    log_action(f'Changed owner of {file} to {user}')

def date_command():
    current_date = datetime.datetime.now()
    print(current_date.strftime("%Y-%m-%d %H:%M:%S"))
    log_action('Executed date command')

def uptime_command():
    # Для Windows можно использовать systeminfo, для UNIX uptime
    if os.name == 'nt':
        process = subprocess.Popen(['systeminfo'], stdout=subprocess.PIPE, text=True)
        output = process.communicate()[0]
        print(output)
    else:
        process = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, text=True)
        output = process.communicate()[0]
        print(output)

    log_action('Executed uptime command')

# Основная функция
def main():
    config = load_config()
    
    if config is None:
        print("Failed to load configuration.")  # Отладочная печать
        exit(1)

    tar_path = config.get('virtual_filesystem_path')
    log_path = config.get('log_file_path')

    if not tar_path or not log_path:
        print("Missing configuration values. Please check config.yaml.")
        exit(1)

    print(f"Tar path: {tar_path}, Log path: {log_path}")  # Отладочная печать

    extract_tar(tar_path)

    while True:
        command = input(f"{os.getcwd()} $ ").strip().split()

        if not command:
            continue

        cmd = command[0]
        args = command[1:]

        if cmd == 'ls':
            ls()
        elif cmd == 'cd':
            if args:
                cd(args[0])
            else:
                print("cd: missing argument")
        elif cmd == 'exit':
            exit_shell()
        elif cmd == 'chown':
            if len(args) == 2:
                chown(args[0], args[1])
            else:
                print("chown: invalid arguments")
        elif cmd == 'date':
            date_command()
        elif cmd == 'uptime':
            uptime_command()
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
