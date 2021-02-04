from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///list.db')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
menu_text = '''
1) Today's activity
2) Week's activity
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
'''


def add_task():
    task = input('Enter activity\n')
    deadline = input('Enter deadline\n')
    new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def print_tasks(day, rows, inline_date=False):
    if inline_date is True:
        for row in rows:
            print(f'{row.id}. {row}. {row.deadline.strftime("%d %b")}')
    else:
        print(day.strftime('%A %d %b:'))
        if len(rows) == 0:
            print('Nothing to do!')
            return
        for row in rows:
            print(f'{row.id}. {row}')


def make_list_of_week_dates(start_day):
    dates = list()
    for i in range(0, 7):
        new_day = start_day + timedelta(days=i)
        dates.append(new_day)
    return dates


def print_missed_tasks():
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    if len(rows) != 0:
        print_tasks(today, rows)
        return
    print('Nothing is missed!')


while True:
    command = input(menu_text)
    today = datetime.today()
    if command == '0':
        print('Bye!')
        break
    if command == '1':
        # today's tasks
        table_rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print_tasks(today, table_rows)
    if command == '2':
        # week's tasks
        days = make_list_of_week_dates(today)
        for week_day in days:
            table_rows = session.query(Table).filter(Table.deadline == week_day.date()).all()
            print_tasks(week_day, table_rows)
            print()
    if command == '3':
        # all tasks
        table_rows = session.query(Table).all()
        print_tasks(today, table_rows, inline_date=True)
    if command == '4':
        # missed tasks
        table_rows = session.query(Table).filter(Table.deadline < today.date()).all()
        print_tasks(today, table_rows, inline_date=True)
    if command == '5':
        add_task()
    if command == '6':
        # delete task
        print('Chose the number of the task you want to delete:')
        table_rows = session.query(Table).all()
        print_tasks(today, table_rows, inline_date=True)
        task_num = int(input())
        session.delete(table_rows[task_num])
        session.commit()
