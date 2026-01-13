"""
Action Recorder for Product Registration
Allows user to record custom automation workflow
"""

import keyboard
import time
import json
from pathlib import Path


class ActionRecorder:
    """Records user actions for automation workflow"""

    def __init__(self):
        self.actions = []
        self.recording = False
        self.last_action_time = None

    def start_recording(self):
        """Start recording actions"""
        self.recording = True
        self.last_action_time = time.time()
        print("\n🔴 GRAVANDO - Pressione F9 para parar")
        print("\n📋 Ações de Navegação:")
        print("  - F1: Marcar 'Abrir navegador'")
        print("  - F2: Marcar 'Navegar para URL'")
        print("  - F8: Adicionar delay (3 segundos)")
        print("\n🔐 Ações de Login:")
        print("  - F3: Marcar 'Fazer login completo'")
        print("  - Ctrl+E: Preencher campo EMAIL")
        print("  - Ctrl+P: Preencher campo SENHA")
        print("\n📦 Ações de Produto:")
        print("  - F4: Clicar primeiro campo produto")
        print("  - F5: Preencher todos os campos produto")
        print("  - F6: Submeter formulário")
        print("  - F7: Scroll para cima")
        print("\n💡 Dica: Use Ctrl+E e Ctrl+P para configurações reutilizáveis!")

    def record_action(self, action_type, data=None):
        """Record an action with timestamp"""
        if not self.recording:
            return

        current_time = time.time()
        delay = current_time - self.last_action_time if self.last_action_time else 0

        action = {"type": action_type, "delay": round(delay, 2), "data": data or {}}

        self.actions.append(action)
        self.last_action_time = current_time

        # Visual feedback
        print(f"  ✓ Gravado: {action_type} (depois de {delay:.1f}s)")

    def stop_recording(self):
        """Stop recording"""
        self.recording = False
        print("\n⏹️  Gravação parada!")

    def save(self, filepath):
        """Save recorded actions to JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.actions, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Ações salvas em: {filepath}")


# Key handler mapping (moved outside to reduce complexity)
KEY_ACTIONS = {
    "f1": ("open_browser", None),
    "f3": ("login", None),
    "f4": ("click_first_field", None),
    "f5": ("fill_product_fields", None),
    "f6": ("submit_form", None),
}


def handle_f2(recorder):
    """Handle navigate URL"""
    url = input("\n  Digite a URL: ")
    recorder.record_action("navigate_to_url", {"url": url})


def handle_f7(recorder):
    """Handle scroll"""
    amount = input("\n  Scroll amount (ex: 5000): ")
    recorder.record_action("scroll", {"amount": int(amount)})


def handle_f8(recorder):
    """Handle delay"""
    recorder.record_action("delay", {"seconds": 3})


def handle_ctrl_e(recorder):
    """Handle email field marker"""
    recorder.record_action(
        "fill_email", {"source": "config", "suggestion": "Usa email da configuração"}
    )


def handle_ctrl_p(recorder):
    """Handle password field marker"""
    recorder.record_action(
        "fill_password", {"source": "config", "suggestion": "Usa senha da configuração"}
    )


def create_key_handler(recorder):
    """Create keyboard event handler"""

    def on_key(event):
        # Stop
        if event.name == "f9":
            recorder.stop_recording()
            return False

        # Ctrl combinations
        if keyboard.is_pressed("ctrl"):
            if event.name == "e":
                handle_ctrl_e(recorder)
            elif event.name == "p":
                handle_ctrl_p(recorder)
            return

        # Special handlers
        if event.name == "f2":
            handle_f2(recorder)
        elif event.name == "f7":
            handle_f7(recorder)
        elif event.name == "f8":
            handle_f8(recorder)
        # Simple mappings
        elif event.name in KEY_ACTIONS:
            action_type, data = KEY_ACTIONS[event.name]
            recorder.record_action(action_type, data)

    return on_key


def print_instructions():
    """Print initial instructions"""
    print("=" * 70)
    print("🎬 GRAVADOR DE WORKFLOW - Product Registration")
    print("=" * 70)
    print("\n📋 Grave o fluxo EXATO da sua automação.")
    print("\n💡 Use Ctrl+E/Ctrl+P para marcar campos configuráveis!")


def get_workflow_filepath():
    """Get the workflow file path"""
    base_dir = Path(__file__).parent
    src_dir = base_dir.parent.parent
    config_dir = src_dir / "data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "product_registration_workflow.json"


def print_summary(recorder):
    """Print recording summary"""
    print("\n" + "=" * 70)
    print("✅ Workflow gravado!")
    print("=" * 70)
    print(f"\nTotal de ações: {len(recorder.actions)}")
    for i, action in enumerate(recorder.actions, 1):
        print(f"  {i}. {action['type']} (delay: {action['delay']}s)")


def main():
    """Main recorder interface"""
    print_instructions()
    input("\nPressione ENTER para começar...")

    recorder = ActionRecorder()
    recorder.start_recording()

    keyboard.on_press(create_key_handler(recorder))
    keyboard.wait("f9")

    recorder.save(get_workflow_filepath())
    print_summary(recorder)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Gravação cancelada")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
