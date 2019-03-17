import json
import pprint
from objects import Day, Group, DayController
print = pprint.PrettyPrinter(indent=4).pprint

d = json.loads(open("config.json", "r", encoding = "utf-8").read())

def make_lessons_time(lessons):
    return dict((n+1, {"start_at": i, "lesson":{"group":None, "name":None, "type": None}}) for n, i in enumerate(lessons.values()))

#print()

def make_schedule(d):
    days = {}
    days_list = []
    #print(d['auditory'])
    lessons_time = d['start_at']
    #auditory_controller = Auditories(d['auditory'], d['available_days'], lessons_time)
    day_controller = DayController(d['available_days'], d['auditory'], d['start_at'])
    for group in d['group_list']:
        g = Group(group, d['group'][group]['studying_at'], d['group'][group]['max_lesson_per_day'], d['group'][group]['lessons'], day_controller)
        #for lesson_name, lesson_data in d['group'][group]['lessons'].items():
        #    pass
        g.make_schedule()

    day_controller.show_schedule()
    day_controller.save_to_table()

    '''
    for i in auditory_controller.audit:
        print(i)
        print('\n')
        for i in g.get_labas():
            print(i)
        print('\n')
        for i in g.get_practices():
            print(i)'''
    '''sch = Schedule(d['available_days'], lessons_time, d['auditory'])
    for group in d['group_list']:
        for lesson_name, lesson_data in d['group'][group]['lessons'].items():
            for i in range(0, lesson_data['laba']['count'], 1):
                print(sch.add_lesson_to_schedule(0, 1, 'random', group, lesson_name, 'laba'))
            for i in range(0, lesson_data['lection']['count'], 1):
                print(sch.add_lesson_to_schedule(0, 1, 'random', group, lesson_name, 'lection'))
            for i in range(0, lesson_data['practice']['count'], 1):
                print(sch.add_lesson_to_schedule(0, 1, 'random', group, lesson_name, 'practice'))
    #sch.add_lesson_to_schedule(0, 1, 404, 'kn-323', 'Проектування програмних систем', 'laba')
    for i in sch.get_denominator():
        print(i)
        print('\n\n')
        print(i.get_group_lessons_count('kn-323'))
    for i in sch.get_numerator():
        print(i)

        print(i.get_group_lessons_count('kn-323'))'''
    '''monday = sch.get_day(0, 0)
    monday.add_lesson(1, 404, 'kn-323', 'Проектування програмних систем', 'laba')
    monday.add_lesson(1, 303, 'kn-323', 'Моделювання систем', 'lection')
    print(monday)'''
    '''for i in sch.get_denominator():
        print(i.get_all_schedule())
        print(i.have_group('kn-323'))
    for i in sch.get_numerator():
        print(i.get_all_schedule())'''

    '''for i in d['available_days']:
        auditory_dict = {}
        for num, data in d['auditory'].items():
            #print(num)
            #print(data)
            data.update({"lessons": make_lessons_time(lessons_time)})
            auditory_dict.update(
            {num: data}
            )
        days.update({i: auditory_dict})
    for i in days_list:
        print(str(i))
    #print(days)
    for group in d['group_list']:
        studying_days = d['group'][group]['studying_at']
        max_lection_per_day = d['group'][group]['max_lesson_per_day']
        print(studying_days)
        print(max_lection_per_day)
        for lesson_name, lesson_data in d['group'][group]['lessons'].items():
            print(lesson_name)
            print(lesson_data)
            for i in range(0, lesson_data['laba']['count'], 1):
                #print('laba')
                print(add_lesson(days, studying_days, lesson_name, group, 'laba', lesson_data['laba']['per_day']))
                for study_day in studying_days:
                    if days[study_day]:
                        for room in days[study_day].keys():
                            #print(room)
                            for time in days[study_day][room]['lessons']:
                                if days[study_day][room]['lessons'][time]['lesson']['group'] is None:
                                    days[study_day][room]['lessons'][time]['lesson']['group'] = group
                                    days[study_day][room]['lessons'][time]['lesson']['name'] = lesson_name
                                    break
            for i in range(0, lesson_data['lection']['count'], 1):
                #print('lection')
                print(add_lesson(days, studying_days, lesson_name, group, 'lection', lesson_data['lection']['per_day']))
            for i in range(0, lesson_data['practice']['count'], 1):
                #print('practice')
                print(add_lesson(days, studying_days, lesson_name, group, 'practice', lesson_data['practice']['per_day']))
    #print(days)'''

def add_lesson(days, studying_days, lesson_name, group_name, lesson_type, per_day):
    print('per day')
    print(per_day)
    for study_day in studying_days:
        print(study_day)
        print(lesson_name)
        for room in days[study_day].keys():
            #print(room)
            for time in days[study_day][room]['lessons']:
                if days[study_day][room]['lessons'][time]['lesson']['group'] is None:
                    days[study_day][room]['lessons'][time]['lesson']['group'] = group_name
                    days[study_day][room]['lessons'][time]['lesson']['name'] = lesson_name
                    days[study_day][room]['lessons'][time]['lesson']['type'] = lesson_type
                    return True
                elif days[study_day][room]['lessons'][time]['lesson']['group'] == group_name and days[study_day][room]['lessons'][time]['lesson']['name'] == lesson_name and days[study_day][room]['lessons'][time]['lesson']['type'] == lesson_type:
                    return True




make_schedule(d)
