```markdown
# **ERP MPRO Build Status**
**Sistema Integrado de Gestão Empresarial baseado em Django**

Projeto independente open-source desenvolvido em Python 3 no Windows, testado no GNU/Linux e Windows.

---

## **Dependências**
- **Python** - Versão 3.5+
- **Django** - `3.1.7`
- **Geraldo** - Geração de PDF para pedidos de venda/compra
- **PySIGNFe (Opcional)** - Necessário para a geração de NF-e, NFC-e, comunicação com SEFAZ, geração do DANFE, etc.
- **Apache2 (Opcional)**
- **mod_wsgi (Opcional)**

---

## **Instalação**
### **1. Instalar bibliotecas/pacotes no Linux:**
```bash
sudo apt install -y libxml2 gcc python3-dev libxml2-dev libxslt1-dev zlib1g-dev python3-pip
sudo apt update
```

### **2. Instalar dependências:**
```bash
pip install -r requirements.txt
```

### **3. Configuração inicial:**
Edite o conteúdo do arquivo `erp_mpro/configs/configs.py`.

### **4. Gere um arquivo `.env` local:**
```bash
python contrib/env_gen.py
```

### **5. Sincronize a base de dados:**
```bash
python manage.py migrate
```

### **6. Crie um usuário administrador do sistema:**
```bash
python manage.py createsuperuser
```

### **7. Teste a instalação:**
Carregue o servidor de desenvolvimento e acesse em seu navegador: [http://localhost:8000](http://localhost:8000).

```bash
python manage.py runserver
```

---

## **Implementações**
- Cadastro de **produtos**, **clientes**, **empresas**, **fornecedores** e **transportadoras**.
- **Login/Logout**.
- Criação de **perfil** para cada usuário.
- Definição de **permissões** para usuários.
- Criação e geração de **PDF** para orçamentos e pedidos de compra/venda.
- **Módulo financeiro**:
  - Plano de Contas
  - Fluxo de Caixa
  - Lançamentos
- **Módulo para controle de estoque**.
- **Módulo fiscal**:
  - Geração e armazenamento de notas fiscais.
  - Validação do XML de NF-e/NFC-es.
  - Emissão, download, consulta e cancelamento de NF-e/NFC-es (Testar em ambiente de homologação).
  - Comunicação com SEFAZ:
    - Consulta de cadastro.
    - Inutilização de notas.
    - Manifestação do destinatário.

---

## **Interface**
- Interface simples e em português.

---

## **Créditos**
- **AdminBSBMaterialDesign**
- **Geraldo**
- **jQuery-Mask-Plugin**
- **DataTables**
- **JQuery multiselect**

---

## **Base do projeto**
**Projeto Open Source**.

---

## **Ajuda**
- Para relatar bugs ou fazer perguntas, utilize o [Issues](https://github.com/ERP_MPRO/issues) ou entre em contato via email: **isaac.ponce@duponce.com**.

---

**Nota:** Como este é um projeto em desenvolvimento, qualquer feedback será bem-vindo!
```