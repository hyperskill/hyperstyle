class Student:

    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year


student_name = Student(input(), input(), input())
print(student_name.name[0])
