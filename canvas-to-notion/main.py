import json
from Notion.Property import Property
from Notion.NotionWriter import NotionWriter
from Canvas.CanvasReader import CanvasReader

info = {}
with open('info.json') as f:
    info = json.load(f)

reader = CanvasReader(info['canvas_key'])
writer = NotionWriter(info['notion_token'], info['notion_database_id'])

print("Reading Notion database...")
writer.cache_pages()

for id_name in info['course_ids']:
    print(f"Reading assignments for course {id_name['name']}...")
    assignments = reader.read_course_assignments(id_name['id'])

    for a in assignments:
        print(f'    Loading assignment "{a["name"]}"...')

        properties = []

        for format in info['property_formats']:
            if format['assignment_value'] in a:
                if a[format['assignment_value']]: # this could be None 
                    properties.append(Property(format['notion_name'], format['notion_type'], a[format['assignment_value']]))
            else:
                raise Exception(f"Assignment value {format['assignment_value']} is not valid!")

        writer.update_or_append(a['name'], properties)

print("\nSuccess!\n")