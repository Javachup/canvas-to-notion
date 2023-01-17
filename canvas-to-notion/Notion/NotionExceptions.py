import requests
import json

#{"object":"error",
# "status":400,
# "code":"validation_error",
# "message":"path failed validation: path.database_id should be a valid uuid, instead was `\"e2bc03bd89ee4ca6984d8c746fbf5bc8 this is wrong\"`."}

class DatabaseQueryError(Exception):
    def __init__(self, r: requests.Response):
        errorJSON = json.loads(r.text)
        self.status = errorJSON["status"]
        self.error = errorJSON["code"]
        self.message = errorJSON["message"]

    def __str__(self) -> str:
        return f"{self.error}: {self.message}"