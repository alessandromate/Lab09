from database.DB_connect import DBConnect

class RegioneDAO:
    
    @staticmethod
    def get_regioni() :  # lista di oggetti
        """Restituisce tutte le regioni:return: lista di tutte le Regioni"""
        from model.regione import Regione
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = '''SELECT * FROM regione'''
        try:
            cursor.execute(query)
            for row in cursor:
                regione = Regione(
                    id=row["id"],
                    nome=row["nome"]
                )
                result.append(regione)
        except Exception as e:
            print(f"Errore durante la query get_regioni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
