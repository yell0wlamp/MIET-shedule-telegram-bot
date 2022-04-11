from datetime import datetime
from operator import attrgetter
import info
import connect


def define_day_number():
    """determines the numerator or denominator today"""
    week_based = datetime(2022, 2, 7).isocalendar()[1]
    week_today = datetime.today().isocalendar()[1]
    day_number = (week_today - week_based) % 4
    return day_number


def exact_time(number_of_lesson):
    """get exact time start and stop lesson as string"""
    if number_of_lesson[0] == '1':
        return '09:00-10:30'
    elif number_of_lesson[0] == '2':
        return '10:40-12:10'
    elif number_of_lesson[0] == '3':
        return '12:20-13:50 / 12:50-14:20'
    elif number_of_lesson[0] == '4':
        return '14:30-16:00'
    elif number_of_lesson[0] == '5':
        return '16:10-17:40'
    elif number_of_lesson[0] == '6':
        return '18:20-19:50'
    elif number_of_lesson[0] == '7':
        return '20:00-21:30'



def search_schedule(database, day, bias_week):
    """
    getting a schedule for one day
    :param database:
    :param bias_week: number of week to shift right
    :return: schedule for one day as list
    """
    # variables
    day_number = define_day_number() + bias_week  # day number from 0 before 3
    schedule = []
    # processing
    if day > 7:  # parameter bounds checking
        day = 1
        day_number += 1
        if day_number > 3:
            day_number = 0
    if day == 7:
        schedule.append(info.Lesson(7, 'time', 'room', 'Выходной', 'teacher'))
        return schedule
    for lesson in database['Data']:  # research schedule
        if lesson['Day'] == day:
            if lesson['DayNumber'] == day_number:
                # record schedule
                schedule.append(info.Lesson(lesson['Day'], lesson['Time']['Time'], lesson['Room']['Name'],
                                            lesson['Class']['Name'], lesson['Class']['TeacherFull']))
    schedule.sort(key=attrgetter('number'))
    return schedule


def schedule_day(name_of_group, bias_day):
    """
    change schedule type to string for one day
    :param bias_day: number of day to shift right
    :return: schedule for one day as string
    """
    database = connect.data(name_of_group)
    day = datetime.isoweekday(datetime.today()) + bias_day
    schedule = search_schedule(database, day, 0)
    schedule_string = ''
    if schedule[0].name == 'Выходной':
        return 'Выходной'
    elif schedule[0].name == 'Военная подготовка':
        return 'Военная подготовка'
    else:
        for lesson in schedule:
            schedule_string += lesson.number + ' ' + exact_time(lesson.number) + '\n' + lesson.room + '\n' + lesson.name + '\n' \
                               + lesson.teacher + '\n\n'
        return schedule_string


def schedule_week(name_of_group, bias_week):
    """
    change schedule type to string for one week
    :param bias_week: number of week to shift right
    :return: schedule for one week as string
    """
    database = connect.data(name_of_group)
    week = ['Понедельник:', 'Вторник:', 'Среда:', 'Четверг:', 'Пятница:', 'Суббота:']
    schedule_week_string = ''
    for day in range(1, 7):
        schedule = search_schedule(database, day, bias_week)
        schedule_week_string += '\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -' + '\n' \
                                + week[day - 1]
        if schedule[0].name == 'Военная подготовка':
            schedule_week_string += '\nВоенная подготовка'
        else:
            for lesson in schedule:  # change schedule type to string
                schedule_week_string += '\n' + lesson.number[0] + '. ' + lesson.room + '  ' + lesson.name + '  ' + \
                                        lesson.teacher + '\n'
        schedule.clear()
    return schedule_week_string
