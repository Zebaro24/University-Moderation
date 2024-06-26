from logging import getLogger, INFO, FileHandler, Formatter, ERROR
from pytz import timezone
from datetime import datetime

telegram_error = 0
discord_error = 0
start_time = "Не задана"
tz = timezone("Europe/Kyiv")


def time_start_bot():
    global start_time
    start_time = str(datetime.now(tz))
    print(f"{bc(32)}<---Время запуска: {start_time}--->{bc()}")
    info(f"<---Время запуска: {start_time}--->")


def set_logger():
    setup_logger('info', "info.log")
    setup_logger('error', "error.log", ERROR, "\n")


def info(msg):
    if "\033[01;38;05;34m" in msg:
        msg = msg.replace("\033[01;38;05;34m", "")
    if "\033[0m" in msg:
        msg = msg.replace("\033[0m", "")
    getLogger("info").info(msg)


def exception(msg):
    global telegram_error, discord_error
    if msg == "Telegram":
        telegram_error += 1
    elif msg == "Discord":
        discord_error += 1

    getLogger("error").exception(msg)


def setup_logger(logger_name, log_file, level=INFO, end=""):
    logger = getLogger(logger_name)
    formatter = Formatter(f'{end}[%(asctime)s] : [%(levelname)s] : %(message)s')  # noqa
    file_handler = FileHandler(log_file, 'a', 'utf-8')
    file_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)


def bc(color=0):
    return f"\033[{color}m"


def print_ds(text):
    print(f"{bc(35)}Discord:{bc()} {text}")
    getLogger('info').info(f"[Discord] : {text}")


def print_tg(text):
    text = text.replace(r"Z̜̫̣̼̠͓̈e̻̰̱̥ͥ̒ͅb̻̦͉͛̏̈́ͅǎ̭̲͕̍̂ͩr̻̰̾̓̅ͬͬo̩ͭ̇̏ͩ̾̄", "Zebaro")
    print(f"{bc(34)}Telegram:{bc()} {text}")
    getLogger('info').info(f"[Telegram] : {text}")


def from_bytes(byte):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while byte >= 1024 and i < len(suffixes) - 1:
        byte /= 1024.
        i += 1
    f = ('%.2f' % byte).rstrip('0').rstrip('.')
    return f"{f} {suffixes[i]}"
