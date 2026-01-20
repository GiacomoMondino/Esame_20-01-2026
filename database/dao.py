from database.DB_connect import DBConnect
from model.artist import Artist
from model.collegamenti import Collegamento

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_n_maggiore_album(NumAlbum):

        conn = DBConnect.get_connection()
        artisti = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id as id, ar.name as name
                FROM album al, artist ar
                WHERE al.artist_id = ar.id
                GROUP BY al.artist_id
                HAVING COUNT(*) >= %s
                """
        cursor.execute(query, (NumAlbum, ))
        for row in cursor:
            if row['id'] not in artisti:
                artisti[row['id']] = Artist(**row)
        cursor.close()
        conn.close()
        return artisti

    @staticmethod
    def lista_get_artisti_n_maggiore_album(NumAlbum):

        conn = DBConnect.get_connection()
        artisti = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id as id, ar.name as name
                FROM album al, 
                     artist ar
                WHERE al.artist_id = ar.id
                GROUP BY al.artist_id
                HAVING COUNT(*) >= %s 
                """
        cursor.execute(query, (NumAlbum,))
        for row in cursor:
            if row['id'] not in artisti:
                artisti.append(row['id'])
        cursor.close()
        conn.close()
        return artisti

    @staticmethod
    def get_all_edges(NumAlbum, diz_artisti):

        conn = DBConnect.get_connection()
        collegamenti = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT LEAST(artist1.id,  artist2.id) as a1_id, 
                       GREATEST(artist1.id,  artist2.id) as a2_id, 
                       COUNT(*) as peso
                FROM (SELECT t.genre_id as genre_id, a.artist_id as id
                      FROM track t, album a
                      WHERE t.album_id = a.id
                      GROUP BY t.genre_id , a.artist_id) artist1, 
                    (SELECT t.genre_id as genre_id, a.artist_id as id
                      FROM track t, album a
                      WHERE t.album_id = a.id
                      GROUP BY t.genre_id , a.artist_id) artist2
                WHERE artist1.id <> artist2.id and artist1.genre_id = artist2.genre_id
                GROUP BY artist1.id,  artist2.id
                """
        cursor.execute(query)
        lista_artisti = DAO.lista_get_artisti_n_maggiore_album(NumAlbum)
        for row in cursor:
            if row['a1_id'] in lista_artisti and row['a2_id'] in lista_artisti:
                a1_object = diz_artisti.get(row['a1_id'])
                a2_object = diz_artisti.get(row['a2_id'])
                if a1_object is not None and a2_object is not None and (a1_object, a2_object) not in collegamenti:
                    collegamenti[a1_object, a2_object] = Collegamento(a1_object, a2_object, row['peso'])
        cursor.close()
        conn.close()
        return collegamenti

    @staticmethod
    def get_artisti():

        conn = DBConnect.get_connection()
        artisti = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT id ,name
                FROM artist
                """
        cursor.execute(query)
        for row in cursor:
            if row['id'] not in artisti:
                artisti[row['id']] = Artist(**row)
        cursor.close()
        conn.close()
        return artisti

    @staticmethod
    def get_artisti_canzone_min(durata_min, NumAlbum):

        conn = DBConnect.get_connection()
        artisti = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.id as id , ar.name as name
                FROM track t, album al, artist ar     
                WHERE (t.milliseconds/60000) > %s and al.id = t.album_id and ar.id = al.artist_id
                """
        cursor.execute(query, (durata_min,))
        for row in cursor:
            lista_artisti = DAO.lista_get_artisti_n_maggiore_album(NumAlbum)
            for row in cursor:
                if row['id'] in lista_artisti :
                    artisti[row['id']] = Artist(**row)
        cursor.close()
        conn.close()
        return artisti

