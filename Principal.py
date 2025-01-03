import flet as ft
from Funções import Leitor_de_Arquivos, Tradutor_de_CNAB
from openpyxl import Workbook


def main(page: ft.Page):
    page.title = "Cnab Bradesco"
    page.window.width = 700
    page.window.height = 450
    page.window.center()
    page.window.resizable = False
    page.window.maximizable = False
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.to_front()
    page.update()

    def resultado_selecao_arquivos(e: ft.FilePickerResultEvent):
        if e.files:
            caminho_arquivo = e.files[0].path
            conteudo = Leitor_de_Arquivos(caminho_arquivo)
            conteudo_arquivo.value = conteudo
            arquivos_selecionados.value = e.files[0].name
        else:
            arquivos_selecionados.value = "Seleção cancelada!"
        page.update()

    def resultado_salvamento_arquivos(e: ft.FilePickerResultEvent):
        if e.path:
            salvar_arquivo(e.path)
        else:
            arquivos_selecionados.value = "Salvamento cancelado!"
        page.update()

    def salvar_arquivo(caminho):
        if not caminho.endswith('.xlsx'):
            caminho += '.xlsx'

        if conteudo_arquivo.value:
            dados = Tradutor_de_CNAB(conteudo_arquivo.value)
            try:
                wb = Workbook()
                ws = wb.active
                ws.title = "CNAB Dados"
                ws.append(["Favorecido", "Ocorrências", "Descrições"])

                for linha in dados:
                    partes = linha.split(" ")
                    favorecido = " ".join(
                        partes[1:partes.index("Ocorrências:")])
                    ocorrencias = partes[partes.index("Ocorrências:") + 1]
                    descricoes = " ".join(
                        partes[partes.index("Descrições:") + 1:])
                    ws.append([favorecido, ocorrencias, descricoes])

                wb.save(caminho)
                arquivos_selecionados.value = "Arquivo salvo com sucesso!"
            except Exception as e:
                arquivos_selecionados.value = f"Erro ao criar arquivo de saída: {
                    str(e)}"
        else:
            arquivos_selecionados.value = "Nenhum arquivo selecionado!"
        page.update()

    def btn_selecionar_arquivo(e):
        dialogo_selecao_arquivos.pick_files(
            allow_multiple=False, allowed_extensions=["ret"])

    def btn_salvar_arquivo(e):
        if '.ret' in arquivos_selecionados.value:
            dialogo_salvamento_arquivos.save_file(
                file_name="Sem_Nome.xlsx", allowed_extensions=["xlsx"])
        else:
            arquivos_selecionados.value = "Nenhum arquivo selecionado!"
            arquivos_selecionados.update()

    conteudo_arquivo = ft.Text()

    arquivos_selecionados = ft.TextField(
        label="Arquivo Selecionado",
        value=" ",
        read_only=True,
        width=520,
        prefix_icon=ft.Icons.ATTACH_FILE,
        text_size=14,
    )

    dialogo_selecao_arquivos = ft.FilePicker(
        on_result=resultado_selecao_arquivos)

    dialogo_salvamento_arquivos = ft.FilePicker(
        on_result=resultado_salvamento_arquivos)

    page.overlay.append(dialogo_selecao_arquivos)
    page.overlay.append(dialogo_salvamento_arquivos)

    imagem = ft.Image(
        src=r"C:\Leitor_CNAB_Bradesco-main\Bradesco.ico", width=150, height=150)

    btn_selecionar = ft.ElevatedButton(
        text="Selecionar Arquivo",
        width=250,
        height=50,
        bgcolor='#f0152d',
        color=ft.Colors.GREY_100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
        on_click=btn_selecionar_arquivo
    )

    btn_criar_tabela = ft.ElevatedButton(
        text="Processar Arquivo",
        width=250,
        height=50,
        bgcolor=ft.Colors.GREY_100,
        color='#f0152d',
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
        on_click=btn_salvar_arquivo,
    )

    linha_imagem = ft.Row(
        controls=[imagem],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    linha_botoes = ft.Row(
        controls=[btn_selecionar, btn_criar_tabela],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    linha_textfield = ft.Row(
        controls=[arquivos_selecionados],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )

    coluna = ft.Column(
        controls=[linha_imagem, linha_botoes, linha_textfield],
        width=500,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Container(
            content=coluna,
            alignment=ft.alignment.center,
            expand=True,
            padding=20,
            border_radius=10,
        )
    )


ft.app(target=main)
