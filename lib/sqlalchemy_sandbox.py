#!/usr/bin/env python3

#imports
from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


#data models
class Student(Base):
    __tablename__ = 'students'

    #indexes are used to speed up lookups on certain column values. Use name because teachers/ administartors ar eunlikley to know a stuents ID
    Index('index_name', 'name')

    #Column provides a number of optional arguments to make code more "secure"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    #standard output value, in place of te obejct which is hard to distinguish/ read for humans
    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"


# if __name__ == '__main__':

#     engine = create_engine('sqlite:///:memory:')
#     Base.metadata.create_all(engine)

#     Session = sessionmaker(bind=engine)
#     session = Session()

#     albert_einstein = Student(
#         name="Albert Einstein",
#         email="albert.einstein@zurich.edu",
#         grade=6,
#         birthday=datetime(
#             year=1879,
#             month=3,
#             day=14
#         ),
#     )

#     session.add(albert_einstein)
#     #generates a statement to include in the session's transaction
#     session.commit()
#     #executes all statements in the transaction and saves any changes to the database. Also updatee the Student objetc with an id

#     print(f"New student ID is {albert_einstein.id}.")


if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )


    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")



    # #---query instance method
    # session.bulk_save_objects([albert_einstein, alan_turing])
    # session.commit()

    # students = session.query(Student)

    # print([student for student in students])




    # #---all instance method---
    # session.bulk_save_objects([albert_einstein, alan_turing])
    # session.commit()

    # students = session.query(Student).all()

    # print(students)



    # #---Specific columns---
    # session.bulk_save_objects([albert_einstein, alan_turing])
    # session.commit()
    
    # names = session.query(Student.name).all()
    # print(names)


    #---order---
    students_by_grade_desc = session.query(
        Student.name, Student.grade).order_by(
        desc(Student.grade)).all()

    print(students_by_grade_desc)


    #---limit to x number of records. 1 in this case---
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).limit(1).all()

    print(oldest_student)


    #---first is a quick way to limit to 1
    oldest_student = session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).first()

    print(oldest_student)


    #---func gives us access to common operations such as count and sum
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)


    #---filter typically has a column, standard operator and vbalue. Can be chained but can be fiddifult to read
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11).all()

    for record in query:
        print(record.name)


    
    #--- update() methd allows us to update records without creating objecs. In theis example move students all up one grade. Could do this y looping through but update more efficient

    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])


    # #---"manual" way ot update not using update()

    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # print([(student.name,
    #     student.grade) for student in session.query(Student)])


    # #---Delete
    # query = session.query(
    #     Student).filter(
    #         Student.name == "Albert Einstein")        

    # # retrieve first matching record as object
    # albert_einstein = query.first()

    # # delete record
    # session.delete(albert_einstein)
    # session.commit()

    # # try to retrieve deleted record
    # albert_einstein = query.first()

    # #---Or use delete method
    # query = session.query(
    #     Student).filter(
    #         Student.name == "Albert Einstein")

    # query.delete()

    # albert_einstein = query.first()

    # print(albert_einstein)
