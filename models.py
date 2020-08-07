from typing import List, Optional

from pydantic import BaseModel, HttpUrl, PositiveInt


class UserModel(BaseModel):
    id: PositiveInt
    name: str
    username: str
    state: str
    avatar_url: HttpUrl
    web_url: HttpUrl


class ProjectModel(BaseModel):
    id: PositiveInt
    name: str
    name_with_namespace: str
    web_url: HttpUrl


class TimeStatsModel(BaseModel):
    time_estimate: int
    total_time_spent: int
    human_time_estimate: Optional[str] = None
    human_total_time_spent: Optional[str] = None


class ReferencesModel(BaseModel):
    short: str
    relative: str
    full: str


class IssueModel(BaseModel):
    id: PositiveInt
    title: str
    description: str
    created_at: str
    updated_at: str
    left_side: Optional[str]
    right_side: Optional[str]
    labels: List[str]
    assignees: List[UserModel]
    author: UserModel
    web_url: HttpUrl
    time_stats: TimeStatsModel
    references: ReferencesModel


class LabelModel(BaseModel):
    id: PositiveInt
    name: str
    color: str
    text_color: str
    description: Optional[str] = None
    description_html: Optional[str] = None


class MemberModel(BaseModel):
    id: PositiveInt
    name: str
    username: str
    state: str
    avatar_url: str
    web_url: str


class ListModel(BaseModel):
    id: PositiveInt
    label: LabelModel
    position: PositiveInt


class BoardModel(BaseModel):
    id: PositiveInt
    lists: List[ListModel]


class GroupModel(BaseModel):
    id: PositiveInt
    web_url: HttpUrl
    name: str
    projects: Optional[List[ProjectModel]] = None
