Excelente! Vamos fazer exatamente o que pediu: **tradução para inglês** do seu README, mas mantendo também a parte em português (PT-BR) em seções distintas, tudo num arquivo **Markdown (README.md)** bem organizado.

Segue o arquivo pronto para usar — **bilingue** — com as duas versões separadas. Pode copiar e colar direto no seu projeto!

---

````markdown
# 🎛️ YASB Control Panel - Python Version

_A modern and intuitive graphical interface to configure YASB (Yet Another Status Bar) on Windows, developed in Python with tkinter/ttk._

---

## 📋 About the Project

This control panel allows you to visually configure YASB without manually editing YAML and CSS files. With a native and modern desktop interface, you can manage widgets, customize styles, and adjust advanced settings in a simple and efficient way.

---

## ✨ Features

### 🧩 Widget Management
- **Tree view** of all configured widgets
- **Enable/disable** widgets with a single click
- **Edit properties** like position (left, center, right)
- **Configure specific parameters** for each widget
- **Add new widgets** with custom settings
- **Duplicate existing widgets**
- **Remove unnecessary widgets**

### 🎨 Style Editor
- **Integrated color picker** for visual customization
- **Predefined themes** (Dark, Light, Blue, Green)
- **Font configuration** (family, size, weight)
- **Spacing adjustments** (padding, margin)
- **Border settings** (width, radius, color)
- **Advanced style editor** with multiple categories
- **Save and load** custom themes

### ⚙️ Advanced Settings
- **System settings** (auto-start, debug mode)
- **Display settings** (monitor, position, dimensions)
- **Integrated YAML editor** for manual configurations
- **Real-time YAML syntax validation**
- **Automatic YAML formatting**

### 👁️ Preview and Testing
- **Visual preview** of the status bar
- **Detailed configuration information**
- **Test configuration** with validation
- **Take screenshots** of the preview
- **Automatically reload YASB**

---

## 🚀 Technologies Used

- **Python 3.11+** - Programming language
- **tkinter/ttk** - Native graphical interface
- **PyYAML** - YAML file handling
- **JSON** - Saving custom themes

---

## 🛠️ Installation and Configuration

### Prerequisites
- Python 3.11 or higher
- YASB installed and configured on Windows
- Python libraries: `pyyaml`, `tkinter` (usually included with Python)

### Installation

1. **Download the control panel files**
   ```bash
   # Clone or download files into a local folder
   mkdir yasb_control_panel
   cd yasb_control_panel
````

2. **Install dependencies**

   ```bash
   pip install pyyaml
   ```

3. **Check if tkinter is available**

   ```bash
   python -c "import tkinter; print('tkinter available')"
   ```

---

### Initial Configuration

1. **Run the control panel**

   ```bash
   python main_enhanced.py
   ```

2. **Set the YASB path**

   * Click "📂 Set YASB Path"
   * Select the directory where YASB is installed
   * Example: `C:\Program Files\yasb` or `C:\Users\YourUser\yasb`

3. **Load your existing configuration**

   * Click "📁 Open Config"
   * Select your YASB `config.yaml` file
   * Or let the panel auto-load it from the default directory

---

## 📖 How to Use

### Widget Management

1. **View Widgets**

   * Go to the "🧩 Widgets" tab
   * See all widgets listed in the tree on the left
   * Click on a widget to see its properties

2. **Add New Widget**

   * Click "➕ Add"
   * Choose widget type
   * Configure options
   * Set position on the bar (left, center, right)

3. **Edit Existing Widget**

   * Select the widget in the tree
   * Click "✏️ Edit"
   * Modify settings as needed

4. **Enable/Disable Widget**

   * Select the widget
   * Click "🔄 Enable/Disable"

---

### Style Customization

1. **Apply Predefined Theme**

   * Go to the "🎨 Styles" tab
   * Choose a theme (Dark, Light, Blue, Green)
   * Theme is applied automatically

2. **Customize Colors**

   * Click the "🎨" buttons next to each color
   * Use the color picker
   * Or enter the hex code manually

3. **Configure Font and Layout**

   * Adjust font family, size, and weight
   * Configure padding and margin
   * Click "✅ Apply Styles"

4. **Advanced Editor**

   * Click "🎨 Advanced Editor"
   * Configure colors, typography, layout, and effects
   * Save advanced settings

---

### Advanced Settings

1. **System Settings**

   * Go to the "⚙️ Advanced" tab
   * Configure auto-start and debug mode
   * Adjust display settings

2. **YAML Editor**

   * Edit configuration directly in YAML
   * Use "✅ Validate YAML" to check syntax
   * Use "🔧 Format" to organize code

---

### Preview and Testing

1. **Visual Preview**

   * Go to the "👁️ Preview" tab
   * Click "🔄 Refresh Preview"
   * See how the bar will look

2. **Test Configuration**

   * Click "🚀 Test Configuration"
   * Check for issues in your config

3. **Apply to YASB**

   * Save the configuration with "💾 Save Config"
   * Click "🔄 Reload YASB" to apply

---

## 📁 File Structure

```
yasb_control_panel/
├── main_enhanced.py          # Main application
├── widget_dialogs.py         # Dialogs for widget editing
├── config_example.yaml       # Sample configuration
├── test_config.py            # Test scripts
├── README.md                 # This file
└── themes/                   # Custom themes (created automatically)
```

---

## 🔧 Supported Widget Types

* **ClockWidget** - Clock with date and time
* **CpuWidget** - CPU monitor
* **MemoryWidget** - RAM monitor
* **BatteryWidget** - Battery status
* **VolumeWidget** - Volume control
* **NetworkWidget** - Network status
* **ActiveWindowWidget** - Active window
* **WeatherWidget** - Weather information
* **DiskWidget** - Disk usage
* **CustomWidget** - Custom widget

---

## 🎨 Predefined Themes

### Dark Theme (Default)

* Background: `#1e1e1e`
* Text: `#ffffff`
* Accent: `#007acc`
* Border: `#333333`

