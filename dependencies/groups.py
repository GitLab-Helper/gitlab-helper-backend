from fastapi import Query, HTTPException
from pydantic.types import PositiveInt


class IssueQueryChecker:
    def __init__(self):
        self.state = ["opened", "closed"]
        self.order_by = ["created_at", "updated_at", "priority", "due_date", "relative_position", "label_priority",
                         "milestone_due", "popularity", "weight"]

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
