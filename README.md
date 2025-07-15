🎛️ YASB Control Panel (Python Version)
A modern and intuitive graphical interface to configure YASB (Yet Another Status Bar) on Windows, built with Python and tkinter/ttk.

Repository: Criar-painel-de-controle-do-YASB-em-Python

📋 About the Project
This control panel lets you visually configure YASB without manually editing YAML or CSS files. With a native desktop interface, you can manage widgets, customize styles, and adjust advanced settings easily.

✨ Features
🧩 Widget Management
Tree view of all configured widgets
Enable/disable widgets with one click
Edit properties (position, parameters)
Add, duplicate, and remove widgets
🎨 Style Editor
Integrated color picker
Predefined themes: Dark, Light, Blue, Green
Font, spacing, and border configuration
Advanced style editor by category
Save and load custom themes
⚙️ Advanced Settings
System options (auto-start, debug mode)
Display settings (monitor, position, size)
Integrated YAML editor with validation and auto-formatting
👁️ Preview & Testing
Visual preview of the status bar
Configuration validation and testing
Screenshot capture of the preview
Automatic YASB reload
🚀 Technologies Used
Python 3.11+
tkinter/ttk
PyYAML
JSON
🛠️ Installation
Prerequisites
Python 3.11 or higher
YASB installed on Windows
Libraries: pyyaml, tkinter (included with Python)
Steps
Download the control panel files


git clone https://github.com/charaodaniel/Criar-painel-de-controle-do-YASB-em-Python.gitcd Criar-painel-de-controle-do-YASB-em-Python
Install dependencies


pip install pyyaml
Check tkinter


python -c "import tkinter; print('tkinter available')"
Run the control panel


python main_enhanced.py
Set the YASB path

Click "📂 Set YASB Path" and select your YASB folder
Load your configuration

Click "📁 Open Config" and select your config.yaml
📖 How to Use
Widget Management
Go to the "🧩 Widgets" tab to view, add, edit, duplicate, or remove widgets.
Style Customization
In the "🎨 Styles" tab, select a theme or customize colors, fonts, and layout.
Advanced Settings
Adjust system and display options in the "⚙️ Advanced" tab.
Edit YAML directly and validate syntax.
Preview & Testing
See the preview in the "👁️ Preview" tab.
Test your configuration and apply it to YASB.
📁 File Structure

yasb_control_panel/├── main_enhanced.py          # Main application├── widget_dialogs.py         # Widget editing dialogs├── config_example.yaml       # Example configuration├── test_config.py            # Test script├── README.md                 # This file└── themes/                   # Custom themes
🔧 Supported Widget Types
ClockWidget
CpuWidget
MemoryWidget
BatteryWidget
VolumeWidget
NetworkWidget
ActiveWindowWidget
WeatherWidget
DiskWidget
CustomWidget
🎨 Predefined Themes
Theme	Background	Text	Accent	Border
Dark	#1e1e1e	#ffffff	#007acc	#333333
Light	#ffffff	#000000	#0078d4	#cccccc
Blue	#0f1419	#e6e6e6	#00d4ff	#1e3a5f
Green	#0d1117	#c9d1d9	#00ff88	#21262d
🐛 Troubleshooting
YASB not found: Check if YASB is installed and the path is correct.
Error loading configuration: Validate the YAML file and ensure it’s not in use.
Failed to reload YASB: Run as administrator and verify the path.
Interface unresponsive: Restart the app and check the console.
📝 Usage Tips
Always back up your config.yaml
Test before applying changes
Organize widgets by position and name
Customize styles gradually and save themes
🤝 Contribution
Suggestions and improvements are welcome! This panel is a desktop alternative to the original web panel.

📄 License
Project under the MIT License. See LICENSE for details.

🙏 Acknowledgements
YASB Team
Python Community
Users and contributors
Developed with ❤️ for the YASB community.

Let me know if you want any adjustments or further improvements!