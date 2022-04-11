bot_token = "YOUR BOT TOKEN"

class Lesson:
    def __init__(self, day, number, room, name, teacher):
        self.day = 0
        self.number = number  # format: 1 пара
        self.room = room
        self.name = name
        self.teacher = teacher

    def print_lesson(self):
        print('\n', self.number, '\n', self.room, '\n', self.name, '\n', self.teacher)












