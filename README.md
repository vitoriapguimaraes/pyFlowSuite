# PyFlow Suite

> Uma suíte consolidada de ferramentas Python focada em **Otimização** e **Produtividade**. Este repositório unifica projetos de automação e backups em uma interface fluida e moderna com **sistema de configuração inteligente**.

![Demonstração do sistema](https://github.com/vitoriapguimaraes/pyFlowSuite/blob/main/src/demos/navigation.gif)

## Funcionalidades Principais

- **Launcher Modular**: Interface Flet elegante com navegação intuitiva em colunas (Otimização, Produtividade).
- **Product Registration**: Automação completa de cadastro em formulários web a partir de arquivos CSV, incluindo capturador de coordenadas e gravador de workflow.
- **Sales Report**: Geração e envio automático de relatórios de vendas por email (Outlook).
- **Backup Tool**: Sistema robusto de backup automático de diretórios com timestamp e preservação de estrutura.
- **Sistema de Configuração**: Configure seus aplicativos diretamente no launcher com interface de formulário e validação.

## Tecnologias Utilizadas

- **Python 3.11+**
- **Flet** (UI Framework)
- **PyAutoGUI** (Automação de GUI)
- **Pandas** (Análise de Dados)
- **OpenPyXL** (Manipulação de Excel)
- **JSON** (Gerenciamento de Configuração)

## Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/vitoriapguimaraes/pyFlowSuite.git
   cd pyFlowSuite
   ```

2. Crie um ambiente virtual (Recomendado):

   ```bash
   conda create -n pyflow python=3.11
   conda activate pyflow
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o Launcher:

   ```bash
   python src/launcher/main.py
   ```

## Como Usar

1. **Abra o Launcher**: Execute o comando acima para abrir a interface principal.
2. **Escolha a Ferramenta**: Navegue pelas categorias "Otimização" e "Produtividade".
3. **Configure**: Clique no botão "Configurar" (ícone de engrenagem) se a aplicação exigir (ex: caminhos de arquivos, credenciais).
   - _Nota:_ Os campos vêm com exemplos genéricos; substitua pelos seus dados reais.
4. **Execute**: Clique em "Iniciar Aplicação" para rodar a automação ou ferramenta.

### Ferramentas de Auxílio (Product Registration)

- **Capturador de Coordenadas**: Use para mapear posições X,Y dos campos do seu formulário web.
- **Gravador de Workflow**: Grave sequências de ações personalizadas para automação.

## Estrutura de Diretórios

```bash
pyFlowSuite/
├── src/
│   ├── launcher/              # Interface principal e gerenciamento
│   │   ├── main.py
│   │   ├── apps_data.py
│   │   └── ...
│   ├── apps/                  # Aplicações individuais
│   │   ├── product_registration/
│   │   ├── sales_report/
│   │   └── backup_tool/
│   └── data/config/           # Arquivos JSON de configuração do usuário
├── requirements.txt
└── README.md
```

## Status

✅ Concluído

> Veja as [issues abertas](https://github.com/vitoriapguimaraes/pyFlowSuite/issues) para sugestões de melhorias e próximos passos.

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
