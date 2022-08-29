# Missing  "multi_select", "formula", "relation", "rollup", "people", "files"

class Property:
    def __init__(self, name: str, type: str, value: object) -> None:
        value = Property._correct_value(type, value)

        self.name = name
        self.data = { 'type': type, type: value }

    def __str__(self) -> str:
        return str(self.data)

    def _correct_value(type: str, value: object):
        match type:
            case "title":
                return [ { 'text': { 'content': value }}]
            case "rich_text":
                return [ { 'text': { 'content': value }}]
            case "select":
                return { 'name': value }
            case "status":
                return { 'name': value }
            case "date":
                return { 'start': value }

            case other:
                return value

    def create_page_data(properties: list, parentDatabaseID: str = None):
        data = {}

        if parentDatabaseID:
            data['parent'] = { 'type': 'database_id', 'database_id': parentDatabaseID }

        data['properties'] = {}
        for p in properties:
            data['properties'][p.name] = p.data

        return data