import mysql.connector

class PostModel:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234',
            database='doctoro',
        )

    def fetch_posts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT btitle, bcontent FROM board")
        rows = cursor.fetchall()
        # 딕셔너리 리스트로 변환
        posts = [{"btitle": row[0], "bcontent": row[1]} for row in rows]
        cursor.close()

        return posts  # 딕셔너리 리스트 반환

        print(posts)
    def close_connection(self):
        self.connection.close()