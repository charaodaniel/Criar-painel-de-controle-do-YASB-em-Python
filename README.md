# 🎛️ YASB Control Panel - Python Version
_A modern and intuitive graphical interface to configure YASB (Yet Another Status Bar) on Windows, developed in Python with tkinter/ttk._

Repository: [Criar-painel-de-controle-do-YASB-em-Python](https://github.com/charaodaniel/Criar-painel-de-controle-do-YASB-em-Python.git)

---

## 📋 About the Project

This control panel allows you to visually configure YASB without manually editing YAML and CSS files. With a native and modern desktop interface, you can manage widgets, customize styles, and adjust advanced settings easily and efficiently.

---

## ✨ Features

### 🧩 Widget Management
- **Tree view** of all configured widgets
- **Enable/disable** widgets with a click
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
- **Border configuration** (width, radius, color)
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
- **Configuration testing** with validation
- **Screenshot capture** of the preview
- **Automatic YASB reload**

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
   # Clone or download the files to a local folder
   mkdir yasb_control_panel
   cd yasb_control_panel
Install dependencies

bash
Copiar
Editar
pip install pyyaml
Check if tkinter is available

bash
Copiar
Editar
python -c "import tkinter; print('tkinter available')"
Initial Configuration
Run the control panel

bash
Copiar
Editar
python main_enhanced.py
Set the YASB path

Click "📂 Set YASB Path"

Select the directory where YASB is installed

Example: C:\Program Files\yasb or C:\Users\YourUser\yasb

Load your existing configuration

Click "📁 Open Config"

Select your YASB config.yaml file

Or let the panel load automatically if in the default directory

📖 How to Use
Widget Management
View Widgets

Go to the "🧩 Widgets" tab

See all widgets in the tree view on the left

Click a widget to view its properties

Add New Widget

Click "➕ Add"

Choose widget type

Configure options

Set its position on the bar (left, center, right)

Edit Existing Widget

Select the widget in the tree

Click "✏️ Edit"

Modify the settings as needed

Enable/Disable Widget

Select the widget

Click "🔄 Enable/Disable"

Style Customization
Apply Predefined Theme

Go to the "🎨 Styles" tab

Select a theme (Dark, Light, Blue, Green)

The theme will be applied automatically

Customize Colors

Click the "🎨" buttons next to each color

Use the color picker

Or enter the hex code manually

Configure Font and Layout

Adjust font family, size, and weight

Set padding and margin

Click "✅ Apply Styles"

Advanced Editor

Click "🎨 Advanced Editor"

Configure colors, typography, layout, and effects

Save advanced configurations

Advanced Settings
System Settings

Go to the "⚙️ Advanced" tab

Configure auto-start and debug mode

Adjust display settings

YAML Editor

Edit configuration directly in YAML

Use "✅ Validate YAML" to check syntax

Use "🔧 Format" to organize code

Preview and Testing
View Preview

Go to the "👁️ Preview" tab

Click "🔄 Refresh Preview"

See how the bar will look

Test Configuration

Click "🚀 Test Configuration"

Check for issues in the configuration

Apply to YASB

Save the configuration with "💾 Save Config"

Click "🔄 Reload YASB" to apply

📁 File Structure
bash
Copiar
Editar
yasb_control_panel/
├── main_enhanced.py          # Main application
├── widget_dialogs.py         # Widget editing dialogs
├── config_example.yaml       # Example configuration
├── test_config.py            # Test script
├── README.md                 # This file
└── themes/                   # Custom themes (created automatically)
🔧 Supported Widget Types
ClockWidget - Clock with date and time

CpuWidget - CPU monitor

MemoryWidget - RAM monitor

BatteryWidget - Battery status

VolumeWidget - Volume control

NetworkWidget - Network status

ActiveWindowWidget - Active window

WeatherWidget - Weather information

DiskWidget - Disk usage

CustomWidget - Custom widget

🎨 Predefined Themes
Dark Theme (Default)
Background: #1e1e1e

Text: #ffffff

Accent: #007acc

Border: #333333

Light Theme
Background: #ffffff

Text: #000000

Accent: #0078d4

Border: #cccccc

Blue Theme
Background: #0f1419

Text: #e6e6e6

Accent: #00d4ff

Border: #1e3a5f

Green Theme
Background: #0d1117

Text: #c9d1d9

Accent: #00ff88

Border: #21262d

🐛 Troubleshooting
Error: "YASB not found"
Check that YASB is installed

Use "📂 Set YASB Path" to manually set the path

Ensure the directory contains the YASB files

Error: "Error loading configuration"
Check if the YAML file is valid

Use the integrated YAML validator

Ensure the file isn't used by another program

Error: "Failed to reload YASB"
Make sure YASB isn’t running

Run the panel as administrator if needed

Verify that the YASB path is correct

Interface unresponsive
Close and reopen the app

Check for console errors

Ensure Python and tkinter are working

📝 Usage Tips
Backup Your Config

Always back up your config.yaml before making changes

Use "💾 Save Config" regularly

Test Before Applying

Use the preview to check how it looks

Test the configuration before reloading YASB

Organize Widgets

Keep related widgets in the same position

Use descriptive names for custom widgets

Customize Styles

Start with a predefined theme

Make gradual adjustments

Save custom themes for reuse

🤝 Contribution
This panel was developed as a desktop alternative to the original web panel. Suggestions and improvements are welcome!

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
YASB Team - For the excellent YASB project

Python Community - For the libraries used

Users - For feedback and suggestions

Developed with ❤️ for the YASB community