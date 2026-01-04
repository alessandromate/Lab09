from database.DB_connect import DBConnect
class AttrazioneDAO:
    @staticmethod
    def get_attrazioni():
        """
        Restituisce tutte le attrazioni
        :return: un dizionario di tutte le Attrazioni
        """
        from model.attrazione import Attrazione
        cnx = DBConnect.get_connection()
        result = {}        #dict di dict (key= id , value= tutte le info)
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM attrazione"""
        try:
            cursor.execute(query)
            for row in cursor:
                attrazione = Attrazione(
                    id=row["id"],
                    nome=row["nome"],
                    valore_culturale=row["valore_culturale"]
                )
                result[attrazione.id] = attrazione    #id dell ogg attrazione sarà la key del dict da aggiungere in result
        except Exception as e:                      #result = {}
            print(f"Errore durante la query get_attrazioni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
