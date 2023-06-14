import os, platform, sys

def create_start_script():
    from queries import startup_script
    try:
        with open('start.sh', 'w') as f:
            f.write(startup_script())
    except Exception as e:
        print(f"Error creating start.sh file: {e}")
        sys.exit(1)

def copy_env_example():
    if os.path.exists('.env.example'):
        try:
            with open('.env.example', 'r') as f:
                env_example_lines = f.readlines()
            with open('.env', 'w') as f:
                f.writelines(env_example_lines)
        except Exception as e:
            print(f"Error copying .env.example to .env file: {e}")
            sys.exit(1)
        print('.env file created from .env.example')
        update_env = input('Would you like to update the values in the new .env file? (y/n): ')
        if update_env.lower().startswith('y'):
            try:
                env_dict = {}
                with open('.env', 'r') as f:
                    for line in f.readlines():
                        line = line.strip()
                        if '=' not in line:
                            continue
                        key, value = line.split('=')
                        env_dict[key] = value
                for key in env_dict:
                    new_value = input(f'{key} ({env_dict[key]}): ')
                    if new_value:
                        env_dict[key] = new_value
                with open('.env', 'w') as f:
                    for key, value in env_dict.items():
                        f.write(f'{key}={value}\n')
            except Exception as e:
                print(f"Error updating .env file.  Please try updating manually.")
                print(f'Error: : {e}')
                sys.exit(1)
        else:
            print('Please edit the .env file manually before continuing.')
            sys.exit(0)
    else:
        print(".env.example not found.  Please reclone the git repo.")
        sys.exit(1)

def env_check():
    if not os.path.exists('.env'):
        print(".env not found.")
        create_env = input("Would you like to create a .env file? (y/n): ")
        if create_env.lower().startswith('y'):
            try: 
                copy_env_example()
            except Exception as e:
                print(f"Error creating .env file: {e}")
                sys.exit(1)
            return True
        else:
            print("Please create a .env file before continuing.")
            sys.exit(0)
    else:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_lines = f.readlines()
                if len(env_lines) > 0 or any("=" in line for line in env_lines):
                    return True
                else:
                    delete_create_new = input('.env file exists but is invalid. Do you want to delete it and create a new one? (y/n): ')
                    if delete_create_new.lower().startswith('y'):
                        os.remove('.env')
                        copy_env_example()
                        return True
                    else:
                        raise SystemExit('Invalid .env file exists. Please delete it and try again.')
        return True
    
def init_checks():
    listen_port = os.getenv('LISTEN_PORT')
    if listen_port and int(listen_port) < 1024 and not os.geteuid() == 0:
        sys.exit("Script must be run as root (sudo) due to your Listening Port being below 1024.")
    if platform.system() != 'Darwin':
        sys.exit("This script can only be run on macOS (Darwin).")
    if env_check():
        db_path = os.getenv('DB_PATH')
        if db_path and not os.path.exists(db_path):
            sys.exit("CHAT_DB_PATH is not accessible. Please go to Settings > Privacy > Full Disk Access and add Terminal to it. Then re-run this script with sudo.")
    else:
        sys.exit("Error loading .env file.")
    return True

def ssl_check():

    return False

    # TO DO: fix the below code to work with SSL

    if 'USE_SSL' in os.environ and os.environ['USE_SSL'].lower() == 'true':
        if 'SSL_CERT_PATH' in os.environ and 'SSL_PRIV_KEY_PATH' in os.environ:
            ssl_cert_path = os.path.join(os.getcwd(), os.environ['SSL_CERT_PATH'])
            ssl_priv_path = os.path.join(os.getcwd(), os.environ['SSL_PRIV_KEY_PATH'])
            if os.path.exists(ssl_cert_path) and os.path.exists(ssl_priv_path):
                print("SSL certificate and private key verified. Running with SSL.")
                return True
            else:
                print("Invalid paths to SSL certificate or private key. Running without SSL.")
                return False
        else:
            print("SSL_CERT_PATH or SSL_PRIV_KEY_PATH in .env not provided. Running without SSL.")
            return False
    else:
        print("USE_SSL in .env not set to true. Running without SSL.")
        return False

def start_sh_check():
    if not os.path.exists('start.sh'):
        print("start.sh not found.")
        create_start_sh = input("Would you like to create a 'start.sh' file? (y/n): ")
        if create_start_sh.lower().startswith('y'):
            try:
                create_start_script()
                print('Be sure to execute chmod +x start.sh to make the script executable.')
                print('Then run sudo ./start.sh to start the server.')
                return True
            except Exception as e:
                print(f"Error creating start.sh: {e}")
                sys.exit(1)
        return False
    else:
        return False
    