from src.DBUtils.connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO


class NewTicketHandler:
    @staticmethod
    def create_ticket(d_id, c_id, title, description):
        with DatabaseConnection() as conn:

            with TicketDAO(conn) as t_dao:
                t_dao.create_new_ticket(d_id, c_id, title, description)

