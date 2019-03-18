import random
import textwrap
import xlsxwriter

##############
class Group(object):
    def __init__(self, name, study_at, max_lesson_per_day, lessons, day_controller):
        self.name = name
        self.study_at = study_at
        self.max_lesson_per_day = max_lesson_per_day
        self.lessons_lection = [Lesson(lesson_name, self.name, 'lection', lesson['lection']['count'], lesson['lection']['per_day']) for lesson_name, lesson in lessons.items()]
        self.lessons_laba = [Lesson(lesson_name, self.name, 'laba', lesson['laba']['count'], lesson['laba']['per_day']) for lesson_name, lesson in lessons.items()]
        self.lessons_practice = [Lesson(lesson_name, self.name, 'practice', lesson['practice']['count'], lesson['practice']['per_day']) for lesson_name, lesson in lessons.items()]
        self.all_lessons = [*self.lessons_lection, *self.lessons_laba, *self.lessons_practice]
        self.day_controller = day_controller
        self.schedule = dict((day_name, {}) for day_name in study_at)


    def get_lections(self):
        return self.lessons_lection

    def get_labas(self):
        return self.lessons_laba

    def get_practices(self):
        return self.lessons_practice

    def make_schedule(self):
        cur = 1
        for lesson in self.all_lessons:
            cur = self.day_controller.add_lesson(lesson, self.max_lesson_per_day, cur)


class Lesson(object):
    def __init__(self, name, group, type, count, per_day):
        self.name = name
        self.group = group
        self.type = type
        self.count = count
        self.per_day = per_day
        self.auditory = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        shortened = textwrap.shorten(text=self.name, width=50, placeholder = '...')
        return "Lesson: {} Group: {} Type: {}".format(shortened, self.group, self.type)

class DayController(object):
    def __init__(self, available_days, available_auditory, lessons_time):
        self.available_days = available_days
        self.lessons_time = lessons_time
        self.auditory = available_auditory
        self.days_denominator = [Day(self, name, 0, available_auditory, lessons_time, available_days) for name in available_days]
        self.days_numerator = [Day(self, name, 1, available_auditory, lessons_time, available_days) for name in available_days]
        #for i in self.days_denominator:
        #    print(i)

    def add_lesson(self, lesson, max_lesson_per_day, current):
        offset = 0
        list_day = self.get_day(offset)
        #print(day)
        for i in range(lesson.count):
            #print(i+1)
            current = 0 if current == 1 else 1
            day = None
            if (current)==0:
                day = list_day[0]
                #print(day)
                lesson_day = day.get_group_lesson_count(lesson.group)
                while(lesson_day >= max_lesson_per_day):
                    offset += 1
                    list_day = self.get_day(offset)
                    day = list_day[0]
                    #print(day)
                    lesson_day = day.get_group_lesson_count(lesson.group)

                day.add_lesson(lesson)
                    #print(lesson_day)
            else:
                day = list_day[1]
                lesson_day = day.get_group_lesson_count(lesson.group)
                while(lesson_day >= max_lesson_per_day):
                    offset += 1
                    list_day = self.get_day(offset)
                    day = list_day[1]
                    #print(day)
                    lesson_day = day.get_group_lesson_count(lesson.group)

                day.add_lesson(lesson)
            #print(day)

        return current

    def get_day(self, offset):
        #print(offset)
        return [self.days_denominator[offset], self.days_numerator[offset]]

    def get_day_denom(self, offset):
        return self.days_denominator[offset]

    def get_day_numer(self, offset):
        return self.days_numerator[offset]

    def show_schedule(self):
        for d, n in zip(self.days_denominator, self.days_numerator):
            print(d, n)
            #print()
            #print(i.get_group_lesson_count('kn-323'))

    def save_to_table(self, path = 'test.xlsx'):
        workbook = xlsxwriter.Workbook(path)

        worksheet_denom = workbook.add_worksheet('denominator')

        row = 0
        col = 0

        for day in self.available_days:
            worksheet_denom.write(row, col, day)
            worksheet_denom.set_column(row, col, 20)
            row += 1

        workbook.close()

class Day(object):
    def __init__(self, father, day_name, type, au_dict, lessons_time, available_days):
        self.father = father
        self.name = day_name
        self.type = type #0 - знаменник 1 - чисельник
        self.auditories = [Auditory(self, num, data['seats_number'], data['board'], lessons_time) for num, data in au_dict.items()]#dict((n+1, {"start_at": i, "lesson":{"group":None, "name":None, "type": None, "auditory": None}}) for n, i in enumerate(lessons_time.values()))
        self.this_day_auditory = []

    def add_lesson(self, lesson):
        audit = self.get_auditory()
        lesson_at_athis_day = self.get_group_lesson_count(lesson.group)
        #print(lesson_at_athis_day)
        res = audit.add_lesson(lesson, lesson_at_athis_day + 1)
        while(res == False):
            #print(res)
            audit = self.get_auditory()
            res = audit.add_lesson(lesson, lesson_at_athis_day + 1)

    def get_group_lesson_count(self, group_name):
        count = 0
        for i in self.get_auditories():
            for t in i.schedule:
                if i.schedule[t]['lesson'] is not None:
                    if i.schedule[t]['lesson'].group == group_name:
                        count += 1
        return count

    def get_auditories(self):
        return self.auditories

    def get_auditory(self):
        return random.choice(self.auditories)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        to = ''
        for i in self.get_auditories():
            to += '\t'+str(i)
            #print(self.day_schedule[i])
            #if self.day_schedule[i]['lesson']['group'] is not None:
            #    to += "\t"+str(i)+" "+self.day_schedule[i]['lesson']['group']+" "+self.day_schedule[i]['lesson']['name']+" "+self.day_schedule[i]['lesson']['auditory'].number+" "+self.day_schedule[i]['lesson']['type']+"\n"

        return "Day: {}\t{}\n{}".format(self.name, "Знаменник" if self.type == 0 else "Чисельник", to)

class Auditory(object):
    def __init__(self, father, number, seats_number, board, lessons_time):
        self.father = father
        self.number = number
        self.seats_number = seats_number
        self.board = board
        self.schedule = dict((n+1, {"start_at": i, "lesson": None}) for n, i in enumerate(lessons_time.values()))

    def add_lesson(self, lesson, para_number = 1):
        '''for i in self.schedule:
            if self.schedule[i]['lesson'] is None:
                self.schedule[i]['lesson'] = lesson
                return i'''
        if para_number<6:
            if self.schedule[para_number]['lesson'] is None:
                self.schedule[para_number]['lesson'] = lesson
                return para_number
            else:
                return False#self.add_lesson(lesson,para_number+1)
        '''l_count = self.get_lesson_count()
        self.schedule[l_count+1]['lesson'] = lesson
        return l_count+1'''

    def get_lesson_count(self):
        count = 0
        for i in self.schedule:
            if self.schedule[i]['lesson'] is not None:
                count += 1

        return count


    def __repr__(self):
        return "Auditory: {}".format(self.number)

    def __str__(self):
        to = ''
        for i in self.schedule:
            if self.schedule[i]['lesson'] is not None:
                to += "\t\t"+str(i)+" "+self.schedule[i]['lesson'].group+" "+str(self.schedule[i]['lesson'])+"\n"
        return "Auditory: {} seats: {} board: {}\n{}".format(self.number, self.seats_number, self.board, to)
