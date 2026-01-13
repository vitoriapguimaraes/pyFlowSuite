# Hashzap - Modern Desktop Chat (Flet)

import flet as ft

def main(page: ft.Page):
    page.title = "HashZap Desktop"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Header
    titulo = ft.Text("HashZap", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400)

    # Chat Area
    chat = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # State: User Name
    nome_usuario = ft.TextField(label="Escreva seu nome", width=300)

    # Event: Receive Message from PubSub
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            # Align user's own messages to the right, others to the left
            is_me = (usuario_mensagem == nome_usuario.value)
            alignment = ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START
            bg_color = ft.Colors.CYAN_900 if is_me else ft.Colors.GREY_800
            
            chat.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.Text(usuario_mensagem, size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_200),
                                ft.Text(texto_mensagem, size=14),
                            ]),
                            bgcolor=bg_color,
                            padding=10,
                            border_radius=10,
                            width=300 if len(texto_mensagem) > 50 else None,
                        )
                    ],
                    alignment=alignment
                )
            )
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(
                ft.Row(
                    [ft.Text(f"{usuario_mensagem} entrou no chat", size=12, italic=True, color=ft.Colors.ORANGE_500)],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        page.update()

    page.pubsub.subscribe(enviar_mensagem_tunel)

    # Event: Send Message
    def enviar_mensagem(e):
        if not nome_usuario.value:
            nome_usuario.error_text = "Nome é obrigatório!"
            nome_usuario.update()
            return
            
        if not campo_mensagem.value.strip():
            campo_mensagem.error_text = "Mensagem vazia!"
            campo_mensagem.update()
            return

        page.pubsub.send_all({
            "texto": campo_mensagem.value.strip(),
            "usuario": nome_usuario.value,
            "tipo": "mensagem"
        })
        campo_mensagem.value = ""
        campo_mensagem.focus()
        page.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem, expand=True)
    botao_enviar_mensagem = ft.IconButton(ft.Icons.SEND, icon_color=ft.Colors.CYAN_400, on_click=enviar_mensagem)

    # Popup: Join Chat
    def entrar_popup(e):
        if not nome_usuario.value.strip():
            nome_usuario.error_text = "Nome é obrigatório!"
            nome_usuario.update()
            return
            
        page.pubsub.send_all({"usuario": nome_usuario.value.strip(), "tipo": "entrada"})
        
        # Switch UI to Chat Mode
        page.dialog.open = False
        page.clean()
        
        # Add Header and Chat Area
        page.add(
            ft.Container(
                content=ft.Column([
                    titulo,
                    ft.Container(content=chat, expand=True, padding=10, border=ft.border.all(1, ft.Colors.GREY_800), border_radius=10),
                    ft.Row([campo_mensagem, botao_enviar_mensagem], alignment=ft.MainAxisAlignment.CENTER),
                ]),
                expand=True,
                padding=20
            )
        )
        page.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem-vindo ao HashZap"),
        content=ft.Column([
            ft.Text("Converse em tempo real!"),
            nome_usuario
        ], height=100, tight=True),
        actions=[ft.FilledButton("Entrar", on_click=entrar_popup)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def entrar_chat(e):
        page.dialog = popup
        popup.open = True
        page.update()

    # Initial View: Start Button
    botao_iniciar = ft.FilledButton("Iniciar Chat", icon=ft.Icons.CHAT_BUBBLE, on_click=entrar_chat)

    page.add(
        ft.Container(
            content=ft.Column([
                titulo,
                botao_iniciar
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)