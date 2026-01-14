# PyFlow Suite

> Uma suíte consolidada de ferramentas Python focada em **Otimização** e **Produtividade**. Este repositório unifica projetos de automação, backups e comunicação em uma interface fluida e moderna com **sistema de configuração inteligente**.

[![Acesse o Repositório](https://img.shields.io/badge/Ver%20no%20GitHub-gray?style=for-the-badge)](https://github.com/vitoriapguimaraes/pyFlowSuite)

## ✨ Destaques

- 🎨 **Launcher Modular** - Interface Flet elegante com navegação intuitiva
- ⚙️ **Sistema de Configuração** - Configure apps uma vez, use sempre
- 🎯 **Captura de Coordenadas** - Ferramenta interativa para automação GUI
- 🎬 **Gravador de Workflow** - Defina fluxos personalizados de automação
- 🛑 **Parada de Emergência** - ESC para interromper automações com segurança
- 📦 **Código Modularizado** - Arquitetura limpa e manutenível

## Funcionalidades Principais

O **PyFlow Launcher** organiza as ferramentas em três pilares essenciais:

### 🔥 Otimização & Automação

_Ferramentas para economizar tempo e eliminar tarefas repetitivas._

#### Product Registration

Automação completa de cadastro em formulários web a partir de arquivos CSV.

**Recursos:**

- 📄 Importa dados de CSV
- 🌐 Preenche formulários web automaticamente
- ⚡ Processa centenas de produtos
- 🎯 **Capturador de coordenadas** (posições X,Y dos campos)
- 🎬 **Gravador de workflow** (define fluxo completo: navegação, login, preenchimento)
- 🛑 **Parada de emergência** (ESC ou mova mouse para canto)
- ⚙️ **Configurável** (CSV, URL, email, senha via launcher)

#### Sales Report Generator

Geração e envio automático de relatórios de desempenho por email.

**Recursos:**

- 📊 Análise automática de vendas
- 📧 Envio por email (Outlook)
- 💰 Cálculo de métricas-chave
- ⚙️ **Configurável** (Excel path, email destinatário)

### 💼 Produtividade & Utilitários

_Ferramentas para segurança e gestão de arquivos._

#### Backup Tool

Sistema robusto de backup automático com organização por data/hora.

**Recursos:**

- 💾 Backup completo de diretórios
- 🕐 Timestamp automático
- 📁 Preserva estrutura de pastas
- 🚀 Interface de seleção de pastas

### 💬 Comunicação

_Ferramentas para conexão em tempo real._

#### Real-Time Chat

Chat moderno com suporte a Web e Desktop.

**Versões:**

- **Web** (Flask + SocketIO) - Acesso via navegador
- **Desktop** (Flet) - Interface nativa
- 👥 Múltiplos usuários simultâneos
- ⚡ Mensagens em tempo real

## Tecnologias Utilizadas

### Core

- **Python 3.11+**
- **Flet 0.23.2** - UI Framework (baseado em Flutter)

### Automação

- **PyAutoGUI** - Automação de GUI
- **Keyboard** - Detecção de teclas (ESC emergency stop)
- **Pandas** - Manipulação de dados
- **OpenPyXL** - Excel I/O

### Web & Comunicação

- **Flask** - Web framework
- **Flask-SocketIO** - Real-time messaging

### Gerenciamento

- **JSON** - Armazenamento de configurações
- **Pathlib** - Manipulação de caminhos

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/vitoriapguimaraes/pyFlowSuite.git
cd pyFlowSuite
```

### 2. Crie ambiente Conda (Recomendado)

```bash
conda create -n pyflow python=3.11
conda activate pyflow
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o Launcher

```bash
python src/launcher/main.py
```

## 🎯 Como Configurar Aplicações

### Via Launcher (Recomendado)

1. Abra o launcher
2. Clique no aplicativo desejado
3. Clique em **"Configurar"**
4. Preencha os campos:
   - **Product Registration**: CSV path, URL, email, senha
   - **Sales Report**: Excel path, email destinatário
5. Clique em **"Salvar"**

### Ferramentas Especiais (Product Registration)

#### 🎯 Capturador de Coordenadas

1. No diálogo de configuração, clique em **"🎯 Capturar Coordenadas"**
2. Posicione o mouse sobre cada campo (5 segundos)
3. Coordenadas são salvas automaticamente

#### 🎬 Gravador de Workflow

1. No diálogo de configuração, clique em **"🎬 Gravar Workflow"**
2. Execute ações manualmente e pressione:
   - **F1**: Abrir navegador
   - **F2**: Navegar para URL
   - **Ctrl+E**: Marcar campo EMAIL (usa config)
   - **Ctrl+P**: Marcar campo SENHA (usa config)
   - **F4-F7**: Ações de produto
   - **F9**: Finalizar gravação
3. Workflow salvo em JSON

## Estrutura de Diretórios

```
pyFlowSuite/
├── src/
│   ├── launcher/              # Launcher modular
│   │   ├── main.py           # Entry point
│   │   ├── apps_data.py      # Definições de apps
│   │   ├── dialogs.py        # Gerenciamento de modais
│   │   ├── ui_builder.py     # Construção da UI
│   │   └── config_manager.py # Gerenciamento de configs
│   │
│   ├── apps/                  # Aplicações
│   │   ├── product_registration/
│   │   │   ├── app.py                  # App principal
│   │   │   ├── capture_coordinates.py  # Capturador
│   │   │   ├── record_workflow.py      # Gravador
│   │   │   ├── COORDINATES_GUIDE.md
│   │   │   └── WORKFLOW_GUIDE.md
│   │   ├── backup_tool/
│   │   ├── sales_report/
│   │   └── realtime_chat/
│   │
│   └── data/
│       └── config/            # Configurações salvas (JSON)
│
├── legacy_code/               # Código original (histórico)
├── requirements.txt
├── SETUP.md
└── README.md
```

## 🔧 Configurações Salvas

As configurações são salvas em `src/data/config/`:

- `product_registration.json` - Config do Product Registration
- `product_registration_coordinates.json` - Coordenadas capturadas
- `product_registration_workflow.json` - Workflow gravado
- `sales_report.json` - Config do Sales Report

## � Recursos de Segurança

### Emergency Stop (Product Registration)

Durante a automação, você pode parar imediatamente:

1. **Pressione ESC** - Interrompe no próximo loop
2. **Mouse no canto** - PyAutoGUI failsafe

## Status

🚀 **Ativo e Funcional**

### Próximas Melhorias

- [ ] Integração de workflow recorder com app
- [ ] Validação de arquivos na configuração
- [ ] Testes automatizados
- [ ] Suporte a múltiplos perfis de configuração

> Veja as [issues abertas](https://github.com/vitoriapguimaraes/PyFlow-Suite/issues) para sugestões.

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.