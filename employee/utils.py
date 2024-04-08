from django.utils import timezone
# from datetime import datetime, time, timezone
from django.utils import timezone as tz
from datetime import datetime, time, timezone, timedelta
import pytz

from employee.models import Attendance

def calculate_average_hours_for_current_month(user):
    # Get the current month's first and last dates
    today = tz.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = today.replace(day=1, month=today.month % 12 + 1, hour=0, minute=0, second=0, microsecond=0) - tz.timedelta(days=1)

    # Filter Attendance records for the current month for the user
    attendances = Attendance.objects.filter(user=user, date__range=[first_day_of_month, last_day_of_month])

    # Calculate total working hours for each day and sum up
    total_working_hours = 0
    for attendance in attendances:
        if attendance.check_out:
            working_hours = (attendance.check_out - attendance.check_in).total_seconds() / 3600  # Convert seconds to hours
            total_working_hours += working_hours

    # Calculate the number of working days in the month
    number_of_working_days = len(attendances)

    # Calculate the average hours
    if number_of_working_days > 0:
        average_hours = total_working_hours / number_of_working_days
    else:
        average_hours = 0

    # Convert average hours to hh:mm format
    hours = int(average_hours)
    minutes = int((average_hours - hours) * 60)
    average_hours_formatted = "{:02d}h {:02d}m".format(hours, minutes)

    return average_hours_formatted

def calculate_average_checkout_time_for_current_month(user):
    # Get the current month's first and last dates
    today = tz.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = today.replace(day=1, month=today.month % 12 + 1, hour=0, minute=0, second=0, microsecond=0) - tz.timedelta(days=1)

    # Filter Attendance records for the current month for the user
    attendances = Attendance.objects.filter(user=user, date__range=[first_day_of_month, last_day_of_month])
    # print(attendances)
    datetime_list = [x.check_out for x in attendances if x.check_out]
    print(datetime_list)
    total_hour = sum(dt.hour for dt in datetime_list)
    total_minute = sum(dt.minute for dt in datetime_list)
    total_second = sum(dt.second for dt in datetime_list)

    # Calculate the average time
    num_datetimes = len(datetime_list)
    average_hour = total_hour // num_datetimes
    average_minute = total_minute // num_datetimes
    average_second = total_second // num_datetimes

    # Construct a new datetime object using the average time
    average_datetime = datetime(2024, 4, 7, average_hour, average_minute, average_second, tzinfo=timezone.utc)

    print("Average time:", average_datetime.time())
    target_timezone = timezone(timedelta(hours=5, minutes=30))
    converted_datetime = average_datetime.astimezone(target_timezone)
    return converted_datetime.strftime("%I:%M %p")
    

def calculate_average_checkin_time_for_current_month(user):
    # Get the current month's first and last dates
    today = tz.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month % 12 + 1) - timedelta(days=1)

    # Filter Attendance records for the current month for the user
    attendances = Attendance.objects.filter(user=user, date__range=[first_day_of_month, last_day_of_month])
    datetime_list = [x.check_in for x in attendances if x.check_in]

    # Calculate the total time for each component
    total_hour = sum(dt.hour for dt in datetime_list)
    total_minute = sum(dt.minute for dt in datetime_list)
    total_second = sum(dt.second for dt in datetime_list)

    # Calculate the average time
    num_datetimes = len(datetime_list)
    average_hour = total_hour // num_datetimes
    average_minute = total_minute // num_datetimes
    average_second = total_second // num_datetimes

    # Construct a new datetime object using the average time
    average_datetime = datetime(2024, 4, 7, average_hour, average_minute, average_second, tzinfo=timezone.utc)

    # Convert the average datetime to Indian Standard Time (+05:30)
    target_timezone = tz.timedelta(hours=5, minutes=30)
    converted_datetime = average_datetime.astimezone(tz=tz.timezone(target_timezone))
    
    return converted_datetime.strftime("%I:%M %p")

def percent_count_checkins_within_10_minutes(user):
    # Get the current month's first and last dates
    IST = pytz.timezone('Asia/Kolkata')
    today = tz.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month % 12 + 1) - timedelta(days=1)

    # Calculate the time range 10 minutes before and after 10 AM
    ten_am_minus_10_minutes = time(9, 50)  # 10 AM - 10 minutes
    ten_am_plus_10_minutes = time(10, 10)  # 10 AM + 10 minutes

    # Filter Attendance records for the current month for the user
    attendances = Attendance.objects.filter(user=user, date__range=[first_day_of_month, last_day_of_month])
    for i in attendances:
        print(i.check_in.astimezone(IST).time(), i.date, ten_am_plus_10_minutes)
    # Count the number of check-ins within the time range
    count_checkins = sum(
        ten_am_minus_10_minutes <= attendance.check_in.astimezone(IST).time() <= ten_am_plus_10_minutes
        for attendance in attendances
        if attendance.check_in
    )
    percent = (count_checkins / attendances.count())*100


    return percent

def get_dates_excluding_sunday_monday():
    # Get the current month's first and last dates
    today = datetime.now()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today

    # Initialize the list to store the dates
    dates_list = []

    # Iterate through all the dates of the current month
    current_date = first_day_of_month
    while current_date <= last_day_of_month:
        # Exclude Sundays (6) and Mondays (0)
        if current_date.weekday() not in [6, 0]:  # 6 is Sunday, 0 is Monday
            dates_list.append(current_date)
        current_date += timedelta(days=1)

    return dates_list

def count_checkins(user):
    # Get the current month's first and last dates
    IST = pytz.timezone('Asia/Kolkata')
    today = tz.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = first_day_of_month.replace(month=first_day_of_month.month % 12 + 1) - timedelta(days=1)

    # Calculate the time range 10 minutes before and after 10 AM
    ten_am_minus_10_minutes = time(9, 50)  # 10 AM - 10 minutes
    ten_am_plus_10_minutes = time(10, 10)  # 10 AM + 10 minutes

    # Filter Attendance records for the current month for the user
    attendances = Attendance.objects.filter(user=user, date__range=[first_day_of_month, last_day_of_month])
    # Count the number of check-ins within the time range
    count_checkins_on_time = sum(
        ten_am_minus_10_minutes <= attendance.check_in.astimezone(IST).time() <= ten_am_plus_10_minutes
        for attendance in attendances
        if attendance.check_in
    )
    count_checkins_early = sum(
        attendance.check_in.astimezone(IST).time() < ten_am_minus_10_minutes
        for attendance in attendances
        if attendance.check_in
    )
    count_checkins_late = sum(
        ten_am_plus_10_minutes < attendance.check_in.astimezone(IST).time()
        for attendance in attendances
        if attendance.check_in
    )
    total_days = len(get_dates_excluding_sunday_monday())
    data = {
        "count_checkins_on_time": count_checkins_on_time,
        "count_checkins_early": count_checkins_early,
        "count_checkins_late": count_checkins_late,
        "total_checkedin": attendances.count(),
        "absent": total_days - attendances.count(),
        "total": total_days
    }
    print(get_dates_excluding_sunday_monday())


    return data