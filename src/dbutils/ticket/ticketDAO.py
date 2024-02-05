import logging
import shortuuid
from flask import current_app
from datetime import datetime


logger = logging.getLogger('main.ticket_dao')


class TicketDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_TICKETS'])
            self.cur.execute(current_app.config['CREATE_TABLE_MESSAGE_FROM_HELPDESK'])
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb or exc_val or exc_type:
            return False
        self.cur.close()

    def create_new_ticket(self, d_id, c_id, title, description):
        t_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(current_app.config['INSERT_INTO_TICKETS_TABLE'], (t_id, d_id, c_id, title, description, current_app.config['RAISED'], datetime.now()))
        logger.info(f'New ticket raised with ticket_id:{t_id}, title:{title} by customer:{c_id}')
        return t_id

    def get_ticket_by_tid(self, t_id):
        self.cur.execute(current_app.config['GET_TICKET_BY_TID'], {
            't_id': t_id
        })
        return self.cur.fetchone()

    def get_all_tickets(self):
        self.cur.execute(current_app.config['VIEW_ALL_TICKETS'])
        return self.cur.fetchall()

    def update_message_from_helpdesk(self, message, t_id):

        self.cur.execute(current_app.config['GET_MESSAGE_FROM_HELPDESK'], {
            't_id': t_id
        })

        message_from_helpdesk = self.cur.fetchone()

        if message_from_helpdesk is None:
            mh_id = shortuuid.ShortUUID().random(5)
            self.cur.execute(current_app.config['INSERT_MESSAGE_FROM_HELPDESK'], (mh_id, message, datetime.now(), t_id))
            logger.info(f'Message from helpdesk created for ticket_id:{t_id}, message: {message}')

        else:
            self.cur.execute(current_app.config['UPDATE_MESSAGE_FROM_HELPDESK'], ({
                'message': message,
                'created_at': datetime.now(),
                't_id': t_id
            }))
            logger.info(f'Message from helpdesk updated for ticket_id:{t_id} to {message}')

    def get_message_from_helpdesk(self, t_id):
        self.cur.execute(current_app.config['GET_MESSAGE_FROM_HELPDESK'], {
            't_id': t_id
        })
        return self.cur.fetchone()

    def change_ticket_status(self, t_id, new_status):

        self.cur.execute(current_app.config['UPDATE_TICKET_STATUS'], {
            'status': new_status,
            't_id': t_id
        })
        logger.info(f'Ticket status changed for ticket_id:{t_id} to {new_status}')

    def assign_repr_id(self, t_id, e_id):
        self.cur.execute(current_app.config['ASSIGN_REPR'], {
            'repr_id': e_id,
            't_id': t_id
        })
        logger.info(f'ticket_id: {t_id} assigned to {e_id}')

    def get_detailed_ticket_view(self, t_id):
        self.cur.execute(current_app.config['TICKET_DETAIL_QUERY'], {
            't_id': t_id
        })
        return self.cur.fetchone()

    def get_all_tickets_by_c_id(self, c_id):
        self.cur.execute(current_app.config['GET_TICKETS_BY_CID'], {
            'c_id': c_id
        })
        return self.cur.fetchall()

    def get_tickets_by_c_id_and_status(self, c_id, status):
        self.cur.execute(current_app.config['VIEW_TICKETS_BY_CID_AND_STATUS'], {
            'c_id': c_id,
            'status': status
        })
        return self.cur.fetchall()

    def get_all_tickets_by_d_id(self, d_id):
        self.cur.execute(current_app.config['GET_TICKETS_BY_D_ID'], {
            'd_id': d_id
        })
        return self.cur.fetchall()

    def get_tickets_by_d_id_and_status(self, d_id, status):
        self.cur.execute(current_app.config['VIEW_TICKETS_BY_DID_AND_STATUS'], {
            'd_id': d_id,
            'status': status
        })
        return self.cur.fetchall()

    def get_tickets_by_status(self, status):
        self.cur.execute(current_app.config['GET_TICKETS_BY_STATUS'], {
            'status': status
        })
        return self.cur.fetchall()
