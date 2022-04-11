import connect


def group(name_of_group):
    """
    checking if the group is in the list
    :return: group name in upper case or error message
    """
    name_group_upp = name_of_group.upper()
    groups = connect.groups()
    for i in groups:
        if name_group_upp == i:
            return name_group_upp
    return 'error'
