# General Information

- Language: Python
- Framework: Django and Django REST Framework (DRF)
- Database: PostgreSQL
- Asynchronous Tasks: Celery + Redis
- Authentication: JWT (JSON Web Token)

## Modules and Structure

- CustomUser:
  - A custom user model extending Django's AbstractBaseUser.
  - Allows users to log in using email.
  - Key Fields:
    - annual_leave_days: Total annual leave days for the user.
    - remaining_leave_days: Remaining leave days.
    - used_leave_days: Used leave days.
    - total_late_minutes: Total minutes of lateness.
    - monthly_working_hours: Total working hours for the current month.
  - Relationships:
    - worklog: Many-to-Many relationship with WorkLog.
    - leaverequest: Many-to-Many relationship with LeaveRequest.
- WorkLog:
  - Stores daily check-in/check-out records for users.
  - Fields:
    - date: Represents the workday.
    - check_in_time and check_out_time: Check-in and check-out times.
    - late_minutes: Daily late minutes.
    - total_worked_hours: Total daily worked hours.
- LeaveRequest:
  - Manages annual leave requests for users.
  - Fields:
    - start_date and end_date: Start and end dates of the leave.
    - status: Status of the leave (pending, approved, rejected).
  - Relationships:
    - Many-to-Many relationship with CustomUser.
- Notification:
  - Sends notifications to administrators.
  - Fields:
    - user: The user who will receive the notification (admin).
    - message: Notification content.
    - created_at: Notification creation timestamp.

## Celery Tasks

- send_notification_to_admin:
  - Sends notifications to admins if a user's remaining leave days fall below 3.
  - Prevents duplicate notifications by checking existing entries.
- calculate_monthly_reports:
  - Calculates users' monthly working hours and lateness.
  - Deducts lateness from annual leave days.

# API Endpoints

## User Management

- List Users

  - URL: /api/users/
  - Method: GET
  - Permissions: Admins only.
  - Description: Lists all users.
  - Create User

  - URL: /api/users/
  - Method: POST
  - Permissions: Admins only.
  - Body Example:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "Ali",
  "last_name": "Veli",
  "is_manager": false,
  "is_employee": true
}
```

- User Details

  - URL: /api/users/<id>/
  - Method: GET
  - Permissions: Admins only.
  - Description: Retrieves details of a specific user.

## Attendance Management

- Daily Summary

  - URL: /api/worklog/daily-summary/
  - Method: GET
  - Permissions: All users.
  - Description: Retrieves a summary of the user's daily work logs.

- Check In

  - URL: /api/worklog/check-in/
  - Method: POST
  - Permissions: All users.
  - Description: Creates a check-in record for the user.

- Check Out
  - URL: /api/worklog/check-out/
  - Method: POST
  - Permissions: All users.
  - Description: Creates a check-out record for the user.

## Leave Request Management

- List Leave Requests

  - URL: /api/leaverequest/leave-requests/
  - Method: GET
  - Permissions: Employees can view their requests; managers can view all.
  - Description: Lists leave requests.

- Create Leave Request
  - URL: /api/leaverequest/
  - Method: POST
  - Permissions: Employees only.
  - Body Example:

```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-10"
}
```

- Approve Leave Request

  - URL: /api/leaverequest/<id>/approve/
  - Method: POST
  - Permissions: Managers only.
  - Description: Approves a specific leave request.

- Reject Leave Request
  - URL: /api/leaverequest/<id>/reject/
  - Method: POST
  - Permissions: Managers only.
  - Description: Rejects a specific leave request.

## Notification Management

- List Notifications
  - URL: /api/notifications/
  - Method: GET
  - Permissions: Admins only.
  - Description: Lists notifications sent to administrators.
  - Model Relationships
  - CustomUser → WorkLog: Many-to-Many.
  - CustomUser → LeaveRequest: Many-to-Many.
  - Notification → CustomUser: ForeignKey.
  - Authentication
  - JWT Usage:
  - Obtain tokens using the /api/token/ endpoint:

```

{
"email": "user@example.com",
"password": "password123"
}
```

- Response example:

```

{
"access": "ACCESS_TOKEN",
"refresh": "REFRESH_TOKEN"
}
```

- Permission Requirements:

  - Employees can view their leave requests and work logs.
  - Managers can view all users, leave requests, and notifications.

## Running the Project with Docker

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml run web python manage.py makemigrations
docker-compose -f docker-compose.yml run web python manage.py migrate
docker-compose -f docker-compose.yml up
```

# Notes:

- I will do native language that:

```bash
Enviroment olarak database baglantilarini tutmak icin ugrasmadim sonuc olarak bir production mantigi soz konusu degil burada sizler icin rahatlik olmasi icin direk docker icerisinde bulunuyor.
Yalniz SECRET_KEY i tutmak durumunda kaldim bilginize.
Zevkli bir projeydi saygilarimi sunarim.
Saygilarimi sunarim!
```
