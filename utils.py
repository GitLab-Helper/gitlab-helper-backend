def project_mapping(project):
    return {
        'id': project.id,
        'name': project.name,
        'name_with_namespace': project.name_with_namespace,
        'web_url': project.web_url
    }


def board_list_mapping(board_list):
    return {
        'id': board_list.id,
        'label': board_list.label,
        'position': board_list.position
    }


def board_mapping(board):
    return {
        'id': board.id,
        'lists': [board_list_mapping(board_list) for board_list in board.lists.list()],
    }


def group_mapping(group, boards=None):
    return {
        'id': group.id,
        'web_url': group.web_url,
        'name': group.name,
        'projects': [project_mapping(project) for project in group.projects.list()],
        'boards': [board_mapping(board) for board in boards] if boards is not None else []
    }


def group_list_mapping(group):
    return {
        'id': group.id,
        'web_url': group.web_url,
        'name': group.name,
    }


def label_color(labels: list, position_letter: str) -> str:
    for label in labels:
        if label[0] == position_letter:
            return label


def issue_mapping(issue):
    return {
        'id': issue.id,
        'title': issue.title,
        'description': issue.description if issue.description else '',
        'created_at': issue.created_at,
        'updated_at': issue.updated_at,
        'left_side': label_color(issue.labels, position_letter='0'),
        'right_side': label_color(issue.labels, position_letter='1'),
        'labels': issue.labels,
        'assignees': issue.assignees,
        'author': issue.author,
        'web_url': issue.web_url,
        'time_stats': issue.time_stats,
        'references': issue.references
    }


def label_mapping(label):
    return {
        'id': label.id,
        'name': label.name,
        'color': label.color,
        'text_color': label.text_color
    }


def member_mapping(member):
    return {
        'id': member.id,
        'name': member.name,
        'username': member.username,
        'state': member.state,
        'avatar_url': member.avatar_url,
        'web_url': member.web_url
    }
