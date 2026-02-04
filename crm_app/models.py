from django.db import models
from ulid import new as ulid_new


def generate_ulid():
    return str(ulid_new())


class Employee(models.Model):
    ulid = models.CharField(max_length=26, default=generate_ulid, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.department}"

"""
    2. Attendance Management
        The application should allow the admin to :
            Mark attendance for an employee with :
                Date
                Status (present/absent)
            view attendance records for each employee
"""
class Attendance(models.Model):
    ulid = models.CharField(max_length=26, default=generate_ulid, unique=True, editable=False, primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')])