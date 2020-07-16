import os
from typing import List

import gitlab
from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware

from models import GroupModel, LabelModel, MemberModel, IssueModel
from utils import group_mapping, label_mapping, member_mapping, issue_mapping

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gl = gitlab.Gitlab(os.getenv('GITLAB_URL'), per_page=30, private_token=os.getenv('PRIVATE_TOKEN'))


@app.get("/groups/", response_model=List[GroupModel], response_model_exclude='projects', tags=["groups"])
def read_groups():
    groups = gl.groups.list(all=True)

    return [group_mapping(group) for group in groups]


@app.get("/groups/{group_id}/", response_model=GroupModel, tags=["groups"])
def read_group(group_id: int = Path(..., title="Group_id", description="Id of gitlab group"), ):
    group = gl.groups.get(id=group_id)

    return group_mapping(group)


@app.get("/groups/{group_id}/boards/", response_model=GroupModel, tags=["groups", "boards"])
def read_group_boards(group_id: int = Path(..., title="Group_id", description="Id of gitlab group"), ):
    group = gl.groups.get(id=group_id)
    boards = group.boards.list()

    return group_mapping(group, boards=boards)


@app.get("/groups/{group_id}/members/", response_model=List[MemberModel], tags=["groups", "members"])
def read_group_members(group_id: int = Path(..., title="Group_id", description="Id of gitlab group"), ):
    group = gl.groups.get(id=group_id)
    members = group.members.list()

    return [member_mapping(member) for member in members]


@app.get("/groups/{group_id}/issues/", response_model=List[IssueModel], tags=["groups", "issues"])
def read_group_issues(
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
        labels: str = Query('', alias="labels", max_length=150, title="Labels_name",
                            description="Issue label names"),
        assignee: str = Query(None, alias="assignee_id", max_length=20, title="Assignee_id",
                              description="Assignee user id"),
):
    group = gl.groups.get(id=group_id)

    issues = group.issues.list(all=True, labels=labels.split(','), assignee_id=assignee, state='opened')

    return [issue_mapping(issue) for issue in issues]


@app.get("/groups/{group_id}/labels/", response_model=List[LabelModel], tags=["groups", "labels"])
def read_group_labels(
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    group = gl.groups.get(id=group_id)
    labels = group.labels.list()

    return [label_mapping(label) for label in labels]
