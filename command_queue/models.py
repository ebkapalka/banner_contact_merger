from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

Base = declarative_base()


class Student(Base):
    """
    Represents a student in the database.
    """
    __tablename__ = 'students'
    pidm = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    gid = Column(String, unique=True, nullable=False)
    merged_with_pidm = Column(String, ForeignKey('students.pidm'), nullable=True)
    merged_with = relationship('Student', remote_side=[pidm],
                               backref='merged_by', uselist=False)
    changes = relationship('Change', back_populates='student')


class Change(Base):
    """
    Represents changes made to a student's record.
    """
    __tablename__ = 'changes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_pidm = Column(String, ForeignKey('students.pidm'))
    action = Column(String(128))  # "delete", "add", "skipped"
    value = Column(String(512), nullable=True)
    result = Column(String(512), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    student = relationship('Student', back_populates='changes')


class Command(Base):
    """
    Represents a command in the queue to be processed by workers, with timestamps for tracking.
    """
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(String(128))
    page = Column(String(128), nullable=True)
    tab = Column(String(128), nullable=True)
    action = Column(String(128), nullable=False)
    value = Column(String(512), nullable=False)
    result = Column(String(512), nullable=True)
    added_timestamp = Column(DateTime, server_default=func.now())
    result_updated_timestamp = Column(
        DateTime, nullable=True, onupdate=func.now(), server_default=None)
