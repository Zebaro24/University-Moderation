import psycopg2
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
from utils import bc
from time import perf_counter

admins = {}
teachers = {}
calendar = {}
edit_data = []
default_l = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
default_p = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}
control_sound = {}

conn = None
cursor = None


def db_run(execute):
    global conn, cursor
    if not conn:
        before = perf_counter()
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cursor = conn.cursor()
        print(f"{bc(32)}<База данных была подключена за: {round(perf_counter() - before, 2)} cек>{bc()}")

    cursor.execute(execute + ";")
    if execute[:6] == "SELECT":
        res = cursor.fetchall()
        return res
    else:
        conn.commit()


def load_control_sound(db_select, save_dict):
    row_dict = db_run(db_select)
    for i in row_dict:
        save_dict[i[0]] = {"mute": i[1], "deaf": i[2]}


def load_default_timetable(db_select, save_dict):
    row_dict = db_run(db_select)
    for i in row_dict:  # (0, 'Химия', 'Физика', 'Инф/Англ II', 'Физ-ра', 'Укр лит', 'История', 'Укр м', None, None)
        kol_none = 0
        for b in i[1:]:
            kol_none += 1
            if b is not None:
                save_dict[i[0]][kol_none] = b


def load_moderators(db_select, save_dict):
    row_dict = db_run(db_select)
    for i in row_dict:
        edit_data.append(i[2])
        if i[1] is None:
            save_dict[i[0]] = None
        else:
            save_dict[i[0]] = {"action": i[1], "date": i[2]}


def load_calendar(db_select, save_dict):
    row_dict = db_run(db_select)
    for i in row_dict:
        try:
            save_dict[i[0]][i[1]] = [i[2], i[3]]
        except KeyError:
            save_dict[i[0]] = {}
            save_dict[i[0]][i[1]] = [i[2], i[3]]


def load_all_elements():
    load_control_sound("SELECT * FROM control_sound", control_sound)

    load_moderators("SELECT * FROM admin", admins)
    load_moderators("SELECT * FROM teacher", teachers)

    load_default_timetable("SELECT * FROM default_l ORDER BY day", default_l)
    load_default_timetable("SELECT * FROM default_p ORDER BY day", default_p)

    load_calendar("SELECT * FROM owner ORDER BY day, int", calendar)
    print(f"{bc(32)}<Данные из базы данных были загружены>{bc()}")
