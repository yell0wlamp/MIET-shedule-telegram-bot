import telebot
import info
import check
import get

# variables
groups = dict()  # database of chats and groups assigned to them

# processing
if __name__ == "__main__":
    bot = telebot.TeleBot(info.bot_token)


    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        if message.text == '/help':
            help(message)
        elif message.text == '/set':
            set(message)
        elif message.text == '/today':
            today(message)
        elif message.text == '/nextday':
            nextday(message)
        elif message.text == '/week':
            week(message)
        elif message.text == '/nextweek':
            nextweek(message)


    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Это неофициальный бот для получения расписания МИЭТ-а\n"
                                          "Список комманд:\n"
                                          "/help - список комманд\n"
                                          "/set - выбор группы для чата\n"
                                          "/today - расписание на сегодня\n"
                                          "/nextday - расписание на завтра\n"
                                          "/week - расписание на неделю\n"
                                          "/nextweek расписание на следующую неделю\n"
                                          "Источник:https://miet.ru/schedule")


    @bot.message_handler(commands=['help'])
    def help(message):
        """send user list of commands"""
        bot.send_message(message.chat.id, "Список комманд:\n"
                                          "/help - список комманд\n"
                                          "/set - выбор группы для чата\n"
                                          "/today - расписание на сегодня\n"
                                          "/nextday - расписание на завтра\n"
                                          "/week - расписание на неделю\n"
                                          "/nextweek - расписание на следующую неделю\n")


    @bot.message_handler(commands=['set'])
    def set(message):
        """sets the group to chat with the user"""
        if message.text == '/set':
            bot.send_message(message.chat.id, "Введите группу:")
            bot.register_next_step_handler(message, get_group)


    def get_group(message):
        """converts the group to uppercase, checks for its presence in the list of groups and assigns it to this chat"""
        group = check.group(message.text)
        if group == 'error':
            bot.send_message(message.chat.id, "Группа не найдена, введите её в формате:\n"
                                              "ЭН-25, эн-25, УтС-21, уТс-21")
        else:
            m = 'Группа установлена:' + group
            bot.send_message(message.chat.id, m)
        groups[message.chat.id] = group
        print('\n', groups[message.chat.id])


    @bot.message_handler(commands=['today'])
    def today(message):
        """sends the user a schedule for today"""
        try:
            schedule = get.schedule_day(groups[message.chat.id], 0)
            bot.send_message(message.chat.id, schedule)
        except BaseException:
            bot.send_message(message.chat.id, 'ERROR')


    @bot.message_handler(commands=['nextday'])
    def nextday(message):
        """sends the user a schedule for tomorrow"""
        try:
            schedule = get.schedule_day(groups[message.chat.id], 1)
            bot.send_message(message.chat.id, schedule)
        except BaseException:
            bot.send_message(message.chat.id, 'ERROR')


    @bot.message_handler(commands=['week'])
    def week(message):
        """sends the user a schedule for the current week"""
        try:
            schedule = get.schedule_week(groups[message.chat.id], 0)
            bot.send_message(message.chat.id, schedule)
        except BaseException:
            bot.send_message(message.chat.id, 'ERROR')


    @bot.message_handler(commands=['nextweek'])
    def nextweek(message):
        """sends the user a schedule for the next week"""
        try:
            schedule = get.schedule_week(groups[message.chat.id], 1)
            bot.send_message(message.chat.id, schedule)
        except BaseException:
            bot.send_message(message.chat.id, 'ERROR')

    bot.polling(none_stop=True)
