import flet as ft
import os
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab09"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        # Intestazione
        self.txt_titolo = ft.Text(value="Generatore di Pacchetti Turistici", size=38, weight=ft.FontWeight.BOLD)

        # Mappa
        img_path = os.path.join(os.getcwd(), 'UI/italia_mappa.png')
        self.mappa = ft.Image(src=img_path,height=300)

        # Regioni
        self.dd_regione = ft.Dropdown(
            label="Regione",
            menu_height=150,
            width=200,
            hint_text="Selezionare una regione",
            on_change=self.controller.on_regione_change
        )
        self.controller.popola_dropdown_regione()

        # Durata Massima in Giorni
        self.durata_massima = ft.TextField(label="Durata (in Giorni)",
                                           on_change=self.controller.check_giorni)

        # Budget Massimo
        self.budget_massimo = ft.TextField(label="Budget (es. € 300,00)",
                                           prefix=ft.Text("€ "),
                                           on_change=self.controller.check_budget)

        pulsante_genera_pacchetto = ft.ElevatedButton("Genera Pacchetto", on_click=self.controller.genera_pacchetto)

        # Menu interagibile
        self.menu = ft.Column(controls=[self.dd_regione,
                                        self.durata_massima,
                                        self.budget_massimo,
                                        pulsante_genera_pacchetto],
                              spacing=50)

        # Visualizzazione mediante ListView
        self.lista_visualizzazione = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)


        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            # Sezione 2
            ft.Row(controls=[self.mappa, self.menu], spacing=150, alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            # Sezione 3
            ft.Container(
                content=self.lista_visualizzazione,
                height=250,
                border=ft.border.all(1, ft.Colors.BLACK),
                padding=10,
            )
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
    ''