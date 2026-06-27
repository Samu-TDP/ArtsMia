import flet as ft


class Controller:
    def __init__(self, view, model):
        # Il Controller ha accesso sia alla grafica (View) che al cervello (Model)
        self._view = view
        self._model = model

    # ==========================================
    # AZIONE BOTTONE 1: ANALIZZA OGGETTI (Crea Grafo)
    # ==========================================
    def handleAnalizzaOggetti(self, e):
        # STEP 1: Pulisci l'area risultati
        self._view.txt_result.controls.clear()

        # STEP 2: Valida l'input (In questo caso non ci sono input da validare!)
        # Passiamo direttamente al punto 3.

        # STEP 3: Delega al Model il lavoro pesante
        # Diciamo al Model di costruire il grafo interrogando il DAO
        self._model.crea_grafo()

        # Finito di creare il grafo, chiediamo al model i dati riassuntivi
        n_nodi = self._model.get_num_nodes()
        n_archi = self._model.get_num_edges()

        # STEP 4: Impagina i risultati
        # Stampiamo i messaggi a schermo usando ft.Text
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato con successo!", color="green", weight="bold")
        )
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        # STEP 5: Aggiorna lo schermo
        self._view.update_page()

    # ==========================================
    # AZIONE BOTTONE 2: CERCA COMPONENTE CONNESSA
    # ==========================================
    def handleCompConnessa(self, e):
        # STEP 1: Pulisci l'area risultati
        self._view.txt_result.controls.clear()

        # STEP 2: Valida l'input dell'utente (FONDAMENTALE)

        # 2a. Controllo logico: Il grafo è stato creato?
        # Se l'utente preme questo bottone prima di "Analizza Oggetti", il programma crasherebbe!
        if self._model.get_num_nodes() == 0:
            self._view.create_alert("Attenzione: devi prima creare il grafo cliccando su 'Analizza oggetti'!")
            return

        # 2b. L'utente ha scritto qualcosa nel campo di testo?
        id_inserito = self._view._txtIdOggetto.value
        if not id_inserito:
            self._view.create_alert("Per favore, inserisci un ID Oggetto.")
            return

        # 2c. Quello che ha scritto è un numero intero? (Uso del blocco try-except)
        try:
            obj_id = int(id_inserito)
        except ValueError:
            self._view.create_alert("L'ID deve essere un numero intero (es. 1234).")
            return

        # 2d. Controllo "Intelligente": Questo ID esiste nel nostro database/grafo?
        # Chiediamo al model se la chiave è presente nel dizionario idMap.
        if not self._model.esiste_oggetto(obj_id):
            self._view.create_alert(f"L'oggetto con ID {obj_id} non è presente nel database.")
            return

        # STEP 3: Delega al Model il lavoro algoritmico
        # Chiediamo la componente connessa e riceviamo indietro un 'set' (insieme di nodi)
        componente = self._model.get_connected_component(obj_id)

        # STEP 4: Impagina i risultati
        dimensione = len(componente)
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa trovata!", color="green", weight="bold")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"La componente che contiene l'oggetto {obj_id} ha dimensione: {dimensione}")
        )

        # STEP 5: Aggiorna lo schermo
        self._view.update_page()




