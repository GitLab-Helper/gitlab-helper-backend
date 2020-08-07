import json
from typing import List

import requests
from fastapi import APIRouter, Path, Depends
from pydantic.types import PositiveInt

from dependencies.auth import get_token
from dependencies.groups import IssueQueryChecker, group_id_parameter
from models.auth import TokenData
from models.groups import GroupModel, MemberModel, LabelModel, BoardModel, IssueModel

router = APIRouter()

issue_params_checker = IssueQueryChecker()


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
        group_id: PositiveInt = Depends(group_id_parameter, use_cache=False),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}", headers=authorization_header(token.api_key))
    group = json.loads(response.text)
    return group


@router.get("/{group_id}/boards/", response_model=List[BoardModel], response_model_exclude_unset=True)
def read_group_boards(
        token: TokenData = Depends(get_token),
        group_id: PositiveInt = Depends(group_id_parameter, use_cache=False),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/boards",
                            headers=authorization_header(token.api_key))
    boards = json.loads(response.text)
    return boards


@router.get("/{group_id}/members/", response_model=List[MemberModel], response_model_exclude_unset=True)
def read_group_members(
        token: TokenData = Depends(get_token),
        group_id: PositiveInt = Depends(group_id_parameter, use_cache=False),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/members",
                            headers=authorization_header(token.api_key))
    members = json.loads(response.text)
    return members


@router.get("/{group_id}/issues/", response_model=List[IssueModel], response_model_exclude_unset=True)
def read_group_issues(
        token: TokenData = Depends(get_token),
        group_id: PositiveInt = Depends(group_id_parameter, use_cache=False),
        query_string: str = Depends(issue_params_checker)
):
    url = f"{token.app_url}/api/v4/groups/{group_id}/issues{query_string}"
    response = requests.get(url, headers=authorization_header(token.api_key))
    issues = json.loads(response.text)
    return issues


@router.get("/{group_id}/labels/", response_model=List[LabelModel], response_model_exclude_unset=True)
def read_group_labels(
        token: TokenData = Depends(get_token),
        group_id: PositiveInt = Depends(group_id_parameter, use_cache=False),
):
    response = requests.get(f"{token.app_url}/api/v4/groups/{group_id}/labels",
                            headers=authorization_header(token.api_key))
    labels = json.loads(response.text)
    return labels
