"""
Módulo para diálogos de edição e criação de widgets.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List


class WidgetDialog:
    """Diálogo base para edição de widgets."""
    
    def __init__(self, parent, title: str, widget_data: Optional[Dict[str, Any]] = None):
        self.parent = parent
        self.result = None
        self.widget_data = widget_data or {}
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.center_window()
        
        # Configurar interface
        self.setup_ui()
        
        # Carregar dados se fornecidos
        if self.widget_data:
            self.load_data()
    
    def center_window(self):
        """Centraliza a janela na tela."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome do widget
        ttk.Label(main_frame, text="Nome do Widget:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        
        # Tipo do widget
        ttk.Label(main_frame, text="Tipo do Widget:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, width=37)
        self.type_combo['values'] = self.get_widget_types()
        self.type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        self.type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Status
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Widget Ativo", variable=self.enabled_var).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Posição na barra
        ttk.Label(main_frame, text="Posição na Barra:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.position_var = tk.StringVar(value="left")
        position_frame = ttk.Frame(main_frame)
        position_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        
        for pos in ["left", "center", "right"]:
            ttk.Radiobutton(position_frame, text=pos.capitalize(), variable=self.position_var, 
                           value=pos).pack(side=tk.LEFT, padx=(0, 10))
        
        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Opções do widget
        ttk.Label(main_frame, text="Opções do Widget:", 
                 font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Frame para opções (será preenchido dinamicamente)
        self.options_frame = ttk.Frame(main_frame)
        self.options_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="OK", command=self.ok).pack(side=tk.RIGHT)
        
        # Configurar redimensionamento
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.options_frame.columnconfigure(1, weight=1)
    
    def get_widget_types(self) -> List[str]:
        """Retorna a lista de tipos de widgets disponíveis."""
        return [
            "yasb.clock.ClockWidget",
            "yasb.cpu.CpuWidget",
            "yasb.memory.MemoryWidget",
            "yasb.battery.BatteryWidget",
            "yasb.volume.VolumeWidget",
            "yasb.network.NetworkWidget",
            "yasb.active_window.ActiveWindowWidget",
            "yasb.weather.WeatherWidget",
            "yasb.disk.DiskWidget",
            "yasb.custom.CustomWidget"
        ]
    
    def on_type_change(self, event=None):
        """Callback para mudança de tipo de widget."""
        self.update_options_ui()
    
    def update_options_ui(self):
        """Atualiza a interface de opções baseada no tipo de widget."""
        # Limpar opções atuais
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        widget_type = self.type_var.get()
        self.option_vars = {}
        
        # Definir opções baseadas no tipo
        options_config = self.get_options_for_type(widget_type)
        
        row = 0
        for option_name, option_config in options_config.items():
            ttk.Label(self.options_frame, text=f"{option_name}:").grid(
                row=row, column=0, sticky=tk.W, pady=(0, 5))
            
            option_type = option_config.get('type', 'string')
            default_value = option_config.get('default', '')
            
            if option_type == 'boolean':
                var = tk.BooleanVar(value=default_value)
                ttk.Checkbutton(self.options_frame, variable=var).grid(
                    row=row, column=1, sticky=tk.W, pady=(0, 5), padx=(10, 0))
            elif option_type == 'integer':
                var = tk.StringVar(value=str(default_value))
                ttk.Spinbox(self.options_frame, textvariable=var, from_=0, to=10000, width=20).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
            elif option_type == 'choice':
                var = tk.StringVar(value=default_value)
                combo = ttk.Combobox(self.options_frame, textvariable=var, width=17)
                combo['values'] = option_config.get('choices', [])
                combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
            else:  # string
                var = tk.StringVar(value=default_value)
                ttk.Entry(self.options_frame, textvariable=var, width=20).grid(
                    row=row, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
            
            self.option_vars[option_name] = var
            row += 1
    
    def get_options_for_type(self, widget_type: str) -> Dict[str, Dict[str, Any]]:
        """Retorna as opções disponíveis para um tipo de widget."""
        options_map = {
            "yasb.clock.ClockWidget": {
                "label": {"type": "string", "default": "{%H:%M:%S}"},
                "label_alt": {"type": "string", "default": "{%A, %B %d, %Y}"},
                "update_interval": {"type": "integer", "default": 1000},
                "timezone": {"type": "string", "default": "local"}
            },
            "yasb.cpu.CpuWidget": {
                "label": {"type": "string", "default": "CPU: {cpu_percent}%"},
                "update_interval": {"type": "integer", "default": 2000},
                "show_frequency": {"type": "boolean", "default": False}
            },
            "yasb.memory.MemoryWidget": {
                "label": {"type": "string", "default": "RAM: {memory_percent}%"},
                "update_interval": {"type": "integer", "default": 2000},
                "show_available": {"type": "boolean", "default": False}
            },
            "yasb.battery.BatteryWidget": {
                "label": {"type": "string", "default": "🔋 {battery_percent}%"},
                "show_charging_status": {"type": "boolean", "default": True},
                "low_battery_threshold": {"type": "integer", "default": 20}
            },
            "yasb.volume.VolumeWidget": {
                "label": {"type": "string", "default": "🔊 {volume_percent}%"},
                "show_mute_status": {"type": "boolean", "default": True},
                "step": {"type": "integer", "default": 5}
            },
            "yasb.network.NetworkWidget": {
                "label": {"type": "string", "default": "📶 {network_status}"},
                "show_speed": {"type": "boolean", "default": True},
                "interface": {"type": "string", "default": "auto"}
            },
            "yasb.active_window.ActiveWindowWidget": {
                "label": {"type": "string", "default": "{win_title}"},
                "max_length": {"type": "integer", "default": 50},
                "show_icon": {"type": "boolean", "default": True}
            },
            "yasb.weather.WeatherWidget": {
                "label": {"type": "string", "default": "🌤️ {temperature}°C"},
                "location": {"type": "string", "default": "auto"},
                "update_interval": {"type": "integer", "default": 600000},
                "units": {"type": "choice", "default": "metric", "choices": ["metric", "imperial"]}
            },
            "yasb.disk.DiskWidget": {
                "label": {"type": "string", "default": "💾 {disk_percent}%"},
                "path": {"type": "string", "default": "C:\\"},
                "update_interval": {"type": "integer", "default": 5000}
            },
            "yasb.custom.CustomWidget": {
                "label": {"type": "string", "default": "Custom"},
                "command": {"type": "string", "default": ""},
                "update_interval": {"type": "integer", "default": 5000}
            }
        }
        
        return options_map.get(widget_type, {})
    
    def load_data(self):
        """Carrega os dados do widget no diálogo."""
        if 'name' in self.widget_data:
            self.name_var.set(self.widget_data['name'])
        
        if 'type' in self.widget_data:
            self.type_var.set(self.widget_data['type'])
            self.update_options_ui()
        
        if 'enabled' in self.widget_data:
            self.enabled_var.set(self.widget_data['enabled'])
        
        if 'position' in self.widget_data:
            self.position_var.set(self.widget_data['position'])
        
        # Carregar opções
        if 'options' in self.widget_data:
            for option_name, option_value in self.widget_data['options'].items():
                if option_name in self.option_vars:
                    if isinstance(self.option_vars[option_name], tk.BooleanVar):
                        self.option_vars[option_name].set(bool(option_value))
                    else:
                        self.option_vars[option_name].set(str(option_value))
    
    def get_data(self) -> Dict[str, Any]:
        """Retorna os dados do widget do diálogo."""
        data = {
            'name': self.name_var.get().strip(),
            'type': self.type_var.get(),
            'enabled': self.enabled_var.get(),
            'position': self.position_var.get(),
            'options': {}
        }
        
        # Coletar opções
        for option_name, var in self.option_vars.items():
            if isinstance(var, tk.BooleanVar):
                data['options'][option_name] = var.get()
            else:
                value = var.get().strip()
                # Tentar converter para número se possível
                try:
                    if '.' in value:
                        data['options'][option_name] = float(value)
                    else:
                        data['options'][option_name] = int(value)
                except ValueError:
                    data['options'][option_name] = value
        
        return data
    
    def validate_data(self) -> bool:
        """Valida os dados do diálogo."""
        if not self.name_var.get().strip():
            messagebox.showerror("Erro", "Nome do widget é obrigatório.")
            return False
        
        if not self.type_var.get():
            messagebox.showerror("Erro", "Tipo do widget é obrigatório.")
            return False
        
        return True
    
    def ok(self):
        """Callback para o botão OK."""
        if self.validate_data():
            self.result = self.get_data()
            self.dialog.destroy()
    
    def cancel(self):
        """Callback para o botão Cancelar."""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Mostra o diálogo e retorna o resultado."""
        self.dialog.wait_window()
        return self.result


class AddWidgetDialog(WidgetDialog):
    """Diálogo para adicionar um novo widget."""
    
    def __init__(self, parent):
        super().__init__(parent, "Adicionar Widget")


class EditWidgetDialog(WidgetDialog):
    """Diálogo para editar um widget existente."""
    
    def __init__(self, parent, widget_data: Dict[str, Any]):
        super().__init__(parent, "Editar Widget", widget_data)
        # Desabilitar edição do nome para widgets existentes
        self.name_entry.configure(state='readonly')


class StyleEditorDialog:
    """Diálogo para edição avançada de estilos."""
    
    def __init__(self, parent, style_data: Optional[Dict[str, Any]] = None):
        self.parent = parent
        self.result = None
        self.style_data = style_data or {}
        
        # Criar janela
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editor de Estilos Avançado")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.center_window()
        
        # Configurar interface
        self.setup_ui()
        
        # Carregar dados se fornecidos
        if self.style_data:
            self.load_data()
    
    def center_window(self):
        """Centraliza a janela na tela."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook para diferentes categorias de estilos
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Aba de cores
        self.create_colors_tab(notebook)
        
        # Aba de tipografia
        self.create_typography_tab(notebook)
        
        # Aba de layout
        self.create_layout_tab(notebook)
        
        # Aba de efeitos
        self.create_effects_tab(notebook)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(buttons_frame, text="Aplicar", command=self.ok).pack(side=tk.RIGHT)
    
    def create_colors_tab(self, notebook):
        """Cria a aba de configurações de cores."""
        colors_frame = ttk.Frame(notebook, padding="10")
        notebook.add(colors_frame, text="Cores")
        
        self.color_vars = {}
        colors = [
            ("Cor de Fundo", "background_color", "#1e1e1e"),
            ("Cor do Texto", "text_color", "#ffffff"),
            ("Cor de Destaque", "accent_color", "#007acc"),
            ("Cor da Borda", "border_color", "#333333"),
            ("Cor de Hover", "hover_color", "#404040"),
            ("Cor de Seleção", "selection_color", "#0078d4")
        ]
        
        for i, (label, var_name, default) in enumerate(colors):
            ttk.Label(colors_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=(0, 10))
            
            color_frame = ttk.Frame(colors_frame)
            color_frame.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
            
            self.color_vars[var_name] = tk.StringVar(value=default)
            color_entry = ttk.Entry(color_frame, textvariable=self.color_vars[var_name], width=15)
            color_entry.pack(side=tk.LEFT, padx=(0, 5))
            
            # Botão de preview da cor
            color_preview = tk.Label(color_frame, width=3, height=1, relief=tk.RAISED)
            color_preview.pack(side=tk.LEFT, padx=(0, 5))
            
            # Atualizar preview quando a cor mudar
            def update_preview(var=self.color_vars[var_name], preview=color_preview):
                try:
                    preview.configure(bg=var.get())
                except tk.TclError:
                    preview.configure(bg='white')
            
            self.color_vars[var_name].trace('w', lambda *args, func=update_preview: func())
            update_preview()
        
        colors_frame.columnconfigure(1, weight=1)
    
    def create_typography_tab(self, notebook):
        """Cria a aba de configurações de tipografia."""
        typo_frame = ttk.Frame(notebook, padding="10")
        notebook.add(typo_frame, text="Tipografia")
        
        # Família da fonte
        ttk.Label(typo_frame, text="Família da Fonte:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.font_family_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(typo_frame, textvariable=self.font_family_var, width=25)
        font_combo['values'] = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Segoe UI"]
        font_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Tamanho da fonte
        ttk.Label(typo_frame, text="Tamanho da Fonte:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.font_size_var = tk.StringVar(value="12")
        ttk.Spinbox(typo_frame, from_=8, to=72, textvariable=self.font_size_var, width=25).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Peso da fonte
        ttk.Label(typo_frame, text="Peso da Fonte:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.font_weight_var = tk.StringVar(value="normal")
        ttk.Combobox(typo_frame, textvariable=self.font_weight_var, width=25,
                    values=["normal", "bold", "light"]).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Estilo da fonte
        ttk.Label(typo_frame, text="Estilo da Fonte:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.font_style_var = tk.StringVar(value="normal")
        ttk.Combobox(typo_frame, textvariable=self.font_style_var, width=25,
                    values=["normal", "italic", "oblique"]).grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        typo_frame.columnconfigure(1, weight=1)
    
    def create_layout_tab(self, notebook):
        """Cria a aba de configurações de layout."""
        layout_frame = ttk.Frame(notebook, padding="10")
        notebook.add(layout_frame, text="Layout")
        
        # Padding
        ttk.Label(layout_frame, text="Padding:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.padding_var = tk.StringVar(value="5")
        ttk.Spinbox(layout_frame, from_=0, to=50, textvariable=self.padding_var, width=25).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Margin
        ttk.Label(layout_frame, text="Margin:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.margin_var = tk.StringVar(value="2")
        ttk.Spinbox(layout_frame, from_=0, to=50, textvariable=self.margin_var, width=25).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Largura da borda
        ttk.Label(layout_frame, text="Largura da Borda:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.border_width_var = tk.StringVar(value="1")
        ttk.Spinbox(layout_frame, from_=0, to=10, textvariable=self.border_width_var, width=25).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Raio da borda
        ttk.Label(layout_frame, text="Raio da Borda:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.border_radius_var = tk.StringVar(value="0")
        ttk.Spinbox(layout_frame, from_=0, to=20, textvariable=self.border_radius_var, width=25).grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        layout_frame.columnconfigure(1, weight=1)
    
    def create_effects_tab(self, notebook):
        """Cria a aba de configurações de efeitos."""
        effects_frame = ttk.Frame(notebook, padding="10")
        notebook.add(effects_frame, text="Efeitos")
        
        # Transparência
        ttk.Label(effects_frame, text="Transparência (%):").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.opacity_var = tk.StringVar(value="100")
        ttk.Scale(effects_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.opacity_var).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # Sombra
        self.shadow_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(effects_frame, text="Ativar Sombra", variable=self.shadow_enabled_var).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Blur
        self.blur_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(effects_frame, text="Ativar Blur", variable=self.blur_enabled_var).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        effects_frame.columnconfigure(1, weight=1)
    
    def load_data(self):
        """Carrega os dados de estilo no diálogo."""
        # Implementar carregamento de dados
        pass
    
    def get_data(self) -> Dict[str, Any]:
        """Retorna os dados de estilo do diálogo."""
        data = {
            'colors': {},
            'typography': {},
            'layout': {},
            'effects': {}
        }
        
        # Cores
        for var_name, var in self.color_vars.items():
            data['colors'][var_name] = var.get()
        
        # Tipografia
        data['typography'] = {
            'font_family': self.font_family_var.get(),
            'font_size': self.font_size_var.get(),
            'font_weight': self.font_weight_var.get(),
            'font_style': self.font_style_var.get()
        }
        
        # Layout
        data['layout'] = {
            'padding': self.padding_var.get(),
            'margin': self.margin_var.get(),
            'border_width': self.border_width_var.get(),
            'border_radius': self.border_radius_var.get()
        }
        
        # Efeitos
        data['effects'] = {
            'opacity': self.opacity_var.get(),
            'shadow_enabled': self.shadow_enabled_var.get(),
            'blur_enabled': self.blur_enabled_var.get()
        }
        
        return data
    
    def ok(self):
        """Callback para o botão OK."""
        self.result = self.get_data()
        self.dialog.destroy()
    
    def cancel(self):
        """Callback para o botão Cancelar."""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Mostra o diálogo e retorna o resultado."""
        self.dialog.wait_window()
        return self.result

