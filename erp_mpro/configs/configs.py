import os
from decouple import config


DEBUG = True

# Configuração da base de dados
# Exemplo: DEFAULT_DATABASE_URL = 'postgres://user:pass@localhost/dbname'
# Caso seja deixado vazio, o padrão será SQLite
DEFAULT_DATABASE_URL = config(
    'DEFAULT_DATABASE_URL',
    default=f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')}"
)

# Configurações do servidor de email
# Obs: O endereço de email é utilizado para troca de senha do usuário e notificações do sistema.

# Endereço de email padrão utilizado
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='isaac.ponce@duponce.com.br')

# Configuração do servidor de e-mail
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')  # Exemplo: Gmail como provedor de SMTP

# Usuário do email padrão
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='isaac.ponce@duponce.com.br')

# Senha do email padrão
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='Poeta.2023')

# Porta utilizada pelo serviço de email
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)

# Uso de TLS (Transport Layer Security) para conexão segura
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# Configuração de Token de acesso
# Define um token fixo para o administrador/desenvolvedor
DEVELOPER_ADMIN_TOKEN = config('DEVELOPER_ADMIN_TOKEN', default='ERP_MPRO_ADMIN_2023')

# Informação adicional do sistema para identificação do desenvolvedor
SYSTEM_ADMIN = {
    'name': config('SYSTEM_ADMIN_NAME', default='Isaac Ponce'),
    'email': config('SYSTEM_ADMIN_EMAIL', default='isaac.ponce@duponce.com.br'),
    'role': config('SYSTEM_ADMIN_ROLE', default='Administrador e Desenvolvedor'),
    'token': DEVELOPER_ADMIN_TOKEN,
}

# Configurações de hosts permitidos
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='nformasmoveis.com.br, www.nformasmoveis.com.br, 127.0.0.1, localhost',
    cast=lambda v: [host.strip() for host in v.split(',')]
)
