import json
import pprint
from objects import Day, Group, DayController
print = pprint.PrettyPrinter(indent=4).pprint

d = json.loads(open("config.json", "r", encoding = "utf-8").read())

def make_lessons_time(lessons):
    return dict((n+1, {"start_at": i, "lesson":{"group":None, "name":None, "type": None}}) for n, i in enumerate(lessons.values()))

#print()

def make_schedule(d):
    day_controller = DayController(d['available_days'], d['auditory'], d['start_at'])
    for group in d['group_list']:
        g = Group(group, d['group'][group]['studying_at'], d['group'][group]['max_lesson_per_day'], d['group'][group]['lessons'], day_controller)
        #for lesson_name, lesson_data in d['group'][group]['lessons'].items():
        #    pass
        g.make_schedule()
        #g.show_schedule()

    day_controller.show_schedule()
    #day_controller.save_to_table()

make_schedule(d)
