import shortuuid
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.data_containers.named_tuples import Feedback
from src.utils.exceptions.exceptions import NoFeedbackExistsException


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
        if rws is None:
            return []
        return self.format_feedback(rws)

    def get_feedback_by_tid(self, t_id):
        # (f_id, stars, description, t_id)
        rws = self.cur.execute(QueriesConfig.GET_FEEDBACK_BY_TID, (t_id,))
        feedback = [dict(row) for row in rws.fetchall()]
        if len(feedback) == 0:
            raise NoFeedbackExistsException('Currently, no feedback exists.')
        return feedback[0]

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