### Light Theme

* Background: `#ffffff`
* Text: `#000000`
* Accent: `#0078d4`
* Border: `#cccccc`

### Blue Theme

* Background: `#0f1419`
* Text: `#e6e6e6`
* Accent: `#00d4ff`
* Border: `#1e3a5f`

### Green Theme

* Background: `#0d1117`
* Text: `#c9d1d9`
* Accent: `#00ff88`
* Border: `#21262d`

---

## 🐛 Troubleshooting

### Error: "YASB not found"

* Check if YASB is installed
* Use "📂 Set YASB Path" to manually set the path
* Ensure the directory contains YASB files

### Error: "Error loading configuration"

* Check if YAML file is valid
* Use the integrated YAML validator
* Ensure the file isn't in use by another program

### Error: "Failed to reload YASB"

* Make sure YASB isn’t running
* Run the panel as administrator if needed
* Check if the YASB path is correct

### Interface not responding

* Close and reopen the app
* Check for errors in the console
* Ensure Python and tkinter are working properly

---

## 📝 Usage Tips

1. **Backup your Config**

   * Always back up your `config.yaml` before making changes
   * Use "💾 Save Config" regularly

2. **Test Before Applying**

   * Use the preview to see how it will look
   * Test your config before reloading YASB

3. **Organize Widgets**

   * Keep related widgets in the same position
   * Use descriptive names for custom widgets

4. **Customize Styles**

   * Start with a predefined theme
   * Make gradual changes
   * Save custom themes for reuse

---

## 🤝 Contribution

This panel was developed as a desktop alternative to the original web panel. Suggestions and improvements are welcome!

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 🙏 Acknowledgements

* **YASB Team** - For the excellent YASB project
* **Python Community** - For the libraries used
* **Users** - For feedback and suggestions

---

**Developed with ❤️ for the YASB community**

---

---

# 🇧🇷 **Leia em Português (PT-BR)**

# 🎛️ Painel de Controle YASB - Versão Python


Uma interface gráfica moderna e intuitiva para configurar o YASB (Yet Another Status Bar) no Windows, desenvolvida em Python com tkinter/ttk.

## 📋 Sobre o Projeto

Este painel de controle permite configurar visualmente o YASB sem a necessidade de editar arquivos YAML e CSS manualmente. Com uma interface desktop nativa e moderna, você pode gerenciar widgets, customizar estilos e ajustar configurações avançadas de forma simples e eficiente.

## ✨ Funcionalidades

