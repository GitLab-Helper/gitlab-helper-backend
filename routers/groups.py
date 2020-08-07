import json
from typing import List

import requests
from fastapi import APIRouter, Path, Query, Depends, HTTPException
from pydantic import PositiveInt

from models import GroupModel, MemberModel, LabelModel, BoardModel, IssueModel
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


class IssueQueryChecker:
    def __init__(self, state, order_by):
        self.state = state
        self.order_by = order_by

    def __call__(self,
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
        errors = []
        issue_query = []
        if state:
            if state in self.state:
                issue_query.append(f"state={state}")
            else:
                errors.append('state')
        if labels:
            issue_query.append(f"&labels={labels}")
        if author_id:
            issue_query.append(f"&author_id={author_id}")
        if assignee_id:
            issue_query.append(f"&assignee_id={assignee_id}")
        if search:
            issue_query.append(f"&search={search}")
        if order_by:
            if order_by in self.order_by:
                issue_query.append(f"&order_by={order_by}")
            else:
                errors.append('order_by')
        if with_labels_details:
            issue_query.append(f"&with_labels_details={with_labels_details}")
        if len(errors):
            raise HTTPException(status_code=400, detail=f"Invalid values in: {errors} params.")
        return "?" + "&".join(issue_query)


checker = IssueQueryChecker(state=["opened", "closed"],
                            order_by=["created_at", "updated_at", "priority", "due_date", "relative_position",
                                      "label_priority", "milestone_due", "popularity", "weight"])


@router.get("/groups/{group_id}/issues/", response_model=List[IssueModel], response_model_exclude_unset=True)
def read_group_issues(
        token: TokenData = Depends(get_token),
        group_id: int = Path(..., title="Group_id", description="Id of gitlab group"),
        query_string: str = Depends(checker)
):
    url = f"{token.app_url}/api/v4/groups/{group_id}/issues{query_string}"
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
