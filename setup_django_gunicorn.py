import os
import subprocess
import sys
import time

# Defina o caminho do projeto e do ambiente virtual
PROJECT_DIR = '/home/isaac_ponce/ERP_MPRO/'
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
GUNICORN_SERVICE_PROD_PATH = '/etc/systemd/system/gunicorn.service'
GUNICORN_SERVICE_TEST_PATH = '/etc/systemd/system/gunicorn.service'
NGINX_CONF_PROD_PATH = '/etc/nginx/sites-available/erp_mpro'
NGINX_LINK_PROD_PATH = '/etc/nginx/sites-enabled/erp_mpro'
NGINX_CONF_TEST_PATH = '/etc/nginx/sites-available/erp_mpro'
NGINX_LINK_TEST_PATH = '/etc/nginx/sites-enabled/erp_mpro'
CLOUDFLARE_TUNNEL_FILE = '/etc/cloudflared/3c61dd5c-6c39-470e-9d8a-45cb226bb8fd.json'

# Domínio para produção e teste
DOMAIN_PROD = 'nformasmoveis.com.br'
DOMAIN_TEST = 'test.nformasmoveis.com.br'

# Função para rodar comandos no shell
def run_command(command, use_sudo=False):
    try:
        # Adiciona sudo ao comando se necessário
        if use_sudo:
            command = f"sudo {command}"

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Comando '{command}' executado com sucesso!")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando '{command}': {e.stderr.decode()}")
        return e.stderr.decode()
    return ""

# Função para criar o ambiente virtual
def create_virtualenv():
    if not os.path.exists(VENV_DIR):
        print("Criando ambiente virtual...")
        run_command(f"python3 -m venv {VENV_DIR}")
    else:
        print("Ambiente virtual já existe. Ativando...")

# Função para instalar as dependências
def install_dependencies():
    print("Instalando dependências...")
    run_command(f"{VENV_DIR}/bin/pip install -r {PROJECT_DIR}/requirements.txt")

# Função para recriar o arquivo de serviço do Gunicorn
def recreate_gunicorn_service(env='prod'):
    if env == 'prod':
        service_path = GUNICORN_SERVICE_PROD_PATH
        workers = 4  # Mais workers para produção
    else:
        service_path = GUNICORN_SERVICE_TEST_PATH
        workers = 1  # Menos workers para teste
    
    if os.path.exists(service_path):
        print(f"Removendo arquivo de serviço Gunicorn existente para {env}...")
        run_command(f"sudo rm -f {service_path}")

    print(f"Criando arquivo de serviço Gunicorn para {env}...")
    service_content = f"""
[Unit]
Description=Gunicorn daemon for Django project ({env})
After=network.target

[Service]
User=isaac_ponce
Group=isaac_ponce
WorkingDirectory={PROJECT_DIR}  # Certifique-se de que esta é a pasta que contém o manage.py
ExecStart={VENV_DIR}/bin/gunicorn --workers {workers} --bind unix:{PROJECT_DIR}/erp_mpro.sock ERP_MPRO.wsgi:application
Environment=PYTHONPATH={PROJECT_DIR}
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gunicorn_{env}

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, 'w') as f:
        f.write(service_content)
    print(f"Arquivo de serviço Gunicorn criado em {service_path}")

    # Recarregar o daemon systemd para aplicar a nova configuração
    run_command("sudo systemctl daemon-reload")
    print("Daemon reloaded!")

# Função para reiniciar o Gunicorn e garantir que está funcionando
def restart_and_check_gunicorn(env='prod'):
    print(f"Tentando reiniciar o Gunicorn para {env}...")
    run_command(f"sudo systemctl restart gunicorn_{env}")
    # Aguardar alguns segundos antes de verificar novamente
    time.sleep(5)
    
    # Verificar o status após o restart
    status_output = run_command(f"sudo systemctl status gunicorn_{env}", use_sudo=True)
    
    if "active (running)" not in status_output:
        print(f"Erro ao iniciar o Gunicorn para {env}. Verificando logs...")
        error_log = run_command(f"sudo journalctl -u gunicorn_{env} --since '1 hour ago'", use_sudo=True)
        print(error_log)
        sys.exit(1)
    else:
        print(f"Gunicorn está rodando corretamente em {env}!")

# Função para configurar o Nginx para produção e teste
def configure_nginx(env='prod'):
    if env == 'prod':
        domain = DOMAIN_PROD
        nginx_conf_path = NGINX_CONF_PROD_PATH
        nginx_link_path = NGINX_LINK_PROD_PATH
    else:
        domain = DOMAIN_TEST
        nginx_conf_path = NGINX_CONF_TEST_PATH
        nginx_link_path = NGINX_LINK_TEST_PATH

    if not os.path.exists(nginx_conf_path):
        print(f"Criando configuração do Nginx para {env}...")
        nginx_config = f"""
server {{
    listen 80;
    server_name {domain};

    # Logs
    access_log /var/log/nginx/erp_mpro_{env}_access.log;
    error_log /var/log/nginx/erp_mpro_{env}_error.log;

    # Diretório do seu projeto Django
    root {PROJECT_DIR};

    # Arquivos estáticos
    location /static/ {{
        alias {PROJECT_DIR}/static/;
    }}

    # Arquivos de mídia
    location /media/ {{
        alias {PROJECT_DIR}/media/;
    }}

    # Proxy reverso para Gunicorn
    location / {{
        proxy_pass http://unix:{PROJECT_DIR}/erp_mpro.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        with open(nginx_conf_path, 'w') as f:
            f.write(nginx_config)
        print(f"Configuração do Nginx criada em {nginx_conf_path}")

        run_command(f"sudo ln -s {nginx_conf_path} {nginx_link_path}")
        print(f"Link simbólico criado para o Nginx para {env}.")
    else:
        print(f"Arquivo de configuração do Nginx para {env} já existe.")

    run_command("sudo nginx -t")
    print("Configuração do Nginx está correta!")
    run_command("sudo systemctl restart nginx")
    print(f"Nginx reiniciado com sucesso para {env}!")

# Função para configurar o Cloudflare Tunnel
def configure_cloudflare_tunnel():
    if not os.path.exists(CLOUDFLARE_TUNNEL_FILE):
        print("Arquivo de credenciais do Cloudflare Tunnel não encontrado!")
        sys.exit(1)

    print("Reiniciando o Cloudflare Tunnel...")
    run_command("sudo systemctl restart cloudflared")

def main():
    print("Iniciando a automação da configuração do Gunicorn, Nginx e Cloudflare...")
    
    if os.geteuid() != 0:
        print("Este script precisa ser executado como superusuário.")
        sys.exit(1)
    
    create_virtualenv()
    install_dependencies()

    # Configuração para produção
    recreate_gunicorn_service(env='prod')
    restart_and_check_gunicorn(env='prod')
    configure_nginx(env='prod')

    # Configuração para teste
    recreate_gunicorn_service(env='test')
    restart_and_check_gunicorn(env='test')
    configure_nginx(env='test')

    configure_cloudflare_tunnel()

    print("Configuração concluída com sucesso!")

if __name__ == "__main__":
    main()
