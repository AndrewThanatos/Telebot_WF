from code.models import db, User


def isinDataBase(user_id):
    return User.query.filter_by(user_id=user_id).first() is not None


def add_User(user_id):
    user = User(
        user_id=user_id,
        city_name=None,
        country=None,
        state=None,
        coords=None,
        degree_unit='celsius'
    )
    db.session.add(user)
    db.session.commit()


def change_City(user_id, new_name):
    user = User.query.filter_by(user_id=user_id).first()
    user.city_name = new_name
    db.session.commit()


def change_County(user_id, new_name):
    user = User.query.filter_by(user_id=user_id).first()
    user.country = new_name
    db.session.commit()


def change_State(user_id, new_name):
    user = User.query.filter_by(user_id=user_id).first()
    user.state = new_name
    db.session.commit()


def change_Coords(user_id, new_coords):
    user = User.query.filter_by(user_id=user_id).first()
    user.coords = new_coords
    db.session.commit()


def change_Unit(user_id, new_unit):
    user = User.query.filter_by(user_id=user_id).first()
    user.degree_unit = new_unit
    db.session.commit()


def get_City(user_id):
    return User.query.filter_by(user_id=user_id).first().city_name


def get_Country(user_id):
    return User.query.filter_by(user_id=user_id).first().country


def get_State(user_id):
    return User.query.filter_by(user_id=user_id).first().state


def get_Coords(user_id):
    return User.query.filter_by(user_id=user_id).first().coords


def get_Unit(user_id):
    return User.query.filter_by(user_id=user_id).first().degree_unit
