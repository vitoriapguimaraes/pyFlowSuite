# Gravador de Workflow - Product Registration

## O que é?

Um gravador interativo que permite você definir o **fluxo completo** da automação, não apenas as coordenadas.

## Por que usar?

Diferentes sites podem ter:

- Formas diferentes de abrir (Chrome vs Edge vs já aberto)
- URLs diferentes
- Sequências de login diferentes
- Necessidade de scroll em quantidades diferentes
- Campos em ordens diferentes

## Como Usar

### 1. Executar o Gravador

```bash
cd src/apps/product_registration
python record_workflow.py
```

### 2. Gravar suas Ações

Enquanto o gravador está ativo, **execute manualmente** cada passo e pressione a tecla correspondente:

- **F1** = "Abrir navegador" (quando você abrir)
- **F2** = "Navegar para URL" (quando colar a URL)
- **F3** = "Fazer login" (quando fazer login)
- **F4** = "Clicar primeiro campo" (quando começar produto)
- **F5** = "Preencher campos" (quando preencher)
- **F6** = "Submeter formulário" (quando enviar)
- **F7** = "Scroll" (quando scrollar)
- **F8** = "Esperar 3 segundos"
- **F9** = **PARAR GRAVAÇÃO**

### 3. Fluxo Típico

```bash
1. Pressione ENTER para começar
2. Abra o navegador → Pressione F1
3. Vá para o site → Pressione F2 (vai pedir a URL)
4. Faça login → Pressione F3
5. Comece a preencher 1 produto:
   - Clique no primeiro campo → F4
   - Preencha todos os campos → F5
   - Envie o formulário → F6
   - Scroll se necessário → F7
6. Pressione F9 para finalizar
```

### 4. Exemplo de Saída

```json
[
  { "type": "open_browser", "delay": 0.0 },
  { "type": "navigate_to_url", "delay": 2.3, "data": { "url": "https://..." } },
  { "type": "delay", "delay": 0.5, "data": { "seconds": 3 } },
  { "type": "login", "delay": 3.2 },
  { "type": "click_first_field", "delay": 2.8 },
  { "type": "fill_product_fields", "delay": 0.5 },
  { "type": "submit_form", "delay": 1.2 },
  { "type": "scroll", "delay": 0.3, "data": { "amount": 5000 } }
]
```

## Benefícios

- ✅ **Flexível** - Suporta qualquer fluxo
- ✅ **Timing preciso** - Grava delays reais
- ✅ **Personalizado** - Cada instalação pode ter fluxo diferente
- ✅ **Visual** - Feedback em tempo real

## Arquivo Gerado

`src/data/config/product_registration_workflow.json`

Este arquivo será lido pelo app e executado exatamente como você gravou!
