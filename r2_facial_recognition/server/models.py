from typing import Callable
from flask_sqlalchemy import SQLAlchemy


# PyCharm fix, comment out below for production
class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    LargeBinary: Callable
    Text: Callable
    Table: Callable
    ForeignKey: Callable
    Boolean: Callable
    relationship: Callable
    backref: Callable


db = MySQLAlchemy()
# PyCharm fix, comment out above for production
# db = SQLAlchemy()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    facial_encoding = db.Column(db.LargeBinary, nullable=False)


class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)


MeetingPeople = db.Table(
    'meeting_people',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'),
              primary_key=True),
    db.Column('meetings_id', db.Integer, db.ForeignKey('meetings.id'),
              primary_key=True),
    db.Column('present', db.Boolean, nullable=False, default=False)
)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey(id), index=True)
    subgroups = db.relationship(lambda: Groups, backref=db.backref('parent'),
                                remote_side=id)


PeopleGroups = db.Table(
    'people_groups',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'),
              primary_key=True),
    db.Column('groups_id', db.Integer, db.ForeignKey('groups.id'),
              primary_key=True),
)


# TODO: Untested
def is_subgroup(potential_sub, potential_parent):
    current_node = potential_sub
    while potential_parent != current_node:
        current_node = Groups.query.get(current_node).first()
        if current_node is None:
            return False
    return True

