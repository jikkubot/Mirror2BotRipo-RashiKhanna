from speedtest import Speedtest
from bot.helper.telegram_helper.filters import CustomFilters
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from telegram.ext import CommandHandler


def speedtest(update, context):
    speed = sendMessage("Running Speed Test . . . ", context.bot, update)
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    string_speed = f'''
<b>ð Server ð</b> 
<b>âï¸ Name :</b> <code>{result['server']['name']}</code>
<b>ð Country :</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
<b>ð³ Sponsor :</b> <code>{result['server']['sponsor']}</code>
<b>ð®ISP :</b> <code>{result['client']['isp']}</code>

<b>ð SpeedTest Results ð</b>
<b>ð¥ Upload :</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>ð¤ Download :</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>ð Ping :</b> <code>{result['ping']} ms</code>
<b>ð® ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    editMessage(string_speed, speed)


def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


SPEED_HANDLER = CommandHandler(BotCommands.SpeedCommand, speedtest, 
                                                  filters=CustomFilters.owner_filter | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(SPEED_HANDLER)
