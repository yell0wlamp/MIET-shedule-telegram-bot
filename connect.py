import requests


def data(name_of_group):
    """
    getting database from website
    :return: database of entered group
    """
    payload = {'group': name_of_group}
    response_db = requests.get('https://miet.ru/schedule/data', params=payload)
    if response_db:
        print('\n', 'Response Data OK:', response_db.status_code)
    else:
        print('\n', 'Response Data Failed:', response_db.status_code)
    db = response_db.json()
    return db


def groups():
    """
    getting list of group from website
    :return: list of group
    """
    response_groups = requests.get('https://miet.ru/schedule/groups')
    if response_groups:
        print('\n', 'Response groups OK:', response_groups.status_code)
    else:
        print('\n', 'Response groups Failed:', response_groups.status_code)
    names_of_groups = response_groups.json()
    return names_of_groups
