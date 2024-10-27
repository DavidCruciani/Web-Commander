from ..db_class.db import *


def search_in_docs_title(title) -> list:
    glob_list = []
    splitted_title = title.split(" ")
    all_doc = Documentation.query.all()
    for doc in all_doc:
        if all(t.lower() in doc.title.lower() for t in splitted_title):
            glob_list.append(doc.to_json())
    return glob_list
    # loc = Documentation.query.where(Documentation.title.contains(title)).all()
    # if loc:
    #     return [doc.to_json() for doc in loc]
    # return []
    
def search_in_commands_title(title) -> list:
    glob_list = []
    splitted_title = title.split(" ")
    all_command = Command.query.all()
    for command in all_command:
        if all(t.lower() in command.title.lower() for t in splitted_title):
            glob_list.append(command.to_json())
    return glob_list
    # loc = Command.query.where(Command.title.contains(title)).all()
    # if loc:
    #     return [com.to_json() for com in loc]
    # return []