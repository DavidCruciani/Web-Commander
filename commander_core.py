import subprocess
import datetime
import markdown

import sqlite3
cur = sqlite3.connect('webcommander.db',check_same_thread=False)



def run_command_core(command, term_num, flag):
    # sudo chown root:root ttyecho && sudo chmod u+s ttyecho

    try: 
        cur.execute("UPDATE Command set last_run=? WHERE name=?", (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),command))
        cur.commit()
        # conn.commit()
    except Exception as e: 
        print(f"Error: {e}")
    

    if flag:
        command_base = ['./ttyecho', f"/dev/pts/{term_num}"]
    else:
        command_base = ['./ttyecho', '-n', f"/dev/pts/{term_num}"]
    command_base.append(command)

    subprocess.call(command_base)

def delete_command_core(command):
    try:
        cur.execute("DELETE FROM Command WHERE name=?", (command,))
        cur.commit()
        # conn.commit()
        return True
    except Exception as e: 
        print(f"Error: {e}")
        return False

def add_command_core(command, category):
    cursor = cur.execute("SELECT id FROM Command WHERE name=?", (command.rstrip(),))
    if not cursor:
        try: 
            cur.execute("INSERT INTO Command (name,id_cat) VALUES (?,?)", (command.rstrip(),category))
            cur.commit()
            # conn.commit()
        except Exception as e: 
            print(f"Error: {e}")


def add_category_core(category):
    try: 
        cur.execute("INSERT INTO Category (name) VALUES (?)", (category,))
        cur.commit()
        # conn.commit()
    except Exception as e: 
        print(f"Error: {e}")

def delete_command_core(command):
    try:
        cur.execute("DELETE FROM Command WHERE name=?", (command,))
        cur.commit()
        # conn.commit()
        return True
    except Exception as e: 
        print(f"Error: {e}")
        return False

def delete_category_core(category):
    try:
        loc_list = list()
        cursor = cur.execute("SELECT id FROM Category WHERE name=?", (category,))
        for id in cursor:
            loc_list.append(id)
        
        cur.execute("UPDATE Command SET id_cat=0 WHERE id_cat=?", (loc_list[0][0],))
        cur.execute("DELETE FROM Category WHERE name=?", (category,))
        cur.commit()
        # conn.commit()
        return True
    except Exception as e: 
        print(f"Error delete: {e}")
        return False


def get_command_core(cat = dict()):
    if not cat:
        command_list = list()
        cursor = cur.execute("SELECT name,last_run,id_note FROM Command")
        for (name, last_run, id_note) in cursor:
            loc = ""
            if not last_run:
                loc = "Never Launch yet"
            else:
                # print(last_run)
                # loc = last_run.strftime('%Y-%m-%d %H:%M:%S')
                loc=last_run
            note = get_notes_core(id_note)
            command_list.append((name, loc, [id_note, markdown.markdown(note)]))
    else:
        command_list = list()
        cursor = cur.execute(f"SELECT name, last_run, id_note FROM Command WHERE Command.id_cat = {cat['cat']}")
        for (name, last_run, id_note) in cursor:
            loc = ""
            if not last_run:
                loc = "Never Launch yet"
            else:
                loc = last_run.strftime('%Y-%m-%d %H:%M:%S')
            note = get_notes_core(id_note)
            command_list.append((name, loc, [id_note, markdown.markdown(note)]))

    return command_list

def get_notes_core(id_note):
    notes_list = ""
    cursor = cur.execute("SELECT note FROM Notes WHERE id=(?)", (str(id_note),))
    for c in cursor:
        notes_list = c
    return notes_list[0]

def save_note_core(id, note):
    try:
        cur.execute("UPDATE Notes set note=? WHERE id=?", (note,id))
        cur.commit()
        return True
    except Exception as e: 
        print(f"Error: {e}")
    return False

def get_category_core():
    categ_list = list()
    cursor = cur.execute("SELECT name FROM Category")
    for name in cursor:
        categ_list.append(name)
    return categ_list

def get_categ_core():
    categ_list = list()
    cursor = cur.execute("SELECT id, name FROM Category")
    for (id, name) in cursor:
        categ_list.append((id, name))
    return categ_list

def get_cat_by_id(id):
    cat_name = ""
    cursor = cur.execute(f"SELECT name FROM Category WHERE id={id}")
    for name in cursor:
        cat_name = name
    return cat_name[0]