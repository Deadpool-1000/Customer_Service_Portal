import shortuuid
import logging
from datetime import datetime
from utils.named_tuples import Ticket

logger = logging.getLogger('main.ticket_dao')

CREATE_TABLE_TICKETS = """CREATE TABLE IF NOT EXISTS tickets (
    t_id TEXT PRIMARY_KEY,
    d_id TEXT NOT NULL,
    c_id TEXT NOT NULL,
    repr_id TEXT,
    title TEXT NOT NULL,
    desc TEXT NOT NULL,
    status TEXT NOT NULL,
    cust_feedback_id TEXT,
    created_on timestamp,
    message_from_admin TEXT
)"""
INSERT_INTO_TICKETS_TABLE = "INSERT INTO tickets(t_id, d_id, c_id, title, desc, status, created_on, message_from_admin) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
VIEW_TICKETS = "SELECT * FROM tickets WHERE c_id = ? AND status = ?"
VIEW_TICKETS_BY_STATUS = "SELECT * FROM tickets WHERE status = ? AND d_id = ?"
VIEW_ALL_TICKETS = "SELECT * FROM tickets ORDER BY created_on DESC"
UPDATE_MESSAGE_FROM_HELPDESK = "UPDATE tickets SET message_from_admin = ? WHERE t_id = ?"
IN_PROGRESS = "in_progress"
RAISED = "raised"
CLOSED = "closed"
UPDATE_TICKET_STATUS = "UPDATE tickets SET status=? WHERE t_id = ?"
WE_WILL_GET_BACK = "We will get back to you soon."
ASSIGN_REPR = "UPDATE tickets SET repr_id=? WHERE t_id=?"


class TicketDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(CREATE_TABLE_TICKETS)
            self.singleton -= 1

    def create_new_ticket(self, d_id, c_id, title, desc):
        t_id = shortuuid.ShortUUID().random(5)
        self.cur.execute(INSERT_INTO_TICKETS_TABLE, (t_id, d_id, c_id, title, desc, RAISED, datetime.now(), "We will get back to you soon."))

    def view_in_progress_ticket(self, c_id):
        rws = self.cur.execute(VIEW_TICKETS, (c_id, IN_PROGRESS)).fetchall()
        # 't_id' 'd_id', 'c_id', 'repr_id', 'title', 'description', 'status', 'cust_feedback', 'created_on', 'message_id'
        return self.prepare_tickets(rws)

    def view_closed_tickets(self, c_id):
        rws = self.cur.execute(VIEW_TICKETS, (c_id, CLOSED)).fetchall()
        return self.prepare_tickets(rws)

    def view_raised_tickets(self, c_id):
        rws = self.cur.execute(VIEW_TICKETS, (c_id, RAISED)).fetchall()
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
        rws = self.cur.execute(VIEW_TICKETS_BY_STATUS, (RAISED, dept_id))
        return self.prepare_tickets(rws)

    def view_all_in_progress_tickets(self, dept_id):
        rws = self.cur.execute(VIEW_TICKETS_BY_STATUS, (IN_PROGRESS, dept_id))
        return self.prepare_tickets(rws)

    def view_all_closed_tickets(self, dept_id):
        rws = self.cur.execute(VIEW_TICKETS_BY_STATUS, (CLOSED,dept_id))
        return self.prepare_tickets(rws)

    def view_all_tickets(self):
        rws = self.cur.execute(VIEW_ALL_TICKETS)
        return self.prepare_tickets(rws)

    def match_t_id_with_c_id(self, t_id, c_id):
        pass

    def update_message_from_helpdesk(self, message, t_id):
        logger.debug(f'message:{message} tid:{t_id}')
        self.cur.execute(UPDATE_MESSAGE_FROM_HELPDESK, (message, t_id))

    def change_ticket_status(self, t_id, new_status):
        self.cur.execute(UPDATE_TICKET_STATUS, (new_status, t_id))

    def assign_repr_id(self, t_id, e_id):
        self.cur.execute(ASSIGN_REPR, (e_id, t_id))

