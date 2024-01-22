import logging
import shortuuid
from datetime import datetime

from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.data_containers.named_tuples import Ticket
from src.utils.exceptions.exceptions import NoMessageFromHelpdeskException, NoTicketsException, NoMessageFromManagerException

logger = logging.getLogger('main.ticket_dao')


class TicketDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_TICKETS)
            self.cur.execute(QueriesConfig.CREATE_TABLE_MESSAGE_FROM_HELPDESK)
            self.cur.execute(QueriesConfig.CREATE_TABLE_MESSAGE_FROM_MANAGER)
            self.singleton -= 1

    def create_new_ticket(self, d_id, c_id, title, desc):
        t_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(QueriesConfig.INSERT_INTO_TICKETS_TABLE, (t_id, d_id, c_id, title, desc, DBConfig.RAISED, datetime.now()))
        logger.info(f'New ticket raised with ticket_id:{t_id}, title:{title} by customer:{c_id}')

    def get_in_progress_tickets_with_cid(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.IN_PROGRESS)).fetchall()
        # 't_id' 'd_id', 'c_id', 'repr_id', 'title', 'description', 'status', 'cust_feedback', 'created_on', 'message_id'
        in_progress_tickets_by_c_id = [dict(r) for r in rws.fetchall()]

        if len(in_progress_tickets_by_c_id) == 0:
            raise NoTicketsException('No tickets to show.')

        return in_progress_tickets_by_c_id

    def get_closed_tickets_by_cid(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.CLOSED)).fetchall()
        closed_tickets_by_c_id = [dict(r) for r in rws.fetchall()]

        if len(closed_tickets_by_c_id) == 0:
            raise NoTicketsException('No tickets to show.')

        return closed_tickets_by_c_id

    def get_raised_tickets_by_cid(self, c_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS, (c_id, DBConfig.RAISED)).fetchall()
        raised_tickets_by_c_id = [dict(r) for r in rws.fetchall()]

        if len(raised_tickets_by_c_id) == 0:
            raise NoTicketsException('No tickets to show.')

        return raised_tickets_by_c_id

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

    def get_all_raised_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.RAISED, dept_id))
        raised_tickets = [dict(r) for r in rws.fetchall()]

        if len(raised_tickets) == 0:
            raise NoTicketsException('No tickets to show.')

        return raised_tickets

    def get_all_in_progress_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.IN_PROGRESS, dept_id))
        in_progress_tickets = [dict(r) for r in rws.fetchall()]

        if len(in_progress_tickets) == 0:
            raise NoTicketsException('No tickets to show.')

        return in_progress_tickets

    def get_all_closed_tickets(self, dept_id):
        rws = self.cur.execute(QueriesConfig.VIEW_TICKETS_BY_STATUS, (DBConfig.CLOSED, dept_id))
        closed_tickets = [dict(r) for r in rws.fetchall()]

        if len(closed_tickets) == 0:
            raise NoTicketsException('No tickets to show.')

        return closed_tickets

    def get_all_tickets(self):
        rws = self.cur.execute(QueriesConfig.VIEW_ALL_TICKETS)
        all_tickets = [dict(r) for r in rws.fetchall()]

        if len(all_tickets) == 0:
            raise NoTicketsException('No tickets to show.')

        return all_tickets

    def update_message_from_helpdesk(self, message, t_id):
        mh_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(QueriesConfig.UPDATE_MESSAGE_FROM_HELPDESK, (mh_id, message, datetime.now(), t_id))
        logger.info(f'Message from helpdesk changed for ticket_id:{t_id} to {message}')

    def get_message_from_helpdesk(self, t_id):
        rws = self.cur.execute(QueriesConfig.GET_MESSAGE_FROM_HELPDESK)
        message_from_helpdesk = [dict(r) for r in rws.fetchall()]

        if len(message_from_helpdesk) == 0:
            raise NoMessageFromHelpdeskException('No message from helpdesk yet.')

        return message_from_helpdesk

    def change_ticket_status(self, t_id, new_status):
        self.cur.execute(QueriesConfig.UPDATE_TICKET_STATUS, (new_status, t_id))
        logger.info(f'Ticket status changed for ticket_id:{t_id} to {new_status}')

    def assign_repr_id(self, t_id, e_id):
        self.cur.execute(QueriesConfig.ASSIGN_REPR, (e_id, t_id))
        logger.info(f'ticket_id:{t_id} assigned to {e_id}')

    def is_ticket_closed(self, t_id):
        rws = self.cur.execute(QueriesConfig.IS_TICKET_CLOSED, (t_id, DBConfig.CLOSED))
        return len(rws.fetchall()) != 0

    def update_message_from_manager(self, t_id, message):
        mm_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(QueriesConfig.UPDATE_MESSAGE_FROM_MANAGER, (mm_id, message, datetime.now(), t_id))
        logger.info(f'Message from manager for ticket_id:{t_id} updated')

    def get_message_from_manager(self, t_id):
        rws = self.cur.execute(QueriesConfig.GET_MESSAGE_FROM_MANAGER)
        message_from_manager = [dict(r) for r in rws.fetchall()]

        if len(message_from_manager) == 0:
            raise NoMessageFromManagerException('No message from manager yet.')

        return message_from_manager
