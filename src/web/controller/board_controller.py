from collections import Counter

from src.web.model.board_model import PostModel
import pandas as pd
import  json
import matplotlib
class PostController:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.post_model = PostModel(db_host, db_user, db_password, db_name)

    def get_posts(self):
        return self.post_model.fetch_posts()

    def close_connection(self):
        self.post_model.close_connection()


def save_to_csv(posts, filename):
    # DataFrame 생성
    df = pd.DataFrame(posts, columns=['btitle', 'bcontent'])

    # DataFrame을 CSV로 저장
    df.to_csv(filename, index=False, encoding='utf-8')

if __name__ == "__main__":
    db_host = '127.0.0.1'
    db_user = 'root'
    db_password = '1234'
    db_name = 'doctoro'

################################################################################

    # # flask 에 내보내기
    # @app.route('/word/count',methods=['GET'])
    # def count_word():
    #     result = word_count()
    #     return result









