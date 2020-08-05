from fastapi import Form
from pydantic import HttpUrl


class GitlabAPiKeyRequestForm:
    """
    This is a dependency class, use it like:

        @app.post("/login")
        def login(form_data: GitlabAPiKeyRequestForm = Depends()):
            data = form_data.parse()
            print(data.app_url)
            print(data.api_key)
            return data


    It creates the following Form request parameters in your endpoint:

    app_url: app_url HttpUrl. Url to gitlab instance.
    api_key: api_key string. Account access token used for authorization.
    """

    def __init__(
            self,
            app_url: HttpUrl = Form(...),
            api_key: str = Form(...),
    ):
        # TODO: Fix app_url to have '/' on the end of the url
        self.app_url = app_url
        self.api_key = api_key
