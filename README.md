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

