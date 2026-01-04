from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        self._tour_regione = []
        self._max_giorni = None
        self._max_budget = None

        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni(): # lista di oggetti
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()
    def load_tour(self):     #ORM :   key= tour_id value=ogg di quel tour
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()
    def load_attrazioni(self):   #ORM : Key=attrazione_id value=ogg di quell attrazione
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()
    def load_relazioni(self):          #scopo  è  popolare i set dei due ORM
        """Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.--> Ogni Tour ha un set di Attrazione.--> Ogni Attrazione ha un set di Tour."""
        relazioni = TourDAO.get_tour_attrazioni() #output:list di tuple di dizionari:keys(id_tour,id_attrazione)
        for relazione in relazioni:   #ciclo per ogni binomio tour-attr
            tour_id = relazione["id_tour"]                  #mi salvo la var id tour
            attrazione_id = relazione["id_attrazione"]      #mi salvo in var id attr

            # link Attrazione-Tour: salvo il set di ogg attr dentro ogni ogg tour
            if relazione["id_tour"] in self.tour_map and relazione["id_attrazione"] in self.attrazioni_map:
                tour = self.tour_map[tour_id]    #salvo ogg tour accedendo per id
                attrazione = self.attrazioni_map[attrazione_id]     #salvo ogg attr accedendo per id

                #ogg tour ha un set di attr, le quali vado ad aggiungere
                #ogg attr ha un set di tour, i quali vado ad aggiungere
                tour.attrazioni.add(attrazione)
                attrazione.tour.add(tour)
    #3 parametri in input (quelli dall utente
    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """ Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        1)param id_regione: id della regione 2)param max_giorni: numero massimo di giorni (può essere None --> nessun limite) 3)param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)
        1)return: self._pacchetto_ottimo (una lista di oggetti Tour) 2)return: self._costo (il costo del pacchetto) 3)return: self._valore_ottimo (il valore culturale del pacchetto)"""
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1
        # Vincoli
        self._max_giorni = max_giorni
        self._max_budget = max_budget

        # output: lista di ogg tour (filtrati su id_regione)
        self._tour_regione = self._get_tour_per_regione(id_regione)

        # Inizio ricorsione: do il via alla funzione
        self._ricorsione(start_index=0,pacchetto_parziale=[],durata_corrente=0,
                         costo_corrente=0,valore_corrente=0,attrazioni_usate=set())
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # 🟤 Aggiornamento soluzione ottima
        if valore_corrente > self._valore_ottimo:
            self._valore_ottimo = valore_corrente       #update valore culturale corr
            self._pacchetto_ottimo = pacchetto_parziale.copy() #usando il copy non ha uguaglianza dinamica il pac ottimo
            self._costo = costo_corrente            #update: costo

        # 🟢 Condizione di Terminazione
        #1)analisi finita dei tour nella lista 2) durata sfora 3) costo sfora
        if start_index >= len(self._tour_regione) or \
                (self._max_giorni is not None and durata_corrente >= self._max_giorni) or \
                (self._max_budget is not None and costo_corrente >= self._max_budget):
            return
        # 🟣 Generazione di nuove soluzioni
        for i in range(start_index, len(self._tour_regione)):
            tour = self._tour_regione[i]

            # 🟡 Controllo vincoli
            risultato = self._controllo_vincoli(tour,pacchetto_parziale,attrazioni_usate,durata_corrente,costo_corrente)
            #risultato o è vuoto(xche non ha rispettato vincoli) oppure ha come output 2 valori:durata e costo nuovi
            if risultato is not None:
                nuova_durata, nuovo_costo = risultato
                # 🔵 Aggiungi tour
                pacchetto_parziale.append(tour)       #update: pacchetto parziale
                attrazioni_usate.update(tour.attrazioni)       #update: attrazioni usate
                nuovo_valore = valore_corrente + sum(a.valore_culturale for a in tour.attrazioni) #update: val culturale

                # 🔴 Ricorsione successiva
                self._ricorsione(start_index=i + 1,pacchetto_parziale=pacchetto_parziale,durata_corrente=nuova_durata,
                                 costo_corrente=nuovo_costo,valore_corrente=nuovo_valore,attrazioni_usate=attrazioni_usate)
                # 🟣 Backtracking
                pacchetto_parziale.pop()
                attrazioni_usate.difference_update(tour.attrazioni)

     #ciclo per i tour dentro la map(ORM) , accedo per i valori ( .values() )-> prendo ogg tour e verifico =id_regione
      #output: lista di ogg tour
    def _get_tour_per_regione(self, id_regione: str):
        """ Restituisce tutti i tour disponibili per una regione specifica """
        return [t for t in self.tour_map.values() if t.id_regione == id_regione]

    def _controllo_vincoli(self, tour, pacchetto_parziale, attrazioni_usate, durata_corrente, costo_corrente):
        """Controlla i vincoli: 1)tour duplicati 2)attrazioni duplicate 3)durata massima 4)costo massimo"""
        # L'assenza di tour duplicati è già garantito grazie a start_index

        #1) tour duplicati
        # Controlla attrazioni duplicate facendo intersezione tra set
        if attrazioni_usate.intersection(tour.attrazioni):
            return None

        #2,3) aggiorno durata + costo
        nuova_durata = durata_corrente + tour.durata_giorni
        nuovo_costo = costo_corrente + tour.costo

        #2,3) aggiorno durata + costo oltre limiti
        if self._max_giorni is not None and nuova_durata > self._max_giorni:
            return None
        if self._max_budget is not None and nuovo_costo > self._max_budget:
            return None

        return nuova_durata, nuovo_costo