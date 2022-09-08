def bc(color=0):
    return f"\033[{color}m"


def print_ds(text):
    print(f"{bc(35)}Discord:{bc()} {text}")


def print_tg(text):
    text = text.replace(r"Z̜̫̣̼̠͓̈e̻̰̱̥ͥ̒ͅb̻̦͉͛̏̈́ͅǎ̭̲͕̍̂ͩr̻̰̾̓̅ͬͬo̩ͭ̇̏ͩ̾̄", "Zebaro")
    print(f"{bc(34)}Telegram:{bc()} {text}")
