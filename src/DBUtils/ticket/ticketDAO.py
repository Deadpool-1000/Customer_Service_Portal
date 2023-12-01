import logging
from datetime import datetime

import shortuuid

from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.data_containers.named_tuples import Ticket

logger = logging.getLogger('main.mock_ticket_dao')


class TicketDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_TICKETS)
            self.singleton -= 1

    def create_new_ticket(self, d_id, c_id, title, desc):
        t_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(QueriesConfig.INSERT_INTO_TICKETS_TABLE, (t_id, d_id, c_id, title, desc, DBConfig.RAISED, datetime.now(), "We will get back to you soon."))
        logger.info(f'New ticket raised with ticket_id:{t_id}, title:{title} by customer:{c_id}')

    def view_in_progress_ticket(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.IN_PROGRESS)).fetchall()
        # 't_id' 'd_id', 'c_id', 'repr_id', 'title', 'description', 'status', 'cust_feedback', 'created_on', 'message_id'
        return self.prepare_tickets(rws)

    def view_closed_tickets(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.CLOSED)).fetchall()
        return self.prepare_tickets(rws)

    def view_raised_tickets(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.RAISED)).fetchall()
        return self.prepare_tickets(rws)

    @staticmethod
    def prepare_tickets(rws):
        all_tickets = [
            Ticket(
                t_id=row[0],
                d_id=row[1],
                c_id=row[2],
                repr_id=row[3],
                title=row[4],
                description=row[5],
                status=row[6],
                cust_feedback=row[7],
                created_on=row[8],
                message=row[9]
            )
            for row in rws]
        return all_tickets

    def view_all_raised_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.RAISED, dept_id))
        return self.prepare_tickets(rws)

    def view_all_in_progress_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.IN_PROGRESS, dept_id))
        return self.prepare_tickets(rws)

    def view_all_closed_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.CLOSED, dept_id))
        return self.prepare_tickets(rws)

    def view_all_tickets(self):
        rws = self.cur.execute(QueriesConfig.VIEW_ALL_TICKETS)
        return self.prepare_tickets(rws)

    def update_message_from_helpdesk(self, message, t_id):
        self.cur.execute(QueriesConfig.UPDATE_MESSAGE_FROM_HELPDESK, (message, t_id))
        logger.info(f'Message from helpdesk changed for ticket_id:{t_id} to {message}')

    def change_ticket_status(self, t_id, new_status):
        self.cur.execute(QueriesConfig.UPDATE_TICKET_STATUS, (new_status, t_id))
        logger.info(f'Ticket status changed for ticket_id:{t_id} to {new_status}')

    def assign_repr_id(self, t_id, e_id):
        self.cur.execute(QueriesConfig.ASSIGN_REPR, (e_id, t_id))
        logger.info(f'ticket_id:{t_id} assigned to {e_id}')
