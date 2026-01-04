from database.DB_connect import DBConnect
class TourDAO:
    @staticmethod
    def get_tour() :     #dict di dict: key(=id), value(tutte le info)
        """
        Restituisce tutti i tour
        :return: un dizionario di tutti i Tour
        """
        from model.tour import Tour
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM tour"""
        try:
            cursor.execute(query)
            for row in cursor:
                tour = Tour(
                    id=row["id"],
                    nome=row["nome"],
                    durata_giorni=row["durata_giorni"],
                    costo=row["costo"],
                    id_regione=row["id_regione"]
                )
                result[tour.id] = tour
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_tour_attrazioni() -> list | None: #list di tuple di dizionari:keys (id_tour,id_attrazione)
        """Restituisce tutte le relazioni
        :return: una lista di dizionari [{"id_tour": ..., "id_attrazione": ...}]"""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM tour_attrazione"""
        try:
            cursor.execute(query)
            for row in cursor:
                result.append({
                    "id_tour": row["id_tour"],
                    "id_attrazione": row["id_attrazione"]
                })
        except Exception as e:
            print(f"Errore durante la query get_tour_attrazioni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result
