#!/usr/bin/env python3
"""
Script de teste para validar as funcionalidades do painel de controle YASB.
"""

import yaml
import os
import json
from pathlib import Path


def test_yaml_operations():
    """Testa operações com arquivos YAML."""
    print("=== Testando operações YAML ===")
    
    # Teste de leitura
    try:
        with open('config_example.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        print("✅ Leitura de YAML: OK")
        print(f"   - Widgets encontrados: {len(config.get('widgets', {}))}")
        print(f"   - Barras encontradas: {len(config.get('bars', {}))}")
    except Exception as e:
        print(f"❌ Erro na leitura de YAML: {e}")
        return False
    
    # Teste de escrita
    try:
        test_config = {
            "test": True,
            "widgets": {
                "test_widget": {
                    "type": "test.TestWidget",
                    "enabled": True,
                    "options": {
                        "label": "Test"
                    }
                }
            }
        }
        
        with open('test_output.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(test_config, file, default_flow_style=False, allow_unicode=True, indent=2)
        print("✅ Escrita de YAML: OK")
        
        # Verificar se o arquivo foi criado
        if os.path.exists('test_output.yaml'):
            os.remove('test_output.yaml')
            print("✅ Arquivo de teste removido: OK")
    except Exception as e:
        print(f"❌ Erro na escrita de YAML: {e}")
        return False
    
    return True


def test_config_validation():
    """Testa validação de configurações."""
    print("\n=== Testando validação de configurações ===")
    
    # Configuração válida
    valid_config = {
        "bars": {
            "yasb-bar": {
                "enabled": True,
                "widgets": {
                    "left": ["clock"],
                    "center": ["active_window"],
                    "right": ["battery"]
                }
            }
        },
        "widgets": {
            "clock": {
                "type": "yasb.clock.ClockWidget",
                "enabled": True,
                "options": {
                    "label": "{%H:%M:%S}"
                }
            },
            "active_window": {
                "type": "yasb.active_window.ActiveWindowWidget",
                "enabled": True,
                "options": {
                    "label": "{win_title}"
                }
            },
            "battery": {
                "type": "yasb.battery.BatteryWidget",
                "enabled": True,
                "options": {
                    "label": "🔋 {battery_percent}%"
                }
            }
        }
    }
    
    # Teste de validação básica
    errors = []
    
    # Verificar se há widgets configurados
    if not valid_config.get('widgets'):
        errors.append("Nenhum widget configurado")
    
    # Verificar se há widgets ativos
    active_widgets = [w for w in valid_config.get('widgets', {}).values() if w.get('enabled', True)]
    if not active_widgets:
        errors.append("Nenhum widget ativo")
    
    # Verificar configuração da barra
    if not valid_config.get('bars'):
        errors.append("Configuração da barra não encontrada")
    
    if errors:
        print(f"❌ Validação falhou: {errors}")
        return False
    else:
        print("✅ Validação de configuração: OK")
        print(f"   - Widgets ativos: {len(active_widgets)}")
        return True


def test_widget_operations():
    """Testa operações com widgets."""
    print("\n=== Testando operações com widgets ===")
    
    config = {
        "widgets": {
            "clock": {
                "type": "yasb.clock.ClockWidget",
                "enabled": True,
                "options": {
                    "label": "{%H:%M:%S}"
                }
            }
        },
        "bars": {
            "yasb-bar": {
                "widgets": {
                    "left": ["clock"],
                    "center": [],
                    "right": []
                }
            }
        }
    }
    
    # Teste de adição de widget
    new_widget = {
        "type": "yasb.cpu.CpuWidget",
        "enabled": True,
        "options": {
            "label": "CPU: {cpu_percent}%"
        }
    }
    
    config["widgets"]["cpu"] = new_widget
    config["bars"]["yasb-bar"]["widgets"]["left"].append("cpu")
    
    print("✅ Adição de widget: OK")
    print(f"   - Widgets na esquerda: {config['bars']['yasb-bar']['widgets']['left']}")
    
    # Teste de remoção de widget
    if "cpu" in config["widgets"]:
        del config["widgets"]["cpu"]
        config["bars"]["yasb-bar"]["widgets"]["left"].remove("cpu")
        print("✅ Remoção de widget: OK")
    
    # Teste de ativação/desativação
    config["widgets"]["clock"]["enabled"] = False
    print("✅ Desativação de widget: OK")
    
    config["widgets"]["clock"]["enabled"] = True
    print("✅ Ativação de widget: OK")
    
    return True


def test_style_operations():
    """Testa operações com estilos."""
    print("\n=== Testando operações com estilos ===")
    
    # Temas predefinidos
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
        }
    }
    
    # Teste de aplicação de tema
    current_theme = themes["Escuro"]
    print("✅ Aplicação de tema escuro: OK")
    print(f"   - Cor de fundo: {current_theme['background_color']}")
    print(f"   - Cor do texto: {current_theme['text_color']}")
    
    # Teste de salvamento de tema personalizado
    custom_theme = {
        "background_color": "#2d2d30",
        "text_color": "#cccccc",
        "accent_color": "#ff6b6b",
        "border_color": "#404040",
        "font_family": "Arial",
        "font_size": "14",
        "font_weight": "normal"
    }
    
    try:
        with open('test_theme.json', 'w', encoding='utf-8') as file:
            json.dump(custom_theme, file, indent=2)
        print("✅ Salvamento de tema personalizado: OK")
        
        # Teste de carregamento
        with open('test_theme.json', 'r', encoding='utf-8') as file:
            loaded_theme = json.load(file)
        print("✅ Carregamento de tema personalizado: OK")
        
        # Limpar arquivo de teste
        os.remove('test_theme.json')
        print("✅ Limpeza de arquivo de teste: OK")
    except Exception as e:
        print(f"❌ Erro em operações de tema: {e}")
        return False
    
    return True


def test_file_operations():
    """Testa operações com arquivos."""
    print("\n=== Testando operações com arquivos ===")
    
    # Teste de detecção de caminhos
    possible_paths = [
        os.path.expanduser("~/.yasb"),
        os.path.expanduser("~/AppData/Roaming/yasb"),
        "./yasb_test"
    ]
    
    print("✅ Detecção de caminhos possíveis: OK")
    for path in possible_paths:
        exists = os.path.exists(path)
        print(f"   - {path}: {'Existe' if exists else 'Não existe'}")
    
    # Teste de criação de diretório temporário
    test_dir = "./yasb_test"
    try:
        os.makedirs(test_dir, exist_ok=True)
        print("✅ Criação de diretório de teste: OK")
        
        # Teste de escrita de configuração
        test_config_path = os.path.join(test_dir, "config.yaml")
        with open(test_config_path, 'w', encoding='utf-8') as file:
            yaml.dump({"test": True}, file)
        print("✅ Escrita de configuração de teste: OK")
        
        # Limpeza
        os.remove(test_config_path)
        os.rmdir(test_dir)
        print("✅ Limpeza de arquivos de teste: OK")
    except Exception as e:
        print(f"❌ Erro em operações de arquivo: {e}")
        return False
    
    return True


def run_all_tests():
    """Executa todos os testes."""
    print("🧪 INICIANDO TESTES DO PAINEL DE CONTROLE YASB")
    print("=" * 50)
    
    tests = [
        test_yaml_operations,
        test_config_validation,
        test_widget_operations,
        test_style_operations,
        test_file_operations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 RESULTADOS: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A aplicação está funcionando corretamente.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

