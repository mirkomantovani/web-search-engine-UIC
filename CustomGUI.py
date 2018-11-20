import easygui as eg


def ask_query():
    msg = "Enter your query"
    title = "Query"
    # field_names = ["Query"]
    # fieldValues = []  # we start with blanks for the values
    # fieldValues = eg.multenterbox(msg, title, field_names)
    response = eg.enterbox(msg, title)
    return response
