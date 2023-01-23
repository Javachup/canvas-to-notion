from canvasapi import Canvas
from Canvas.CanvasReaderUtil import utc_to_datetime

class CanvasReader:
    def __init__(self, key, url = "https://champlain.instructure.com/"):
        self._api_key = key
        self._api_url = url

        self._canvas = Canvas(self._api_url, self._api_key)

        # Check if key is valid 
        self._canvas.get_accounts()._get_next_page()

    def read_course_assignments(self, course_id: int, nameDelimiter: str = " - "):
        result = []

        course = self._canvas.get_course(course_id)

        assignments = course.get_assignments()

        for a in assignments:
            data = {}
            data['id'] = a.id
            data['name'] = a.name.replace('\"', '\"\"').strip() # Notion needs double quotes 
            data['desc'] = a.description
            data['created_at'] = a.created_at
            data['updated_at'] = a.updated_at
            data['due_date'] = utc_to_datetime(a.due_at).strftime('%Y-%m-%dT%H:%M:%S.000%z').strip() if a.due_at else None
            data['unlock_at'] = utc_to_datetime(a.unlock_at).strftime('%Y-%m-%dT%H:%M:%S.000%z').strip() if a.unlock_at else None
            i = course.name.find(nameDelimiter)
            data['course_name'] = course.name[:i if i > -1 else len(course.name)].strip()
            data['url'] = a.html_url.strip()
            data['points'] = a.points_possible

            result.append(data)

        return result