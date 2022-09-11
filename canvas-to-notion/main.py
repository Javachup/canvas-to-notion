from __future__ import print_function
import json
from Notion.Property import Property
from Notion.NotionWriter import NotionWriter
from Canvas.CanvasReader import CanvasReader

import time

def Run(filename):
    info = {}
    with open(filename) as file:
        info = json.load(file)

    reader = CanvasReader(info['canvas_key'])
    writer = NotionWriter(info['notion_token'], info['notion_database_id'])

    print("Reading Notion database...")
    writer.cache_pages()

    # Gets each of the course ids from the info file 
    for course_id_name in info['course_ids']:
        if course_id_name['ignore']:
            print(f"Ignoring assignments for course {course_id_name['name']}...")
            continue

        print(f"Reading assignments for course {course_id_name['name']}...")
        assignments = reader.read_course_assignments(course_id_name['id'])

        # Processes each of the assignments for the current course 
        for a in assignments:
            # Check ignore list 
            ignored = False
            for i in info['assignment_ignore_list']:
                if (a['id'] == i['id']):
                    print(f'    Ignoring assignment "{a["name"]}"...')
                    ignored = True
                    break
            if ignored: continue

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