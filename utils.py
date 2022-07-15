def bc(color=0):
    return f"\033[{color}m"


def print_ds(text):
    print(f"{bc(32)}Discord:{bc()} {text}")


def print_tg(text):
    print(f"{bc(34)}Telegram:{bc()} {text}")
