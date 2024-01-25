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
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_TICKETS)
            self.cur.execute(QueriesConfig.CREATE_TABLE_MESSAGE_FROM_HELPDESK)
            self.cur.execute(QueriesConfig.CREATE_TABLE_MESSAGE_FROM_MANAGER)
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb or exc_val or exc_type:
            return False

        self.cur.close()

    def create_new_ticket(self, d_id, c_id, title, description):
        t_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(QueriesConfig.INSERT_INTO_TICKETS_TABLE, (t_id, d_id, c_id, title, description, DBConfig.RAISED, datetime.now()))
        logger.info(f'New ticket raised with ticket_id:{t_id}, title:{title} by customer:{c_id}')
        return t_id

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

    def get_ticket_by_tid(self, t_id):
        self.cur.execute(QueriesConfig.GET_TICKET_BY_TID, {
            't_id': t_id
        })
        return self.cur.fetchone()

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
        self.cur.execute(QueriesConfig.VIEW_ALL_TICKETS)
        return self.cur.fetchall()

    def update_message_from_helpdesk(self, message, t_id):

        self.cur.execute(QueriesConfig.GET_MESSAGE_FROM_HELPDESK, {
            't_id': t_id
        })

        message_from_helpdesk = self.cur.fetchone()

        print(message_from_helpdesk)

        if message_from_helpdesk is None:
            mh_id = shortuuid.ShortUUID().random(5)
            self.cur.execute(QueriesConfig.INSERT_MESSAGE_FROM_HELPDESK, (mh_id, message, datetime.now(), t_id))
            logger.info(f'Message from helpdesk created for ticket_id:{t_id}, message: {message}')

        else:
            self.cur.execute(QueriesConfig.UPDATE_MESSAGE_FROM_HELPDESK, ({
                'message': message,
                'created_at': datetime.now(),
                't_id': t_id
            }))
            logger.info(f'Message from helpdesk updated for ticket_id:{t_id} to {message}')

    def get_message_from_helpdesk(self, t_id):
        rws = self.cur.execute(QueriesConfig.GET_MESSAGE_FROM_HELPDESK)
        message_from_helpdesk = [dict(r) for r in rws.fetchall()]

        if len(message_from_helpdesk) == 0:
            raise NoMessageFromHelpdeskException('No message from helpdesk yet.')

        return message_from_helpdesk

    def change_ticket_status(self, t_id, new_status):

        self.cur.execute(QueriesConfig.UPDATE_TICKET_STATUS, {
            'status': new_status,
            't_id': t_id
        })
        logger.info(f'Ticket status changed for ticket_id:{t_id} to {new_status}')

    def assign_repr_id(self, t_id, e_id):
        self.cur.execute(QueriesConfig.ASSIGN_REPR, {
            'repr_id': e_id,
            't_id': t_id
        })
        logger.info(f'ticket_id: {t_id} assigned to {e_id}')

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

    def get_detailed_ticket_view(self, t_id):
        self.cur.execute(QueriesConfig.TICKET_DETAIL_QUERY, {
            't_id': t_id
        })
        return self.cur.fetchone()

    def get_all_tickets_by_c_id(self, c_id):
        self.cur.execute(QueriesConfig.GET_TICKETS_BY_CID, {
            'c_id': c_id
        })
        return self.cur.fetchall()

    def get_all_tickets_by_d_id(self, d_id):
        self.cur.execute(QueriesConfig.GET_TICKETS_BY_D_ID, {
            'd_id': d_id
        })
        return self.cur.fetchall()

