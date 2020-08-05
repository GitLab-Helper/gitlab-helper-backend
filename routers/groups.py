from typing import List

import gitlab
from fastapi import APIRouter, Path, Query, Depends

from models import GroupModel, MemberModel, IssueModel, LabelModel
from routers.auth import get_token, TokenData
from utils import group_mapping, member_mapping, issue_mapping, label_mapping

router = APIRouter()


@router.get("/", response_model=List[GroupModel], response_model_exclude="projects")
def read_groups(token: TokenData = Depends(get_token)):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    groups = gl.groups.list(all=True)

    return [group_mapping(group) for group in groups]


@router.get("/{group_id}/", response_model=GroupModel)
def read_group(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    group = gl.groups.get(id=group_id)

    return group_mapping(group)


@router.get("/{group_id}/boards/", response_model=GroupModel)
def read_group_boards(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    group = gl.groups.get(id=group_id)
    boards = group.boards.list()

    return group_mapping(group, boards=boards)


@router.get("/{group_id}/members/", response_model=List[MemberModel])
def read_group_members(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    group = gl.groups.get(id=group_id)
    members = group.members.list()

    return [member_mapping(member) for member in members]


@router.get("/groups/{group_id}/issues/", response_model=List[IssueModel])
def read_group_issues(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
        labels: str = Query('', alias="labels", max_length=150, title="Labels_name",
                            description="Issue label names"),
        assignee: str = Query(None, alias="assignee_id", max_length=20, title="Assignee_id",
                              description="Assignee user id"),
):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    group = gl.groups.get(id=group_id)

    issues = group.issues.list(all=True, labels=labels.split(","), assignee_id=assignee, state="opened")

    return [issue_mapping(issue) for issue in issues]


@router.get("/{group_id}/labels/", response_model=List[LabelModel])
def read_group_labels(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    gl = gitlab.Gitlab(token.app_url, per_page=30, private_token=token.api_key)

    group = gl.groups.get(id=group_id)
    labels = group.labels.list()

    return [label_mapping(label) for label in labels]
