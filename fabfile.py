from fabric import task
import os
from datetime import datetime
from invoke import Context

# Caminhos do seu projeto
PROJECT_DIR = "/home/isaac_ponce/ERP_MPRO"
BACKUP_DIR = "/home/isaac_ponce/ERP_MPRO/backups"
VENV_DIR = "/home/isaac_ponce/ERP_MPRO/venv"
GUNICORN_SOCKET = "/tmp/erp.sock"

# Função para criar backup do projeto
def create_backup(c):
    print("Criando uma cópia versionada do projeto...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{BACKUP_DIR}/erp_mpro_backup_{timestamp}.tar.gz"
    
    # Criar diretório de backups se não existir
    c.run(f"mkdir -p {BACKUP_DIR}")
    
    # Criar o arquivo tar.gz do projeto
    c.run(f"tar -czvf {backup_file} -C {PROJECT_DIR} .")
    print(f"Backup criado: {backup_file}")

# Função para garantir que as dependências estão instaladas
def check_requirements(c):
    print("Verificando dependências do projeto...")
    c.run(f"source {VENV_DIR}/bin/activate && pip install -r {PROJECT_DIR}/requirements.txt")

# Função para coletar os arquivos estáticos
def collect_static(c):
    print("Coletando arquivos estáticos...")
    c.run(f"source {VENV_DIR}/bin/activate && python {PROJECT_DIR}/manage.py collectstatic --noinput")

# Função para realizar a migração do banco de dados
def migrate_database(c):
    print("Realizando migrações do banco de dados...")
    c.run(f"source {VENV_DIR}/bin/activate && python {PROJECT_DIR}/manage.py migrate")

# Função para reiniciar o Gunicorn
def restart_gunicorn(c):
    print("Verificando e reiniciando Gunicorn...")
    if not os.path.exists(GUNICORN_SOCKET):
        print("Socket do Gunicorn não encontrado. Iniciando Gunicorn...")
        c.run(f"source {VENV_DIR}/bin/activate && gunicorn --workers 3 --bind unix:{GUNICORN_SOCKET} erp_mpro.wsgi:application &")
    else:
        print("Gunicorn está rodando. Reiniciando Gunicorn...")
        c.run("pkill gunicorn && source {VENV_DIR}/bin/activate && gunicorn --workers 3 --bind unix:{GUNICORN_SOCKET} erp_mpro.wsgi:application &")

# Função para reiniciar o Nginx
def restart_nginx(c):
    print("Verificando e reiniciando Nginx...")
    result = c.run("sudo systemctl status nginx", hide=True, warn=True)
    if result.failed:
        print("Nginx não está rodando. Iniciando Nginx...")
        c.run("sudo systemctl start nginx")
    else:
        print("Nginx está rodando. Reiniciando Nginx...")
        c.run("sudo systemctl restart nginx")

# Função para reiniciar o Cloudflare Tunnel
def restart_cloudflare(c):
    print("Verificando e reiniciando o Cloudflare Tunnel...")
    result = c.run("sudo systemctl status cloudflared", hide=True, warn=True)
    if result.failed:
        print("Cloudflare Tunnel não está rodando. Iniciando Cloudflare Tunnel...")
        c.run("sudo systemctl start cloudflared")
    else:
        print("Cloudflare Tunnel está rodando. Reiniciando Cloudflare Tunnel...")
        c.run("sudo systemctl restart cloudflared")

# Função para verificar e reiniciar o Docker
def restart_docker(c):
    print("Verificando status do Docker...")
    result = c.run("sudo docker ps -q", hide=True, warn=True)
    if result.failed or not result.stdout.strip():
        print("Containers Docker não estão em execução. Iniciando Docker...")
        c.run("sudo docker-compose -f /home/isaac_ponce/ERP_MPRO/docker-compose.yml up -d")
    else:
        print("Containers Docker já estão em execução. Reiniciando serviços necessários...")
        c.run("sudo docker-compose -f /home/isaac_ponce/ERP_MPRO/docker-compose.yml restart web nginx cloudflared")

# Função para testar a conexão (opcional, caso precise verificar conectividade)
def test_connection(c):
    print("Testando conexão local...")
    result = c.run('hostname', warn=True)
    if result.ok:
        print(f"Servidor local: {result.stdout.strip()}")
    else:
        print("Não foi possível determinar o hostname local.")

# Função principal de deploy
@task
def deploy(c):
    print("Iniciando deploy local...")

    # Usar o contexto local
    local_context = Context()

    # Teste de conexão (opcional)
    test_connection(local_context)

    # Criar backup do projeto
    create_backup(local_context)

    # Garantir permissões corretas
    print("Garantindo permissões corretas...")
    local_context.run(f"sudo chown -R $USER:$USER {PROJECT_DIR}")

    # Garantir dependências instaladas
    check_requirements(local_context)

    # Coletar arquivos estáticos
    collect_static(local_context)

    # Realizar migrações
    migrate_database(local_context)

    # Reiniciar Gunicorn
    restart_gunicorn(local_context)

    # Reiniciar Nginx
    restart_nginx(local_context)

    # Reiniciar Cloudflare Tunnel
    restart_cloudflare(local_context)

    # Reiniciar Docker
    restart_docker(local_context)

    print("Deploy concluído com sucesso!")
