from .models import Employee, Attendance
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import exceptionhandler
import json
from datetime import datetime


@csrf_exempt
@exceptionhandler
def AddEmployee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            full_name = data.get('fullName')
            email = data.get('email')
            department = data.get('department')
            
            if not full_name or not email or not department:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            if Employee.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Employee with this email already exists'}, status=400)
            
            employee = Employee(name=full_name, email=email, department=department)
            employee.save()
            
            return JsonResponse({
                'message': 'Employee added successfully',
                'employee': {
                    'ulid': str(employee.ulid),
                    'name': employee.name,
                    'email': employee.email,
                    'department': employee.department
                }
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@exceptionhandler
def EmployeeList(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        employee_list = [
            {
                'employeeId': str(emp.ulid),
                'fullName': emp.name,
                'email': emp.email,
                'department': emp.department
            }
            for emp in employees
        ]
        return JsonResponse(employee_list, safe=False, status=200)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@exceptionhandler
def DeleteEmployee(request, ulid):
    if request.method == 'DELETE':
        try:
            employee = Employee.objects.get(ulid=ulid)
            employee_name = employee.name
            employee.delete()
            return JsonResponse({'message': f'Employee {employee_name} deleted successfully'}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@exceptionhandler
def MarkAttendance(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    employee_ulid = data.get('employeeId')
    date_str = data.get('date')
    status = data.get('status', 'PRESENT').upper()

    if not employee_ulid or not date_str:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if status not in ['PRESENT', 'ABSENT']:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    try:
        employee = Employee.objects.get(ulid=employee_ulid)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    try:
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Date must be YYYY-MM-DD'}, status=400)

    # Check if attendance is already marked for this employee and date
    existing = Attendance.objects.filter(employee=employee, date=attendance_date).first()
    if existing:
        return JsonResponse({
            'message': 'Attendance already marked',
            'attendance': {
                'employee': employee.name,
                'date': str(attendance_date),
                'status': existing.status
            }
        }, status=200)

    # Mark attendance
    attendance = Attendance.objects.create(employee=employee, date=attendance_date, status=status)

    return JsonResponse({
        'message': 'Attendance marked successfully',
        'attendance': {
            'employee': employee.name,
            'date': str(attendance_date),
            'status': status
        }
    }, status=201)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@exceptionhandler
def ViewAttendance(request, ulid):
    if request.method == 'GET':
        try:
            employee = Employee.objects.get(ulid=ulid)
            attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
            
            records_list = [
                {'date': str(record.date), 'status': record.status}
                for record in attendance_records
            ]
            
            return JsonResponse({
                'employee': {
                    'employeeId': str(employee.ulid),
                    'fullName': employee.name,
                    'email': employee.email,
                    'department': employee.department
                },
                'attendanceRecords': records_list
            }, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)