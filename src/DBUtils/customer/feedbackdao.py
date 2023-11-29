import shortuuid

from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.data_containers.named_tuples import Feedback


class FeedbackDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_FEEDBACK)
            self.singleton -= 1

    def add_feedback(self, stars, desc, t_id):
        f_id = shortuuid.ShortUUID().random(length=5)
        self.cur.execute(QueriesConfig.INSERT_INTO_TICKETS, (f_id, stars, desc, t_id))

    def get_feedback(self):
        rws = self.cur.execute(QueriesConfig.GET_ALL_FEEDBACK).fetchall()
        if len(rws) == 0:
            return []
        return self.format_feedback(rws)

    @staticmethod
    def format_feedback(rws):
        return [
            Feedback(
                f_id=row[0],
                stars=row[1],
                desc=row[2],
                t_id=row[3]
            )
            for row in rws
        ]
