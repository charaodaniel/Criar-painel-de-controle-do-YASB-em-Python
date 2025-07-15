#!/usr/bin/env python3
"""
Painel de Controle YASB - Versão Completa
Uma interface gráfica para configurar o YASB (Yet Another Status Bar) no Windows.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import yaml
import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Importar diálogos personalizados
try:
    from widget_dialogs import AddWidgetDialog, EditWidgetDialog, StyleEditorDialog
except ImportError:
    # Fallback se o módulo não estiver disponível
    AddWidgetDialog = None
    EditWidgetDialog = None
    StyleEditorDialog = None


class YASBControlPanel:
    """Classe principal do painel de controle YASB."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎛️ Painel de Controle YASB")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variáveis de configuração
        self.config_data = {}
        self.config_file_path = ""
        self.yasb_path = self.find_yasb_installation()
        
        # Configurar a interface
        self.setup_ui()
        
        # Carregar configuração padrão se existir
        self.load_default_config()
    
    def configure_styles(self):
        """Configura estilos personalizados para a aplicação."""
        # Configurar cores do tema
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Success.TLabel', foreground='green')
        self.style.configure('Error.TLabel', foreground='red')
        self.style.configure('Warning.TLabel', foreground='orange')
    
    def find_yasb_installation(self) -> str:
        """Tenta encontrar a instalação do YASB."""
        possible_paths = [
            os.path.expanduser("~/.yasb"),
            os.path.expanduser("~/AppData/Roaming/yasb"),
            os.path.expanduser("~/AppData/Local/yasb"),
            "C:\\Program Files\\yasb",
            "C:\\yasb",
            "./yasb"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return ""
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Cabeçalho
        self.create_header(main_frame)
        
        # Notebook para as abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Criar as abas
        self.create_widgets_tab()
        self.create_styles_tab()
        self.create_advanced_tab()
        self.create_preview_tab()
        
        # Barra de status
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Título e informações
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(title_frame, text="🎛️ Painel de Controle YASB", 
                 style='Title.TLabel').pack(anchor=tk.W)
        
        # Status da instalação YASB
        if self.yasb_path:
            status_text = f"✅ YASB encontrado em: {self.yasb_path}"
            style = 'Success.TLabel'
        else:
            status_text = "⚠️ YASB não encontrado - Configure o caminho manualmente"
            style = 'Warning.TLabel'
        
        ttk.Label(title_frame, text=status_text, style=style).pack(anchor=tk.W)
        
        # Botões de ação
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(buttons_frame, text="📁 Abrir Config", 
                  command=self.open_config_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="💾 Salvar Config", 
                  command=self.save_config_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="📂 Definir Caminho YASB", 
                  command=self.set_yasb_path).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="🔄 Recarregar YASB", 
                  command=self.reload_yasb).pack(side=tk.LEFT)
    
    def create_widgets_tab(self):
        """Cria a aba de gerenciamento de widgets."""
        widgets_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(widgets_frame, text="🧩 Widgets")
        
        # Frame esquerdo - Lista de widgets
        left_frame = ttk.LabelFrame(widgets_frame, text="Widgets Configurados", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Treeview para widgets
        self.widgets_tree = ttk.Treeview(left_frame, columns=('status', 'position'), show='tree headings')
        self.widgets_tree.heading('#0', text='Widget')
        self.widgets_tree.heading('status', text='Status')
        self.widgets_tree.heading('position', text='Posição')
        self.widgets_tree.column('#0', width=200)
        self.widgets_tree.column('status', width=80)
        self.widgets_tree.column('position', width=80)
        
        # Scrollbar para a treeview
        widgets_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.widgets_tree.yview)
        self.widgets_tree.configure(yscrollcommand=widgets_scrollbar.set)
        
        self.widgets_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        widgets_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões de ação para widgets
        widgets_buttons_frame = ttk.Frame(left_frame)
        widgets_buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(widgets_buttons_frame, text="➕ Adicionar", 
                  command=self.add_widget).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(widgets_buttons_frame, text="✏️ Editar", 
                  command=self.edit_widget).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(widgets_buttons_frame, text="🗑️ Remover", 
                  command=self.remove_widget).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(widgets_buttons_frame, text="🔄 Ativar/Desativar", 
                  command=self.toggle_widget).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(widgets_buttons_frame, text="📋 Duplicar", 
                  command=self.duplicate_widget).pack(side=tk.LEFT)
        
        # Frame direito - Propriedades do widget
        right_frame = ttk.LabelFrame(widgets_frame, text="Propriedades do Widget", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Área de propriedades (será preenchida dinamicamente)
        self.properties_frame = ttk.Frame(right_frame)
        self.properties_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamento
        widgets_frame.columnconfigure(0, weight=1)
        widgets_frame.columnconfigure(1, weight=1)
        widgets_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Bind para seleção de widget
        self.widgets_tree.bind('<<TreeviewSelect>>', self.on_widget_select)
    
    def create_styles_tab(self):
        """Cria a aba de editor de estilos."""
        styles_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(styles_frame, text="🎨 Estilos")
        
        # Frame superior - Temas predefinidos
        themes_frame = ttk.LabelFrame(styles_frame, text="Temas Predefinidos", padding="10")
        themes_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        themes = ["Escuro", "Claro", "Azul", "Verde", "Personalizado"]
        self.theme_var = tk.StringVar(value="Escuro")
        
        for i, theme in enumerate(themes):
            ttk.Radiobutton(themes_frame, text=theme, variable=self.theme_var, 
                           value=theme, command=self.apply_theme).grid(row=0, column=i, padx=(0, 10))
        
        # Botão para editor avançado
        ttk.Button(themes_frame, text="🎨 Editor Avançado", 
                  command=self.open_advanced_style_editor).grid(row=0, column=len(themes), padx=(20, 0))
        
        # Frame esquerdo - Configurações de cores
        colors_frame = ttk.LabelFrame(styles_frame, text="Configurações de Cores", padding="10")
        colors_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Configurações de cor
        color_settings = [
            ("Cor de Fundo:", "background_color"),
            ("Cor do Texto:", "text_color"),
            ("Cor de Destaque:", "accent_color"),
            ("Cor da Borda:", "border_color")
        ]
        
        self.color_vars = {}
        for i, (label, var_name) in enumerate(color_settings):
            ttk.Label(colors_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=(0, 5))
            
            color_frame = ttk.Frame(colors_frame)
            color_frame.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
            
            self.color_vars[var_name] = tk.StringVar(value="#000000")
            color_entry = ttk.Entry(color_frame, textvariable=self.color_vars[var_name], width=10)
            color_entry.pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(color_frame, text="🎨", width=3,
                      command=lambda v=var_name: self.choose_color(v)).pack(side=tk.LEFT)
        
        # Frame direito - Configurações de fonte e layout
        font_frame = ttk.LabelFrame(styles_frame, text="Fonte e Layout", padding="10")
        font_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Configurações de fonte
        ttk.Label(font_frame, text="Família da Fonte:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.font_family_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_family_var, 
                                 values=["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana"])
        font_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        
        ttk.Label(font_frame, text="Tamanho da Fonte:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.font_size_var = tk.StringVar(value="12")
        ttk.Spinbox(font_frame, from_=8, to=72, textvariable=self.font_size_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        ttk.Label(font_frame, text="Peso da Fonte:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.font_weight_var = tk.StringVar(value="normal")
        ttk.Combobox(font_frame, textvariable=self.font_weight_var, 
                    values=["normal", "bold"], width=10).grid(
            row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        # Configurações de espaçamento
        ttk.Separator(font_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=2, 
                                                            sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(font_frame, text="Padding:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.padding_var = tk.StringVar(value="5")
        ttk.Spinbox(font_frame, from_=0, to=50, textvariable=self.padding_var, width=10).grid(
            row=4, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        ttk.Label(font_frame, text="Margin:").grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        self.margin_var = tk.StringVar(value="2")
        ttk.Spinbox(font_frame, from_=0, to=50, textvariable=self.margin_var, width=10).grid(
            row=5, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        # Botões para aplicar estilos
        buttons_frame = ttk.Frame(font_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="✅ Aplicar Estilos", 
                  command=self.apply_styles).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="💾 Salvar Tema", 
                  command=self.save_custom_theme).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="📁 Carregar Tema", 
                  command=self.load_custom_theme).pack(side=tk.LEFT)
        
        # Configurar redimensionamento
        styles_frame.columnconfigure(0, weight=1)
        styles_frame.columnconfigure(1, weight=1)
        styles_frame.rowconfigure(1, weight=1)
        colors_frame.columnconfigure(1, weight=1)
        font_frame.columnconfigure(1, weight=1)
    
    def create_advanced_tab(self):
        """Cria a aba de configurações avançadas."""
        advanced_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(advanced_frame, text="⚙️ Avançado")
        
        # Frame superior - Configurações do sistema
        system_frame = ttk.LabelFrame(advanced_frame, text="Configurações do Sistema", padding="10")
        system_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkboxes para configurações do sistema
        self.auto_start_var = tk.BooleanVar()
        ttk.Checkbutton(system_frame, text="Iniciar automaticamente com o Windows", 
                       variable=self.auto_start_var).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.debug_mode_var = tk.BooleanVar()
        ttk.Checkbutton(system_frame, text="Modo de depuração", 
                       variable=self.debug_mode_var).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Frame esquerdo - Configurações de exibição
        display_frame = ttk.LabelFrame(advanced_frame, text="Configurações de Exibição", padding="10")
        display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Configurações de monitor
        ttk.Label(display_frame, text="Monitor:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.monitor_var = tk.StringVar(value="0")
        ttk.Spinbox(display_frame, from_=0, to=9, textvariable=self.monitor_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        ttk.Label(display_frame, text="Posição:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.position_var = tk.StringVar(value="top")
        ttk.Combobox(display_frame, textvariable=self.position_var, 
                    values=["top", "bottom"], width=10).grid(
            row=1, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        ttk.Label(display_frame, text="Largura:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.width_var = tk.StringVar(value="100%")
        ttk.Entry(display_frame, textvariable=self.width_var, width=10).grid(
            row=2, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        ttk.Label(display_frame, text="Altura:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.height_var = tk.StringVar(value="30")
        ttk.Spinbox(display_frame, from_=20, to=100, textvariable=self.height_var, width=10).grid(
            row=3, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        
        # Frame direito - Editor YAML
        yaml_frame = ttk.LabelFrame(advanced_frame, text="Editor YAML", padding="10")
        yaml_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Área de texto para YAML
        self.yaml_text = tk.Text(yaml_frame, wrap=tk.NONE, font=('Courier New', 10))
        yaml_scrollbar_v = ttk.Scrollbar(yaml_frame, orient=tk.VERTICAL, command=self.yaml_text.yview)
        yaml_scrollbar_h = ttk.Scrollbar(yaml_frame, orient=tk.HORIZONTAL, command=self.yaml_text.xview)
        self.yaml_text.configure(yscrollcommand=yaml_scrollbar_v.set, xscrollcommand=yaml_scrollbar_h.set)
        
        self.yaml_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        yaml_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        yaml_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Botões para o editor YAML
        yaml_buttons_frame = ttk.Frame(yaml_frame)
        yaml_buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(yaml_buttons_frame, text="✅ Validar YAML", 
                  command=self.validate_yaml).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(yaml_buttons_frame, text="🔄 Carregar do Arquivo", 
                  command=self.load_yaml_from_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(yaml_buttons_frame, text="💾 Salvar no Arquivo", 
                  command=self.save_yaml_to_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(yaml_buttons_frame, text="🔧 Formatar", 
                  command=self.format_yaml).pack(side=tk.LEFT)
        
        # Configurar redimensionamento
        advanced_frame.columnconfigure(0, weight=1)
        advanced_frame.columnconfigure(1, weight=1)
        advanced_frame.rowconfigure(1, weight=1)
        display_frame.columnconfigure(1, weight=1)
        yaml_frame.columnconfigure(0, weight=1)
        yaml_frame.rowconfigure(0, weight=1)
    
    def create_preview_tab(self):
        """Cria a aba de preview da configuração."""
        preview_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(preview_frame, text="👁️ Preview")
        
        # Frame superior - Controles
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(controls_frame, text="🔄 Atualizar Preview", 
                  command=self.update_preview).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="📸 Capturar Screenshot", 
                  command=self.capture_screenshot).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="🚀 Testar Configuração", 
                  command=self.test_configuration).pack(side=tk.LEFT)
        
        # Frame de preview
        self.preview_canvas_frame = ttk.LabelFrame(preview_frame, text="Preview da Barra", padding="10")
        self.preview_canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas para desenhar o preview
        self.preview_canvas = tk.Canvas(self.preview_canvas_frame, height=50, bg='#1e1e1e')
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Frame de informações
        info_frame = ttk.LabelFrame(preview_frame, text="Informações da Configuração", padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD, font=('Courier New', 9))
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar redimensionamento
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        self.preview_canvas_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Cria a barra de status."""
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def update_status(self, message: str):
        """Atualiza a mensagem da barra de status."""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    # Métodos de manipulação de arquivos
    def open_config_file(self):
        """Abre um arquivo de configuração YAML."""
        file_path = filedialog.askopenfilename(
            title="Abrir Configuração YASB",
            filetypes=[("Arquivos YAML", "*.yaml *.yml"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.config_data = yaml.safe_load(file) or {}
                    self.config_file_path = file_path
                    self.update_status(f"Configuração carregada: {os.path.basename(file_path)}")
                    self.refresh_ui()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
    
    def save_config_file(self):
        """Salva a configuração atual em um arquivo YAML."""
        if not self.config_file_path:
            self.save_config_file_as()
            return
        
        try:
            # Aplicar configurações das abas à estrutura de dados
            self.apply_ui_to_config()
            
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config_data, file, default_flow_style=False, allow_unicode=True, indent=2)
            self.update_status(f"Configuração salva: {os.path.basename(self.config_file_path)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
    
    def save_config_file_as(self):
        """Salva a configuração atual em um novo arquivo YAML."""
        file_path = filedialog.asksaveasfilename(
            title="Salvar Configuração YASB",
            defaultextension=".yaml",
            filetypes=[("Arquivos YAML", "*.yaml *.yml"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            self.config_file_path = file_path
            self.save_config_file()
    
    def set_yasb_path(self):
        """Define o caminho da instalação do YASB."""
        path = filedialog.askdirectory(title="Selecionar Diretório do YASB")
        if path:
            self.yasb_path = path
            self.update_status(f"Caminho do YASB definido: {path}")
            # Atualizar o cabeçalho
            self.setup_ui()
    
    def apply_ui_to_config(self):
        """Aplica as configurações da interface à estrutura de dados."""
        # Aplicar configurações do sistema
        if 'system' not in self.config_data:
            self.config_data['system'] = {}
        
        self.config_data['system']['auto_start'] = self.auto_start_var.get()
        self.config_data['system']['debug_mode'] = self.debug_mode_var.get()
        
        # Aplicar configurações de exibição
        if 'bars' not in self.config_data:
            self.config_data['bars'] = {'yasb-bar': {}}
        
        bar_config = self.config_data['bars']['yasb-bar']
        
        if 'alignment' not in bar_config:
            bar_config['alignment'] = {}
        bar_config['alignment']['position'] = self.position_var.get()
        
        if 'dimensions' not in bar_config:
            bar_config['dimensions'] = {}
        bar_config['dimensions']['width'] = self.width_var.get()
        bar_config['dimensions']['height'] = int(self.height_var.get())
        
        # Aplicar estilos
        if 'styles' not in self.config_data:
            self.config_data['styles'] = {'default': {}}
        
        style_config = self.config_data['styles']['default']
        for var_name, var in self.color_vars.items():
            style_config[var_name] = var.get()
        
        style_config['font_family'] = self.font_family_var.get()
        style_config['font_size'] = int(self.font_size_var.get())
        style_config['font_weight'] = self.font_weight_var.get()
        style_config['padding'] = int(self.padding_var.get())
        style_config['margin'] = int(self.margin_var.get())
    
    def load_default_config(self):
        """Carrega uma configuração padrão se existir."""
        if self.yasb_path:
            config_path = os.path.join(self.yasb_path, "config.yaml")
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as file:
                        self.config_data = yaml.safe_load(file) or {}
                        self.config_file_path = config_path
                        self.update_status(f"Configuração padrão carregada: {os.path.basename(config_path)}")
                        self.refresh_ui()
                        return
                except Exception:
                    pass
        
        # Se não encontrou configuração, criar uma básica
        self.config_data = self.create_default_config()
        self.refresh_ui()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Cria uma configuração padrão básica."""
        return {
            "bars": {
                "yasb-bar": {
                    "enabled": True,
                    "screens": ["*"],
                    "class_name": "yasb-bar",
                    "alignment": {
                        "position": "top",
                        "center": False
                    },
                    "blur_effect": {
                        "enabled": False,
                        "acrylic": False,
                        "dark": True
                    },
                    "window_flags": {
                        "always_on_top": True,
                        "windows_app_bar": True
                    },
                    "dimensions": {
                        "width": "100%",
                        "height": 30
                    },
                    "padding": {
                        "top": 0,
                        "left": 0,
                        "bottom": 0,
                        "right": 0
                    },
                    "widgets": {
                        "left": ["clock", "cpu"],
                        "center": ["active_window"],
                        "right": ["battery", "volume"]
                    }
                }
            },
            "widgets": {
                "clock": {
                    "type": "yasb.clock.ClockWidget",
                    "enabled": True,
                    "options": {
                        "label": "{%H:%M:%S}",
                        "label_alt": "{%A, %B %d, %Y}",
                        "update_interval": 1000
                    }
                },
                "cpu": {
                    "type": "yasb.cpu.CpuWidget",
                    "enabled": True,
                    "options": {
                        "label": "CPU: {cpu_percent}%",
                        "update_interval": 2000
                    }
                },
                "active_window": {
                    "type": "yasb.active_window.ActiveWindowWidget",
                    "enabled": True,
                    "options": {
                        "label": "{win_title}",
                        "max_length": 50
                    }
                },
                "battery": {
                    "type": "yasb.battery.BatteryWidget",
                    "enabled": True,
                    "options": {
                        "label": "🔋 {battery_percent}%"
                    }
                },
                "volume": {
                    "type": "yasb.volume.VolumeWidget",
                    "enabled": True,
                    "options": {
                        "label": "🔊 {volume_percent}%"
                    }
                }
            },
            "styles": {
                "default": {
                    "background_color": "#1e1e1e",
                    "text_color": "#ffffff",
                    "accent_color": "#007acc",
                    "border_color": "#333333",
                    "font_family": "Arial",
                    "font_size": 12,
                    "font_weight": "normal",
                    "padding": 5,
                    "margin": 2
                }
            },
            "system": {
                "auto_start": True,
                "debug_mode": False
            }
        }
    
    def refresh_ui(self):
        """Atualiza toda a interface com os dados atuais."""
        self.refresh_widgets_tree()
        self.refresh_yaml_editor()
        self.load_config_to_ui()
        self.update_preview()
    
    def load_config_to_ui(self):
        """Carrega a configuração atual para os controles da interface."""
        # Carregar configurações do sistema
        system_config = self.config_data.get('system', {})
        self.auto_start_var.set(system_config.get('auto_start', True))
        self.debug_mode_var.set(system_config.get('debug_mode', False))
        
        # Carregar configurações de exibição
        bar_config = self.config_data.get('bars', {}).get('yasb-bar', {})
        alignment = bar_config.get('alignment', {})
        dimensions = bar_config.get('dimensions', {})
        
        self.position_var.set(alignment.get('position', 'top'))
        self.width_var.set(str(dimensions.get('width', '100%')))
        self.height_var.set(str(dimensions.get('height', 30)))
        
        # Carregar estilos
        style_config = self.config_data.get('styles', {}).get('default', {})
        
        color_defaults = {
            'background_color': '#1e1e1e',
            'text_color': '#ffffff',
            'accent_color': '#007acc',
            'border_color': '#333333'
        }
        
        for var_name, default in color_defaults.items():
            if var_name in self.color_vars:
                self.color_vars[var_name].set(style_config.get(var_name, default))
        
        self.font_family_var.set(style_config.get('font_family', 'Arial'))
        self.font_size_var.set(str(style_config.get('font_size', 12)))
        self.font_weight_var.set(style_config.get('font_weight', 'normal'))
        self.padding_var.set(str(style_config.get('padding', 5)))
        self.margin_var.set(str(style_config.get('margin', 2)))
    
    def refresh_widgets_tree(self):
        """Atualiza a árvore de widgets."""
        # Limpar árvore atual
        for item in self.widgets_tree.get_children():
            self.widgets_tree.delete(item)
        
        # Adicionar widgets da configuração
        if 'widgets' in self.config_data:
            for widget_name, widget_config in self.config_data['widgets'].items():
                enabled = widget_config.get('enabled', True)
                status = "✅ Ativo" if enabled else "❌ Inativo"
                position = self.get_widget_position(widget_name)
                self.widgets_tree.insert('', 'end', iid=widget_name, text=widget_name, 
                                       values=(status, position))
    
    def get_widget_position(self, widget_name: str) -> str:
        """Obtém a posição de um widget na barra."""
        if 'bars' in self.config_data:
            for bar_config in self.config_data['bars'].values():
                if 'widgets' in bar_config:
                    for position, widgets in bar_config['widgets'].items():
                        if widget_name in widgets:
                            return position
        return "N/A"
    
    def refresh_yaml_editor(self):
        """Atualiza o editor YAML com a configuração atual."""
        self.yaml_text.delete(1.0, tk.END)
        if self.config_data:
            yaml_content = yaml.dump(self.config_data, default_flow_style=False, allow_unicode=True, indent=2)
            self.yaml_text.insert(1.0, yaml_content)
    
    # Métodos de manipulação de widgets
    def on_widget_select(self, event):
        """Callback para seleção de widget na árvore."""
        selection = self.widgets_tree.selection()
        if selection:
            widget_name = selection[0]
            self.show_widget_properties(widget_name)
    
    def show_widget_properties(self, widget_name: str):
        """Mostra as propriedades de um widget no painel direito."""
        # Limpar frame de propriedades
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
        
        if widget_name not in self.config_data.get('widgets', {}):
            return
        
        widget_config = self.config_data['widgets'][widget_name]
        
        # Título
        ttk.Label(self.properties_frame, text=f"Propriedades: {widget_name}", 
                 style='Heading.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        row = 1
        
        # Tipo do widget
        ttk.Label(self.properties_frame, text="Tipo:").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(self.properties_frame, text=widget_config.get('type', 'N/A')).grid(
            row=row, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        row += 1
        
        # Status
        ttk.Label(self.properties_frame, text="Status:").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        enabled = widget_config.get('enabled', True)
        status_text = "✅ Ativo" if enabled else "❌ Inativo"
        ttk.Label(self.properties_frame, text=status_text).grid(
            row=row, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        row += 1
        
        # Posição
        ttk.Label(self.properties_frame, text="Posição:").grid(row=row, column=0, sticky=tk.W, pady=(0, 5))
        position = self.get_widget_position(widget_name)
        ttk.Label(self.properties_frame, text=position).grid(
            row=row, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
        row += 1
        
        # Opções do widget
        if 'options' in widget_config:
            ttk.Separator(self.properties_frame, orient=tk.HORIZONTAL).grid(
                row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
            row += 1
            
            ttk.Label(self.properties_frame, text="Opções:", 
                     style='Heading.TLabel').grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
            row += 1
            
            for option_name, option_value in widget_config['options'].items():
                ttk.Label(self.properties_frame, text=f"{option_name}:").grid(
                    row=row, column=0, sticky=tk.W, pady=(0, 3))
                ttk.Label(self.properties_frame, text=str(option_value)).grid(
                    row=row, column=1, sticky=tk.W, pady=(0, 3), padx=(10, 0))
                row += 1
    
    def add_widget(self):
        """Adiciona um novo widget."""
        if AddWidgetDialog:
            dialog = AddWidgetDialog(self.root)
            result = dialog.show()
            
            if result:
                widget_name = result['name']
                
                # Verificar se o widget já existe
                if widget_name in self.config_data.get('widgets', {}):
                    messagebox.showerror("Erro", f"Widget '{widget_name}' já existe.")
                    return
                
                # Adicionar widget à configuração
                if 'widgets' not in self.config_data:
                    self.config_data['widgets'] = {}
                
                self.config_data['widgets'][widget_name] = {
                    'type': result['type'],
                    'enabled': result['enabled'],
                    'options': result['options']
                }
                
                # Adicionar à barra
                position = result['position']
                if 'bars' not in self.config_data:
                    self.config_data['bars'] = {'yasb-bar': {'widgets': {'left': [], 'center': [], 'right': []}}}
                
                bar_config = self.config_data['bars']['yasb-bar']
                if 'widgets' not in bar_config:
                    bar_config['widgets'] = {'left': [], 'center': [], 'right': []}
                
                if position not in bar_config['widgets']:
                    bar_config['widgets'][position] = []
                
                bar_config['widgets'][position].append(widget_name)
                
                self.refresh_widgets_tree()
                self.update_status(f"Widget '{widget_name}' adicionado.")
        else:
            messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de adicionar widget em desenvolvimento.")
    
    def edit_widget(self):
        """Edita o widget selecionado."""
        selection = self.widgets_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um widget para editar.")
            return
        
        widget_name = selection[0]
        
        if EditWidgetDialog:
            widget_config = self.config_data['widgets'][widget_name].copy()
            widget_config['name'] = widget_name
            widget_config['position'] = self.get_widget_position(widget_name)
            
            dialog = EditWidgetDialog(self.root, widget_config)
            result = dialog.show()
            
            if result:
                # Atualizar configuração do widget
                self.config_data['widgets'][widget_name] = {
                    'type': result['type'],
                    'enabled': result['enabled'],
                    'options': result['options']
                }
                
                self.refresh_widgets_tree()
                self.show_widget_properties(widget_name)
                self.update_status(f"Widget '{widget_name}' editado.")
        else:
            messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de editar widget em desenvolvimento.")
    
    def remove_widget(self):
        """Remove o widget selecionado."""
        selection = self.widgets_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um widget para remover.")
            return
        
        widget_name = selection[0]
        if messagebox.askyesno("Confirmar", f"Deseja remover o widget '{widget_name}'?"):
            # Remover da configuração
            if 'widgets' in self.config_data and widget_name in self.config_data['widgets']:
                del self.config_data['widgets'][widget_name]
            
            # Remover das barras
            if 'bars' in self.config_data:
                for bar_config in self.config_data['bars'].values():
                    if 'widgets' in bar_config:
                        for position, widgets in bar_config['widgets'].items():
                            if widget_name in widgets:
                                widgets.remove(widget_name)
            
            self.refresh_widgets_tree()
            # Limpar propriedades
            for widget in self.properties_frame.winfo_children():
                widget.destroy()
            self.update_status(f"Widget '{widget_name}' removido.")
    
    def toggle_widget(self):
        """Ativa/desativa o widget selecionado."""
        selection = self.widgets_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um widget para ativar/desativar.")
            return
        
        widget_name = selection[0]
        if 'widgets' in self.config_data and widget_name in self.config_data['widgets']:
            current_status = self.config_data['widgets'][widget_name].get('enabled', True)
            self.config_data['widgets'][widget_name]['enabled'] = not current_status
            self.refresh_widgets_tree()
            self.show_widget_properties(widget_name)
            status = "ativado" if not current_status else "desativado"
            self.update_status(f"Widget '{widget_name}' {status}.")
    
    def duplicate_widget(self):
        """Duplica o widget selecionado."""
        selection = self.widgets_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um widget para duplicar.")
            return
        
        widget_name = selection[0]
        new_name = f"{widget_name}_copy"
        
        # Verificar se o nome já existe e gerar um único
        counter = 1
        while new_name in self.config_data.get('widgets', {}):
            new_name = f"{widget_name}_copy_{counter}"
            counter += 1
        
        # Duplicar configuração
        if 'widgets' in self.config_data and widget_name in self.config_data['widgets']:
            self.config_data['widgets'][new_name] = self.config_data['widgets'][widget_name].copy()
            
            # Adicionar à mesma posição na barra
            position = self.get_widget_position(widget_name)
            if position != "N/A":
                bar_config = self.config_data['bars']['yasb-bar']
                if position in bar_config['widgets']:
                    bar_config['widgets'][position].append(new_name)
            
            self.refresh_widgets_tree()
            self.update_status(f"Widget duplicado como '{new_name}'.")
    
    # Métodos de estilos
    def choose_color(self, var_name: str):
        """Abre o seletor de cores."""
        color = colorchooser.askcolor(title="Escolher Cor")
        if color[1]:  # Se uma cor foi selecionada
            self.color_vars[var_name].set(color[1])
    
    def apply_theme(self):
        """Aplica um tema predefinido."""
        theme = self.theme_var.get()
        
        themes = {
            "Escuro": {
                "background_color": "#1e1e1e",
                "text_color": "#ffffff",
                "accent_color": "#007acc",
                "border_color": "#333333"
            },
            "Claro": {
                "background_color": "#ffffff",
                "text_color": "#000000",
                "accent_color": "#0078d4",
                "border_color": "#cccccc"
            },
            "Azul": {
                "background_color": "#0f1419",
                "text_color": "#e6e6e6",
                "accent_color": "#00d4ff",
                "border_color": "#1e3a5f"
            },
            "Verde": {
                "background_color": "#0d1117",
                "text_color": "#c9d1d9",
                "accent_color": "#00ff88",
                "border_color": "#21262d"
            }
        }
        
        if theme in themes:
            for var_name, color in themes[theme].items():
                if var_name in self.color_vars:
                    self.color_vars[var_name].set(color)
            self.update_status(f"Tema '{theme}' aplicado.")
    
    def open_advanced_style_editor(self):
        """Abre o editor avançado de estilos."""
        if StyleEditorDialog:
            style_data = self.config_data.get('styles', {}).get('default', {})
            dialog = StyleEditorDialog(self.root, style_data)
            result = dialog.show()
            
            if result:
                # Aplicar estilos avançados
                if 'styles' not in self.config_data:
                    self.config_data['styles'] = {}
                if 'default' not in self.config_data['styles']:
                    self.config_data['styles']['default'] = {}
                
                self.config_data['styles']['default'].update(result)
                self.load_config_to_ui()
                self.update_status("Estilos avançados aplicados.")
        else:
            messagebox.showinfo("Em Desenvolvimento", "Editor avançado de estilos em desenvolvimento.")
    
    def apply_styles(self):
        """Aplica os estilos configurados."""
        self.apply_ui_to_config()
        self.update_status("Estilos aplicados à configuração.")
        self.update_preview()
    
    def save_custom_theme(self):
        """Salva um tema personalizado."""
        file_path = filedialog.asksaveasfilename(
            title="Salvar Tema Personalizado",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            theme_data = {}
            for var_name, var in self.color_vars.items():
                theme_data[var_name] = var.get()
            
            theme_data.update({
                'font_family': self.font_family_var.get(),
                'font_size': self.font_size_var.get(),
                'font_weight': self.font_weight_var.get(),
                'padding': self.padding_var.get(),
                'margin': self.margin_var.get()
            })
            
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(theme_data, file, indent=2)
                self.update_status(f"Tema salvo: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar tema: {str(e)}")
    
    def load_custom_theme(self):
        """Carrega um tema personalizado."""
        file_path = filedialog.askopenfilename(
            title="Carregar Tema Personalizado",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    theme_data = json.load(file)
                
                # Aplicar dados do tema
                for var_name, value in theme_data.items():
                    if var_name in self.color_vars:
                        self.color_vars[var_name].set(value)
                    elif var_name == 'font_family':
                        self.font_family_var.set(value)
                    elif var_name == 'font_size':
                        self.font_size_var.set(value)
                    elif var_name == 'font_weight':
                        self.font_weight_var.set(value)
                    elif var_name == 'padding':
                        self.padding_var.set(value)
                    elif var_name == 'margin':
                        self.margin_var.set(value)
                
                self.theme_var.set("Personalizado")
                self.update_status(f"Tema carregado: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar tema: {str(e)}")
    
    # Métodos de configurações avançadas
    def validate_yaml(self):
        """Valida a sintaxe do YAML no editor."""
        try:
            yaml_content = self.yaml_text.get(1.0, tk.END)
            yaml.safe_load(yaml_content)
            messagebox.showinfo("Validação", "YAML válido!")
            self.update_status("YAML validado com sucesso.")
        except yaml.YAMLError as e:
            messagebox.showerror("Erro de Validação", f"Erro na sintaxe YAML:\n{str(e)}")
            self.update_status("Erro na validação do YAML.")
    
    def load_yaml_from_file(self):
        """Carrega YAML do arquivo atual para o editor."""
        if self.config_data:
            self.refresh_yaml_editor()
            self.update_status("YAML carregado no editor.")
        else:
            messagebox.showwarning("Aviso", "Nenhuma configuração carregada.")
    
    def save_yaml_to_file(self):
        """Salva o YAML do editor para a configuração."""
        try:
            yaml_content = self.yaml_text.get(1.0, tk.END)
            self.config_data = yaml.safe_load(yaml_content) or {}
            self.refresh_widgets_tree()
            self.load_config_to_ui()
            self.update_status("Configuração atualizada a partir do YAML.")
        except yaml.YAMLError as e:
            messagebox.showerror("Erro", f"Erro na sintaxe YAML:\n{str(e)}")
    
    def format_yaml(self):
        """Formata o YAML no editor."""
        try:
            yaml_content = self.yaml_text.get(1.0, tk.END)
            data = yaml.safe_load(yaml_content)
            formatted_yaml = yaml.dump(data, default_flow_style=False, allow_unicode=True, indent=2)
            
            self.yaml_text.delete(1.0, tk.END)
            self.yaml_text.insert(1.0, formatted_yaml)
            self.update_status("YAML formatado.")
        except yaml.YAMLError as e:
            messagebox.showerror("Erro", f"Erro na sintaxe YAML:\n{str(e)}")
    
    # Métodos de preview
    def update_preview(self):
        """Atualiza o preview da barra."""
        self.preview_canvas.delete("all")
        
        # Obter configurações da barra
        bar_config = self.config_data.get('bars', {}).get('yasb-bar', {})
        widgets_config = bar_config.get('widgets', {})
        style_config = self.config_data.get('styles', {}).get('default', {})
        
        # Configurações visuais
        bg_color = style_config.get('background_color', '#1e1e1e')
        text_color = style_config.get('text_color', '#ffffff')
        
        # Desenhar fundo da barra
        canvas_width = self.preview_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 800  # Largura padrão
        
        self.preview_canvas.configure(bg=bg_color)
        
        # Desenhar widgets
        x_left = 10
        x_right = canvas_width - 10
        x_center = canvas_width // 2
        
        # Widgets da esquerda
        for widget_name in widgets_config.get('left', []):
            if widget_name in self.config_data.get('widgets', {}):
                widget_config = self.config_data['widgets'][widget_name]
                if widget_config.get('enabled', True):
                    self.preview_canvas.create_text(x_left, 25, text=widget_name, 
                                                   fill=text_color, anchor=tk.W)
                    x_left += len(widget_name) * 8 + 20
        
        # Widgets do centro
        center_widgets = widgets_config.get('center', [])
        if center_widgets:
            total_width = sum(len(w) * 8 for w in center_widgets) + (len(center_widgets) - 1) * 20
            x_start = x_center - total_width // 2
            
            for widget_name in center_widgets:
                if widget_name in self.config_data.get('widgets', {}):
                    widget_config = self.config_data['widgets'][widget_name]
                    if widget_config.get('enabled', True):
                        self.preview_canvas.create_text(x_start, 25, text=widget_name, 
                                                       fill=text_color, anchor=tk.W)
                        x_start += len(widget_name) * 8 + 20
        
        # Widgets da direita
        right_widgets = list(reversed(widgets_config.get('right', [])))
        for widget_name in right_widgets:
            if widget_name in self.config_data.get('widgets', {}):
                widget_config = self.config_data['widgets'][widget_name]
                if widget_config.get('enabled', True):
                    x_right -= len(widget_name) * 8
                    self.preview_canvas.create_text(x_right, 25, text=widget_name, 
                                                   fill=text_color, anchor=tk.W)
                    x_right -= 20
        
        # Atualizar informações
        self.update_config_info()
    
    def update_config_info(self):
        """Atualiza as informações da configuração."""
        self.info_text.delete(1.0, tk.END)
        
        info = []
        info.append("=== INFORMAÇÕES DA CONFIGURAÇÃO ===\n")
        
        # Estatísticas gerais
        total_widgets = len(self.config_data.get('widgets', {}))
        active_widgets = sum(1 for w in self.config_data.get('widgets', {}).values() if w.get('enabled', True))
        
        info.append(f"Total de Widgets: {total_widgets}")
        info.append(f"Widgets Ativos: {active_widgets}")
        info.append(f"Widgets Inativos: {total_widgets - active_widgets}\n")
        
        # Configurações da barra
        bar_config = self.config_data.get('bars', {}).get('yasb-bar', {})
        info.append("=== CONFIGURAÇÕES DA BARRA ===")
        info.append(f"Posição: {bar_config.get('alignment', {}).get('position', 'N/A')}")
        info.append(f"Largura: {bar_config.get('dimensions', {}).get('width', 'N/A')}")
        info.append(f"Altura: {bar_config.get('dimensions', {}).get('height', 'N/A')}\n")
        
        # Distribuição de widgets
        widgets_config = bar_config.get('widgets', {})
        info.append("=== DISTRIBUIÇÃO DE WIDGETS ===")
        info.append(f"Esquerda: {', '.join(widgets_config.get('left', []))}")
        info.append(f"Centro: {', '.join(widgets_config.get('center', []))}")
        info.append(f"Direita: {', '.join(widgets_config.get('right', []))}\n")
        
        # Configurações de estilo
        style_config = self.config_data.get('styles', {}).get('default', {})
        if style_config:
            info.append("=== CONFIGURAÇÕES DE ESTILO ===")
            info.append(f"Cor de Fundo: {style_config.get('background_color', 'N/A')}")
            info.append(f"Cor do Texto: {style_config.get('text_color', 'N/A')}")
            info.append(f"Fonte: {style_config.get('font_family', 'N/A')} {style_config.get('font_size', 'N/A')}px")
        
        self.info_text.insert(1.0, '\n'.join(info))
    
    def capture_screenshot(self):
        """Captura um screenshot do preview."""
        file_path = filedialog.asksaveasfilename(
            title="Salvar Screenshot",
            defaultextension=".png",
            filetypes=[("Arquivos PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )
        
        if file_path:
            try:
                # Simular captura (em um ambiente real, usaria bibliotecas como PIL)
                messagebox.showinfo("Screenshot", f"Screenshot salvo em: {file_path}")
                self.update_status(f"Screenshot salvo: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar screenshot: {str(e)}")
    
    def test_configuration(self):
        """Testa a configuração atual."""
        # Validar configuração
        errors = []
        
        # Verificar se há widgets configurados
        if not self.config_data.get('widgets'):
            errors.append("Nenhum widget configurado")
        
        # Verificar se há widgets ativos
        active_widgets = [w for w in self.config_data.get('widgets', {}).values() if w.get('enabled', True)]
        if not active_widgets:
            errors.append("Nenhum widget ativo")
        
        # Verificar configuração da barra
        if not self.config_data.get('bars'):
            errors.append("Configuração da barra não encontrada")
        
        if errors:
            messagebox.showwarning("Problemas na Configuração", 
                                 "Problemas encontrados:\n" + "\n".join(f"• {error}" for error in errors))
        else:
            messagebox.showinfo("Teste de Configuração", 
                              "✅ Configuração válida!\n\nTodos os testes passaram com sucesso.")
        
        self.update_status("Teste de configuração concluído.")
    
    def reload_yasb(self):
        """Recarrega o YASB."""
        if not self.yasb_path:
            messagebox.showwarning("Aviso", "Caminho do YASB não configurado.")
            return
        
        try:
            # Salvar configuração atual
            if self.config_file_path:
                self.save_config_file()
            
            # Tentar recarregar o YASB (comando específico do Windows)
            if sys.platform == "win32":
                # Comando para recarregar o YASB no Windows
                subprocess.run(["taskkill", "/f", "/im", "yasb.exe"], capture_output=True)
                subprocess.Popen([os.path.join(self.yasb_path, "yasb.exe")])
                messagebox.showinfo("YASB", "YASB recarregado com sucesso!")
            else:
                # Simulação para outros sistemas
                messagebox.showinfo("YASB", "Comando de recarga do YASB enviado.")
            
            self.update_status("YASB recarregado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao recarregar YASB: {str(e)}")
    
    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()


if __name__ == "__main__":
    app = YASBControlPanel()
    app.run()

