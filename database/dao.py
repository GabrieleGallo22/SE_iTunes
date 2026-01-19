from database.DB_connect import DBConnect
from dataclasses import dataclass

@dataclass (frozen=True)
class Album:
    album_id: int
    title: str
    totD: float

    def __str__(self):
        return f"{self.title} - {self.totD}"


class DAO:
    @staticmethod
    def get_all_albums(min_duration):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT A.id, A.title, SUM(T.milliseconds) as totD
        
        FROM album A
        JOIN TRACK T ON A.id = T.album_id
        GROUP BY A.id, A.title
        HAVING SUM(T.milliseconds) >= %s 
         """

        min_duration = min_duration * (60 * 1000)
        cursor.execute(query, (min_duration,))

        for row in cursor:
            durata_minuti = row["totD"] / (60 * 1000)
            new_album = Album(row["id"], row["title"], durata_minuti)
            result.append(new_album)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_edges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=False)
        query = """ 
            SELECT DISTINCT T1.album_id, T2.album_id
            FROM playlist_track PT1
            JOIN track T1 ON T1.id = PT1.track_id
            JOIN playlist_track PT2 ON PT2.playlist_id = PT1.playlist_id
            JOIN track T2 ON T2.id = PT2.track_id
            WHERE T1.album_id < T2.album_id
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result