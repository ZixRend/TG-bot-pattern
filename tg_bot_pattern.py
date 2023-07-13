from telegram.ext import Updater, CommandHandler
'''MessageHandler для текста'''
from datetime import datetime as dt
from codecs import open as c_open
from os import *
from traceback import format_exc as error

'''
Installation
pip3 install python-telegram-bot==13.15
pip3 install datetime
'''

'''
ZIX BOT PATTERN

* LOG + ERROR LOG + LOGS
* WHITELIST
* AUTO ENVIRONMENT
* SEND FUNCS
* START AND HELP

'''

bot_name = ''
token = ''


def main():
    global bot_name, token

    def error_log(e, update):
        if update == 'Extra_case': nick, msg = 'ZixRend', 'Extra_case'
        else:
            nick = ''
            if str(update.message.from_user.username) != "None": nick += f'@{str(update.message.from_user.username)}'
            nick += ' ' + str(update.message.from_user.id)
            if nick[0] == ' ': nick = nick[1:]
            msg = str(update.message.text)

        temp_log = f'Error at {str(dt.now())}\n{str(e)}\nfrom {nick} because of {msg}\n'
        temp_log.replace('\n', chr(8000)).replace("/", "|")
        with c_open(f'e_log_{bot_name}/{str(dt.now())}_e_log_{bot_name}.txt', 'w+', 'utf-8') as e_log:
            e_log.write(temp_log)

        if int(dt.now().hour) in set(list(range(4))) | {23}:
            data = sorted(listdir(f'e_log_{bot_name}'))
            if len(data) > 9000:
                deleter = data[:(len(data) - 1000)]
                for i in deleter: remove(f'e_log_{bot_name}/' + i)

    def log(update, status):
        try:
            if update != 'Extra_case':
                message, nick = str(update.message.text), ''
                if str(update.message.from_user.username) != "None":
                    nick += f'@{str(update.message.from_user.username)}'
                nick += f' {update.message.from_user.id}'
                if nick[0] == ' ': nick = nick[1:]
            else:
                message = 'Admin command'
                nick = 'unknown user'

            temp_log = f'{str(dt.now())} {nick} ✐ {message} ✐ {status}'.replace("\n", " ")
            makedirs(f'log_{bot_name}/{temp_log.replace("/", "|")}')

            if int(dt.now().hour) in set(list(range(4))) | {23}:
                data = sorted(next(walk(f'log_{bot_name}'))[1])
                if len(data) > 9000:
                    deleter = data[:(len(data) - 1000)]
                    for i in deleter: rmdir(f'log_{bot_name}/' + i)
        except: error_log(error(), update)

    def sends_parse(update, context, text_send):
        if str(update.message.reply_to_message) != 'None' and str(
                update.message.reply_to_message.from_user.id) == '777000':
            while True:
                try:
                    context.bot.send_message(chat_id=update.message.chat_id, text=text_send, parse_mode="Markdown",
                                             reply_to_message_id=update.message.reply_to_message.message_id)
                except:
                    error_log(error(), update)
                else:
                    break
        else:
            while True:
                try:
                    context.bot.send_message(chat_id=update.message.chat_id, text=text_send, parse_mode="Markdown")
                except:
                    error_log(error(), update)
                else:
                    break

    def sends(update, context, text_send):
        if str(update.message.reply_to_message) != 'None' and str(
                update.message.reply_to_message.from_user.id) == '777000':
            while True:
                try:
                    context.bot.send_message(chat_id=update.message.chat_id, text=text_send,
                                             reply_to_message_id=update.message.reply_to_message.message_id)
                except:
                    error_log(error(), update)
                else:
                    break
        else:
            while True:
                try:
                    context.bot.send_message(chat_id=update.message.chat_id, text=text_send)
                except:
                    error_log(error(), update)
                else:
                    break

    def w_list(update):
        with c_open(f'{bot_name}_whitelist.txt') as white_list: vip_list = {i.strip() for i in white_list}
        return str(update.message.from_user.id) in vip_list

    def logs(update, context):
        try:
            context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)
        except:
            pass

        if w_list(update):
            deleter = list(filter(lambda x: path.isfile(x) and f'log_{bot_name}_' in x, listdir()))
            for i in deleter: remove(i)

            data = sorted(next(walk(f'log_{bot_name}'))[1])
            temp = f'log_{bot_name}_{str(dt.now())}.txt'

            with c_open(temp, 'w+', 'utf-8') as writer:
                writer.write('\n'.join(data))

            with c_open(temp, 'rb') as log_doc:
                context.bot.send_document(chat_id=update.message.chat_id, document=log_doc)

            deleter = list(filter(lambda x: path.isfile(x) and f'e_log_{bot_name}_' in x, listdir()))
            for i in deleter: remove(i)

            data = sorted(listdir(f'e_log_{bot_name}'))
            log_name = f'e_log_{bot_name}_{str(dt.now())}.txt'
            temp_log = []
            for i in data:
                with c_open(f'e_log_{bot_name}/{i}') as e_log: temp_log.append(e_log.read())
            temp_log = '\n\n'.join(sorted(temp_log))

            with c_open(log_name, 'w+', 'utf-8') as writer:
                writer.write(temp_log)

            with c_open(log_name, 'rb') as log_doc:
                context.bot.send_document(chat_id=update.message.chat_id, document=log_doc)
        else:
            error_log('Wrong User trying admin command!', update)

    def add_w_list(update, context):
        try:
            context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)
        except:
            pass
        if w_list(update):
            user_id = str(update.message.reply_to_message.from_user.id)
            if user_id == 'None':
                text_send = 'Используйте команду только в ответ на сообщения, тех кого хотите добавить в whitelist!'
                sends(update, context, text_send)
            else:
                with c_open(f'{bot_name}_whitelist.txt') as white_list:
                    vip_list = {i.strip() for i in white_list} | {user_id}
                with c_open(f'{bot_name}_whitelist.txt', 'w+') as white_list:
                    white_list.write('\n'.join(list(vip_list)))
                username = update.message.reply_to_message.from_user.first_name
                text_send = f'[{username}](tg://user?id={user_id}) добавлен в whitelist!'
                sends_parse(update, context, text_send)
        else:
            error_log('Wrong User trying admin command!', update)

    def sends_except(update, context):
        if str(update.message.reply_to_message) != "None":
            if str(update.message.reply_to_message.from_user.id) == "777000":
                try:
                    try:
                        context.bot.send_message(chat_id=update.message.chat_id,
                                    text="Дайте боту права администратора, для большего удобства при использовании.",
                                    reply_to_message_id=update.message.reply_to_message.message_id)
                    except:
                        context.bot.send_message(chat_id=update.message.chat_id,
                                    text="Дайте боту права администратора, для большего удобства при использовании.")
                except: error_log(error(), update)
            else:
                try:
                    context.bot.send_message(chat_id=update.message.chat_id,
                                    text="Дайте боту права администратора, для большего удобства при использовании.")
                except: error_log(error(), update)
        else:
            try:
                context.bot.send_message(chat_id=update.message.chat_id,
                                    text="Дайте боту права администратора, для большего удобства при использовании.")
            except: error_log(error(), update)

    def bad_user(update, context):
        if str(update.message.from_user.id) == "1087968824":
            try:
                context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)
            except:
                sends_except(update, context)
            sends(update, context, "Для использования бота необходимо не использовать анонимность в группе канала.")
            log(update, 'Successful')
        elif str(update.message.reply_to_message) != "None":
            if str(update.message.reply_to_message.from_user.id) == "1087968824":
                try:
                    context.bot.deleteMessage(message_id=update.message.message_id,
                                              chat_id=update.message.chat_id)
                except:
                    sends_except(update, context)
                sends(update, context, "Невозможно взаимодействовать с анонимом")
                log(update, 'Successful')
            else:
                error_log('Wrong User!', update)
        else:
            error_log('Wrong User!', update)

    def starter(update, context):
        try: context.bot.deleteMessage(message_id=update.message.message_id, chat_id=update.message.chat_id)
        except: pass
        sends_parse(update, context, f'[Hello World!](http://t.me/{bot_name}?startgroup=true)')
        log(update, '200')

    updater = Updater(f'{token}', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', starter, run_async=True))
    dp.add_handler(CommandHandler('logs', logs, run_async=True))
    dp.add_handler(CommandHandler('add_wlist', add_w_list, run_async=True))

    '''
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, inside_commands, run_async=True))
    для текстовых команд
    '''

    while True:
        try:
            updater.start_polling()
            updater.idle()
        except:
            error_log(error(), 'Extra_case')


'''env check and launch'''
while True:
    try:
        if __name__ == '__main__':
            if not path.exists(f'{bot_name}_whitelist.txt'):
                with c_open(f'{bot_name}_whitelist.txt', 'w+') as vip_list:
                    vip_list.write('1067702645')
            if not path.exists(f'e_log_{bot_name}'): mkdir(f'e_log_{bot_name}')
            if not path.exists(f'log_{bot_name}'): mkdir(f'log_{bot_name}')
            main()
    except: pass