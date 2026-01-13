# Como Capturar Coordenadas para Product Registration

## O que são coordenadas?

O Product Registration usa **PyAutoGUI** para automatizar o preenchimento de formulários web. Para isso, ele precisa saber exatamente onde clicar na tela (coordenadas X, Y).

## Passo a Passo

### 1. Preparar o Ambiente

```bash
# Ativar ambiente conda
conda activate pyflow

# Navegar para o diretório
cd src/apps/product_registration
```

### 2. Executar o Capturador

```bash
python capture_coordinates.py
```

### 3. Seguir as Instruções

O script vai solicitar que você posicione o mouse sobre cada campo:

1. **Email de Login** - Campo onde você digita o email
2. **Senha de Login** - Campo onde você digita a senha
3. **Botão Login** - Botão para fazer login
4. **Campo Código** - Campo do código do produto
5. **Campo Marca** - Campo da marca do produto
6. **Campo Tipo** - Campo do tipo do produto
7. **Campo Categoria** - Campo da categoria
8. **Campo Preço** - Campo do preço unitário
9. **Campo Custo** - Campo do custo
10. **Campo Observações** - Campo de observações
11. **Botão Enviar** - Botão para submeter o produto

### 4. Dicas Importantes

- ⏰ Você tem **5 segundos** para posicionar o mouse em cada campo
- 🖱️ Posicione o mouse **NO CENTRO** do campo de texto
- 🌐 Abra o site de cadastro **ANTES** de executar o script
- 📐 Use sempre a **mesma resolução de tela** para consistência
- 💾 As coordenadas serão salvas automaticamente em `src/data/config/product_registration_coordinates.json`

### 5. Usar as Coordenadas

Depois de capturar, as coordenadas serão usadas automaticamente pelo app de Product Registration quando você configurá-lo no launcher.

## Recapturar Coordenadas

Se mudou a resolução da tela ou o layout do site mudou:

```bash
python capture_coordinates.py
```

Execute novamente para recapturar todas as posições.