### 🧩 Gerenciamento de Widgets
- **Visualização em árvore** de todos os widgets configurados
- **Ativar/desativar** widgets com um clique
- **Editar propriedades** como posição (left, center, right)
- **Configurar parâmetros** específicos de cada widget
- **Adicionar novos widgets** com configurações personalizadas
- **Duplicar widgets** existentes
- **Remover widgets** desnecessários

### 🎨 Editor de Estilos
- **Seletor de cores** integrado para personalização visual
- **Temas predefinidos** (Escuro, Claro, Azul, Verde)
- **Configuração de fonte** (família, tamanho, peso)
- **Ajuste de espaçamento** (padding, margin)
- **Configuração de bordas** (largura, raio, cor)
- **Editor avançado de estilos** com múltiplas categorias
- **Salvamento e carregamento** de temas personalizados

### ⚙️ Configurações Avançadas
- **Configurações do sistema** (auto-start, debug mode)
- **Configurações de exibição** (monitor, posição, dimensões)
- **Editor YAML** integrado para configurações manuais
- **Validação** de sintaxe YAML em tempo real
- **Formatação automática** de YAML

### 👁️ Preview e Testes
- **Preview visual** da barra de status
- **Informações detalhadas** da configuração
- **Teste de configuração** com validação
- **Captura de screenshots** do preview
- **Recarga automática** do YASB

## 🚀 Tecnologias Utilizadas

- **Python 3.11+** - Linguagem de programação
- **tkinter/ttk** - Interface gráfica nativa
- **PyYAML** - Manipulação de arquivos YAML
- **JSON** - Salvamento de temas personalizados

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- YASB instalado e configurado no Windows
- Bibliotecas Python: `pyyaml`, `tkinter` (geralmente incluído com Python)

### Instalação

1. **Baixe os arquivos do painel de controle**
   ```bash
   # Clone ou baixe os arquivos para uma pasta local
   mkdir yasb_control_panel
   cd yasb_control_panel
   ```

2. **Instale as dependências**
   ```bash
   pip install pyyaml
   ```

3. **Verifique se o tkinter está disponível**
   ```bash
   python -c "import tkinter; print('tkinter disponível')"
   ```

### Configuração Inicial

1. **Execute o painel de controle**
   ```bash
   python main_enhanced.py
   ```

2. **Configure o caminho do YASB**
   - Clique em "📂 Definir Caminho YASB"
   - Selecione o diretório onde o YASB está instalado
   - Exemplo: `C:\Program Files\yasb` ou `C:\Users\SeuUsuario\yasb`

3. **Carregue sua configuração existente**
   - Clique em "📁 Abrir Config"
   - Selecione seu arquivo `config.yaml` do YASB
   - Ou deixe o painel carregar automaticamente se estiver no diretório padrão

## 📖 Como Usar

### Gerenciamento de Widgets

1. **Visualizar Widgets**
   - Acesse a aba "🧩 Widgets"
   - Veja todos os widgets na árvore à esquerda
   - Clique em um widget para ver suas propriedades

2. **Adicionar Novo Widget**
   - Clique em "➕ Adicionar"
   - Escolha o tipo de widget
   - Configure as opções
   - Defina a posição na barra (esquerda, centro, direita)

3. **Editar Widget Existente**
   - Selecione o widget na árvore
   - Clique em "✏️ Editar"
   - Modifique as configurações conforme necessário

4. **Ativar/Desativar Widget**
   - Selecione o widget
   - Clique em "🔄 Ativar/Desativar"

### Personalização de Estilos

1. **Aplicar Tema Predefinido**
   - Acesse a aba "🎨 Estilos"
   - Selecione um tema (Escuro, Claro, Azul, Verde)
   - O tema será aplicado automaticamente

2. **Personalizar Cores**
   - Clique nos botões "🎨" ao lado de cada cor
   - Use o seletor de cores para escolher
   - Ou digite o código hexadecimal diretamente

3. **Configurar Fonte e Layout**
   - Ajuste família, tamanho e peso da fonte
   - Configure padding e margin
   - Clique em "✅ Aplicar Estilos"

4. **Editor Avançado**
   - Clique em "🎨 Editor Avançado"
   - Configure cores, tipografia, layout e efeitos
   - Salve configurações avançadas

