import json
from typing import List

import requests
from fastapi import APIRouter, Path, Query, Depends
from pydantic import PositiveInt

from models import GroupModel, MemberModel, LabelModel, BoardModel
from routers.auth import get_token, TokenData

router = APIRouter()


def authorization_header(api_key: str):
    return {"Authorization": f"Bearer {api_key}"}


@router.get("/", response_model=List[GroupModel], response_model_exclude="projects", response_model_exclude_unset=True)
def read_groups(token: TokenData = Depends(get_token)):
    response = requests.get(f"{token.app_url}/api/v4/groups/", headers=authorization_header(token.api_key))
    groups = json.loads(response.text)
    return groups


@router.get("/{group_id}/", response_model=GroupModel, response_model_exclude_unset=True)
def read_group(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}", headers=authorization_header(token.api_key))
    group = json.loads(response.text)
    return group


@router.get("/{group_id}/boards/", response_model=List[BoardModel], response_model_exclude_unset=True)
def read_group_boards(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/boards",
                            headers=authorization_header(token.api_key))
    boards = json.loads(response.text)
    return boards


@router.get("/{group_id}/members/", response_model=List[MemberModel], response_model_exclude_unset=True)
def read_group_members(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/members",
                            headers=authorization_header(token.api_key))
    members = json.loads(response.text)
    return members


@router.get("/groups/{group_id}/issues/")
def read_group_issues(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
        state: str = Query(None, alias="state", max_length=6, title="Issue state",
                           description="Issue state"),
        labels: str = Query('', alias="labels", max_length=150, title="Labels_name",
                            description="Issue label names"),
        author_id: PositiveInt = Query(None, alias="author_id", title="Author_id",
                                       description="Issue author id"),
        assignee_id: PositiveInt = Query(None, alias="assignee_id", title="Assignee_id",
                                         description="Assignee user id"),
        search: str = Query(None, alias="search", max_length=100, title="Search",
                            description="Search value"),
        order_by: str = Query(None, alias="order_by", max_length=20, title="Order by",
                              description="Order by value"),
        with_labels_details: bool = Query(False, alias="with_labels_details", title="Labels details",
                                          description="Labels details in response"),
):
    url = f"{token.app_url}/api/v4/groups/{group_id}/issues?"
    if state:
        url += f"&state={state}"
    if labels:
        url += f"&labels={labels}"
    if author_id:
        url += f"&author_id={author_id}"
    if assignee_id:
        url += f"&assignee_id={assignee_id}"
    if search:
        url += f"&search={search}"
    if order_by:
        url += f"&order_by={order_by}"
    if with_labels_details:
        url += f"&with_labels_details={with_labels_details}"
    response = requests.get(url, headers=authorization_header(token.api_key))
    issues = json.loads(response.text)
    return issues


@router.get("/{group_id}/labels/", response_model=List[LabelModel], response_model_exclude_unset=True)
def read_group_labels(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/labels",
                            headers=authorization_header(token.api_key))
    labels = json.loads(response.text)
    return labels
