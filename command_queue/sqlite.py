from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from command_queue.models import Base, Student, Change, Command


class SQLiteManager:
    """
    Manages the database connection and operations
    """
    def __init__(self, uri: str, worker_name: str):
        self.worker_name = worker_name
        self.engine = create_engine(uri, echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=self.engine)

    def get_session(self) -> Session:
        """
        Get a session from the database
        :return: Session object
        """
        return self.SessionLocal()

    def add_students(self, student1_data: dict, student2_data: dict):
        """
        Add two Student records to the database, with one being marked as merged with the other
        """
        with self.get_session() as session:
            student1 = Student(**student1_data)
            student2 = Student(**student2_data, merged_with_pidm=student1.pidm)
            session.add(student1)
            session.add(student2)
            session.commit()

    def add_change(self, student_pidm: str, description: str):
        """
        Add a Change record to a Student identified by PIDM
        """
        with self.get_session() as session:
            student = session.query(Student).filter_by(pidm=student_pidm).first()
            if student:
                change = Change(description=description, student=student)
                session.add(change)
                session.commit()
            else:
                print(f"Student with PIDM {student_pidm} not found.")

    def add_command(self, worker_id: str, detail: dict) -> int:
        """
        Add a Command record to the database
        """
        with self.get_session() as session:
            new_command = Command(worker_id=worker_id, **detail)
            session.add(new_command)
            session.commit()
            return new_command.id

    def get_next_command(self, worker_id: str) -> tuple[int, str, str, str, str] | None:
        """
        Get the next command from the queue
        :param worker_id: Worker ID
        :return: Command string
        """
        with (self.get_session() as session):
            command = session.query(Command).filter_by(
                worker_id=worker_id, result=None).first()
            if command:
                command.result = "processing"
                session.commit()
                return (int(command.id), str(command.page), str(command.tab),
                        str(command.action), str(command.value))
            return None

    def update_command(self, command_id: int, result: str):
        """
        Update the result of a command
        """
        with self.get_session() as session:
            command = session.query(Command).filter_by(id=command_id).first()
            if command:
                command.result = result
                session.commit()

    def clean_commands(self):
        """
        Clean all commands from the database
        """
        with self.get_session() as session:
            session.query(Command).delete()
            session.commit()
            print("Commands cleaned")