### Configurações Avançadas

1. **Configurações do Sistema**
   - Acesse a aba "⚙️ Avançado"
   - Configure auto-start e modo debug
   - Ajuste configurações de exibição

2. **Editor YAML**
   - Edite a configuração diretamente em YAML
   - Use "✅ Validar YAML" para verificar sintaxe
   - Use "🔧 Formatar" para organizar o código

### Preview e Testes

1. **Visualizar Preview**
   - Acesse a aba "👁️ Preview"
   - Clique em "🔄 Atualizar Preview"
   - Veja como a barra ficará

2. **Testar Configuração**
   - Clique em "🚀 Testar Configuração"
   - Verifique se há problemas na configuração

3. **Aplicar no YASB**
   - Salve a configuração com "💾 Salvar Config"
   - Clique em "🔄 Recarregar YASB" para aplicar

## 📁 Estrutura de Arquivos

```
yasb_control_panel/
├── main_enhanced.py          # Aplicação principal
├── widget_dialogs.py         # Diálogos de edição de widgets
├── config_example.yaml       # Exemplo de configuração
├── test_config.py           # Script de testes
├── README.md                # Este arquivo
└── themes/                  # Temas personalizados (criado automaticamente)
```

## 🔧 Tipos de Widgets Suportados

- **ClockWidget** - Relógio com data e hora
- **CpuWidget** - Monitor de CPU
- **MemoryWidget** - Monitor de memória RAM
- **BatteryWidget** - Status da bateria
- **VolumeWidget** - Controle de volume
- **NetworkWidget** - Status da rede
- **ActiveWindowWidget** - Janela ativa
- **WeatherWidget** - Informações do clima
- **DiskWidget** - Uso do disco
- **CustomWidget** - Widget personalizado

## 🎨 Temas Predefinidos

### Tema Escuro (Padrão)
- Fundo: `#1e1e1e`
- Texto: `#ffffff`
- Destaque: `#007acc`
- Borda: `#333333`

### Tema Claro
- Fundo: `#ffffff`
- Texto: `#000000`
- Destaque: `#0078d4`
- Borda: `#cccccc`

### Tema Azul
- Fundo: `#0f1419`
- Texto: `#e6e6e6`
- Destaque: `#00d4ff`
- Borda: `#1e3a5f`

### Tema Verde
- Fundo: `#0d1117`
- Texto: `#c9d1d9`
- Destaque: `#00ff88`
- Borda: `#21262d`

## 🐛 Solução de Problemas

### Erro: "YASB não encontrado"
- Verifique se o YASB está instalado
- Use "📂 Definir Caminho YASB" para configurar manualmente
- Certifique-se de que o diretório contém os arquivos do YASB

### Erro: "Erro ao carregar configuração"
- Verifique se o arquivo YAML está válido
- Use o validador YAML integrado
- Verifique se o arquivo não está sendo usado por outro programa

### Erro: "Falha ao recarregar YASB"
- Certifique-se de que o YASB não está em execução
- Execute o painel como administrador se necessário
- Verifique se o caminho do YASB está correto

### Interface não responde
- Feche e reabra a aplicação
- Verifique se há erros no console
- Certifique-se de que o Python e tkinter estão funcionando

## 📝 Dicas de Uso

1. **Backup da Configuração**
   - Sempre faça backup do seu `config.yaml` antes de fazer mudanças
   - Use "💾 Salvar Config" regularmente

2. **Teste Antes de Aplicar**
   - Use o preview para ver como ficará
   - Teste a configuração antes de recarregar o YASB

3. **Organização de Widgets**
   - Mantenha widgets relacionados na mesma posição
   - Use nomes descritivos para widgets personalizados

4. **Personalização de Estilos**
   - Comece com um tema predefinido
   - Faça ajustes graduais
   - Salve temas personalizados para reutilizar

## 🤝 Contribuição

Este painel foi desenvolvido como uma alternativa desktop ao painel web original. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **Equipe YASB** - Pelo excelente projeto YASB
- **Comunidade Python** - Pelas bibliotecas utilizadas
- **Usuários** - Por feedback e sugestões

---

**Desenvolvido com ❤️ para a comunidade YASB**

*Versão Python do Painel de Controle YASB - Uma alternativa desktop moderna e eficiente*

