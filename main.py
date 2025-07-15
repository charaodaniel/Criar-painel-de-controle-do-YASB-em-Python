#!/usr/bin/env python3
"""
Painel de Controle YASB
Uma interface gráfica para configurar o YASB (Yet Another Status Bar) no Windows.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import yaml
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


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
        
        # Variáveis de configuração
        self.config_data = {}
        self.config_file_path = ""
        
        # Configurar a interface
        self.setup_ui()
        
        # Carregar configuração padrão se existir
        self.load_default_config()
    
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
        
        # Barra de status
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(header_frame, text="🎛️ Painel de Controle YASB", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Botões de ação
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(buttons_frame, text="📁 Abrir Config", 
                  command=self.open_config_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="💾 Salvar Config", 
                  command=self.save_config_file).pack(side=tk.LEFT, padx=(0, 5))
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
                  command=self.toggle_widget).pack(side=tk.LEFT)
        
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
        
        # Botão para aplicar estilos
        ttk.Button(font_frame, text="✅ Aplicar Estilos", 
                  command=self.apply_styles).grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
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
                  command=self.save_yaml_to_file).pack(side=tk.LEFT)
        
        # Configurar redimensionamento
        advanced_frame.columnconfigure(0, weight=1)
        advanced_frame.columnconfigure(1, weight=1)
        advanced_frame.rowconfigure(1, weight=1)
        display_frame.columnconfigure(1, weight=1)
        yaml_frame.columnconfigure(0, weight=1)
        yaml_frame.rowconfigure(0, weight=1)
    
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
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config_data, file, default_flow_style=False, allow_unicode=True)
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
    
    def load_default_config(self):
        """Carrega uma configuração padrão se existir."""
        default_paths = [
            os.path.expanduser("~/.yasb/config.yaml"),
            os.path.expanduser("~/AppData/Roaming/yasb/config.yaml"),
            "./config.yaml"
        ]
        
        for path in default_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        self.config_data = yaml.safe_load(file) or {}
                        self.config_file_path = path
                        self.update_status(f"Configuração padrão carregada: {os.path.basename(path)}")
                        self.refresh_ui()
                        return
                except Exception:
                    continue
        
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
                    "options": {
                        "label": "{%H:%M:%S}",
                        "label_alt": "{%A, %B %d, %Y}",
                        "update_interval": 1000
                    }
                },
                "cpu": {
                    "type": "yasb.cpu.CpuWidget",
                    "options": {
                        "label": "CPU: {cpu_percent}%",
                        "update_interval": 2000
                    }
                },
                "active_window": {
                    "type": "yasb.active_window.ActiveWindowWidget",
                    "options": {
                        "label": "{win_title}",
                        "max_length": 50
                    }
                },
                "battery": {
                    "type": "yasb.battery.BatteryWidget",
                    "options": {
                        "label": "🔋 {battery_percent}%"
                    }
                },
                "volume": {
                    "type": "yasb.volume.VolumeWidget",
                    "options": {
                        "label": "🔊 {volume_percent}%"
                    }
                }
            }
        }
    
    def refresh_ui(self):
        """Atualiza toda a interface com os dados atuais."""
        self.refresh_widgets_tree()
        self.refresh_yaml_editor()
    
    def refresh_widgets_tree(self):
        """Atualiza a árvore de widgets."""
        # Limpar árvore atual
        for item in self.widgets_tree.get_children():
            self.widgets_tree.delete(item)
        
        # Adicionar widgets da configuração
        if 'widgets' in self.config_data:
            for widget_name, widget_config in self.config_data['widgets'].items():
                status = "✅ Ativo" if widget_config.get('enabled', True) else "❌ Inativo"
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
            yaml_content = yaml.dump(self.config_data, default_flow_style=False, allow_unicode=True)
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
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
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
                     font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
            row += 1
            
            for option_name, option_value in widget_config['options'].items():
                ttk.Label(self.properties_frame, text=f"{option_name}:").grid(
                    row=row, column=0, sticky=tk.W, pady=(0, 3))
                ttk.Label(self.properties_frame, text=str(option_value)).grid(
                    row=row, column=1, sticky=tk.W, pady=(0, 3), padx=(10, 0))
                row += 1
    
    def add_widget(self):
        """Adiciona um novo widget."""
        # Implementar diálogo para adicionar widget
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de adicionar widget em desenvolvimento.")
    
    def edit_widget(self):
        """Edita o widget selecionado."""
        selection = self.widgets_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um widget para editar.")
            return
        
        # Implementar diálogo de edição
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
            status = "ativado" if not current_status else "desativado"
            self.update_status(f"Widget '{widget_name}' {status}.")
    
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
    
    def apply_styles(self):
        """Aplica os estilos configurados."""
        # Implementar aplicação de estilos
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de aplicar estilos em desenvolvimento.")
        self.update_status("Estilos aplicados.")
    
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
            self.update_status("Configuração atualizada a partir do YAML.")
        except yaml.YAMLError as e:
            messagebox.showerror("Erro", f"Erro na sintaxe YAML:\n{str(e)}")
    
    def reload_yasb(self):
        """Recarrega o YASB (simulado)."""
        # Em um ambiente real, isso executaria um comando para recarregar o YASB
        messagebox.showinfo("YASB", "Comando de recarga do YASB enviado.")
        self.update_status("YASB recarregado.")
    
    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()


if __name__ == "__main__":
    app = YASBControlPanel()
    app.run()

