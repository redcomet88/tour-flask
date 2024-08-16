from . import ma
from .models import Tour, User


class TourSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tour
        load_instance = True

tour_schema = TourSchema()
tours_schema = TourSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ChartData(ma.Schema):
    class Meta:
        fields = ('name', 'value')

chart_schema = ChartData(many=True)