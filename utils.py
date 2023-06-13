import os, platform, shutil, sys

def create_start_script():
    from queries import startup_script
    try:
        with open('start.sh', 'w') as f:
            f.write(startup_script())
    except Exception as e:
        print(f"Error creating start.sh file: {e}")
        sys.exit(1)

def copy_env_example():
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            try:
                shutil.copy('.env.example', '.env')
            except Exception as e:
                print(f"Error copying .env.example .env file: {e}")
                sys.exit(1)
        else:
            print(".env.example not found.  Please reclone the git repo.")
            sys.exit(1)
        print('.env file created from .env.example')
        update_env = input('Would you like to update the values in the new .env file? (y/n): ')
        if update_env.lower().startswith('y'):
            try:
                with open('.env', 'r') as f:
                    env_lines = f.readlines()
                with open('.env', 'w') as f:
                    for line in env_lines:
                        key, value = line.strip().split('=')
                        new_value = input(f'{key} ({value}): ')
                        if new_value:
                            value = new_value
                        f.write(f'{key}={value}\n')
            except Exception as e:
                print(f"Error updating .env file.  Please try updating manually.")
                print(f'Error: : {e}')
                sys.exit(1)
        else:
            print('Please edit the .env file manually before continuing.')
            sys.exit(0)

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
        return True
    
def init_checks():
    if not os.geteuid() == 0:
        sys.exit("Script must be run as root (sudo).")
    if platform.system() != 'Darwin':
        sys.exit("This script can only be run on macOS (Darwin).")
    if env_check():
        if not os.path.exists(os.getenv('DB_PATH')):
            sys.exit("CHAT_DB_PATH is not accessible. Please go to Settings > Privacy > Full Disk Access and add Terminal to it. Then re-run this script with sudo.")
    else:
        sys.exit("Error loading .env file.")
    return True

def ssl_check():
    if 'USE_SSL' in os.environ and os.environ['USE_SSL'].lower() == 'true':
        if 'SSL_CERT_PATH' in os.environ and 'SSL_PRIV_KEY_PATH' in os.environ:
            if os.path.exists(os.environ['SSL_CERT_PATH']) and os.path.exists(os.environ['SSL_PRIV_KEY_PATH']):
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
    