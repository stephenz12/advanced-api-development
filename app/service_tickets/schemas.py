from app.extensions import ma
from app.models import ServiceTicket
from app.mechanics.schemas import MechanicSchema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = ma.Nested(MechanicSchema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
