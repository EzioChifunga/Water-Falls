#!/bin/bash

# 🚀 WaterFalls API - Script de Deploy Automático
# Execute este script na sua VPS para deploy automático

set -e  # Sair em caso de erro

echo "======================================"
echo "  WaterFalls API - Deploy Automático"
echo "======================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para printar com cores
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
   print_error "Este script precisa ser executado como root (sudo)"
   exit 1
fi

# 1. Verificar Docker
print_info "Verificando Docker..."
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado"
    print_info "Instalando Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    print_status "Docker instalado"
else
    print_status "Docker encontrado"
fi

# 2. Verificar Docker Compose
print_info "Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado"
    print_info "Instalando Docker Compose..."
    apt-get update
    apt-get install -y docker-compose
    print_status "Docker Compose instalado"
else
    print_status "Docker Compose encontrado"
fi

# 3. Criar diretório do projeto
print_info "Preparando diretório do projeto..."
mkdir -p /opt/WaterFalls-API
cd /opt/WaterFalls-API
print_status "Diretório criado/verificado"

# 4. Clonar repositório (se não existir)
if [ ! -d ".git" ]; then
    print_info "Clonando repositório..."
    git clone https://github.com/seu-usuario/WaterFalls-API.git .
    print_status "Repositório clonado"
else
    print_info "Repositório já existe, puxando atualizações..."
    git pull origin master
    print_status "Repositório atualizado"
fi

# 5. Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    print_info "Criando arquivo .env..."
    cat > .env << EOF
DATABASE_URL=postgresql://postgres:sua_senha_aqui@31.97.170.13:5433/water_falls?sslmode=disable
API_PORT=8000
EOF
    print_status "Arquivo .env criado"
    print_error "IMPORTANTE: Edite o arquivo .env com suas credenciais!"
    nano .env
else
    print_status "Arquivo .env já existe"
fi

# 6. Parar containers existentes
print_info "Parando containers existentes..."
docker-compose down 2>/dev/null || true
print_status "Containers parados"

# 7. Construir imagem
print_info "Construindo imagem Docker..."
docker-compose build --no-cache
print_status "Imagem construída"

# 8. Iniciar containers
print_info "Iniciando containers..."
docker-compose up -d
print_status "Containers iniciados"

# 9. Aguardar inicialização
print_info "Aguardando inicialização da aplicação (30 segundos)..."
sleep 30

# 10. Executar migrações
print_info "Executando migrações..."
docker-compose exec -T waterfalls-api alembic upgrade head
print_status "Migrações executadas"

# 11. Verificar status
print_info "Verificando status dos containers..."
docker-compose ps
print_status "Containers rodando"

# 12. Testar conexão
print_info "Testando conexão com a API..."
if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
    print_status "API respondendo normalmente"
else
    print_error "API não está respondendo"
    print_info "Verifique os logs: docker-compose logs waterfalls-api"
    exit 1
fi

# 13. Configurar Nginx (opcional)
read -p "Deseja configurar Nginx como proxy reverso? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_info "Configurando Nginx..."
    
    read -p "Digite seu domínio (ex: seu-dominio.com): " DOMAIN
    
    if ! command -v nginx &> /dev/null; then
        print_info "Instalando Nginx..."
        apt-get install -y nginx
        print_status "Nginx instalado"
    fi
    
    # Criar configuração Nginx
    cat > /etc/nginx/sites-available/waterfalls << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }
}
EOF

    # Ativar site
    ln -sf /etc/nginx/sites-available/waterfalls /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
    
    # Testar e reiniciar Nginx
    nginx -t && systemctl restart nginx
    print_status "Nginx configurado"
    
    # Configurar SSL
    read -p "Deseja configurar SSL/HTTPS com Certbot? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        print_info "Instalando Certbot..."
        apt-get install -y certbot python3-certbot-nginx
        
        print_info "Configurando certificado SSL..."
        certbot --nginx -d $DOMAIN --agree-tos --register-unsafely-without-email --non-interactive
        print_status "SSL configurado"
    fi
fi

# Sucesso!
echo ""
echo "======================================"
echo -e "${GREEN}✓ Deploy concluído com sucesso!${NC}"
echo "======================================"
echo ""
echo "📊 Próximos passos:"
echo ""
if [ -z "$DOMAIN" ]; then
    echo "1. Acesse a API em: http://seu_ip_vps:8000"
    echo "2. Documentação: http://seu_ip_vps:8000/docs"
else
    echo "1. Acesse a API em: http://$DOMAIN"
    echo "2. Documentação: http://$DOMAIN/docs"
fi
echo ""
echo "📝 Comandos úteis:"
echo "   Ver logs:              docker-compose logs -f waterfalls-api"
echo "   Ver status:            docker-compose ps"
echo "   Parar aplicação:       docker-compose down"
echo "   Reiniciar aplicação:   docker-compose restart"
echo "   Atualizar código:      git pull && docker-compose build && docker-compose up -d"
echo ""
echo "======================================"
