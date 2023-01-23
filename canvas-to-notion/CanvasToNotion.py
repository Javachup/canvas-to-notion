import json
from Notion.Property import Property
from Notion.NotionWriter import NotionWriter
from Canvas.CanvasReader import CanvasReader
from MyThreads import ErrorHandlingThread
from canvasapi import exceptions
import Notion.NotionExceptions as ne
import requests.exceptions

import time

def cache_pages_wrapper(writer: NotionWriter):
    writer.cache_pages()
    print("Notion Database read!")

def Run(file):
    start = time.time()

    try:
        info = json.load(file)
    except json.JSONDecodeError as e:
        print(f"=== JSON decoder error ===\n{e}")
        return

    # Create Canvas Reader
    try:
        reader = CanvasReader(info['canvas_key'])
    except exceptions.InvalidAccessToken:
        print(f"=== Invalid Canvas Token ===")
        return
    except requests.exceptions.ConnectionError as e:
        print(f"=== ConnectionError ===\nMake sure you are connected to the internet\n\n{e}")
        return

    # Create Notion Writer 
    try:
        writer = NotionWriter(info['notion_token'], info['notion_database_id'])
    except ne.DatabaseQueryError as e:
        if e.error == "validation_error":
            print(f"=== Invalid Database ID ===\n{e}")
        if e.error == "object_not_found":
            print(f"=== Could not find Database ===\n{e}")
        if e.error == "unauthorized":
            print(f"=== Invalid Notion Token ===\n{e}")
        else:
            print(f"=== Failed to query Notion database! ===\n{e}")
        return

    print("Begining to read Notion Database...")
    thread = ErrorHandlingThread(target=cache_pages_wrapper, args=[writer])
    thread.start()

    # Gets each of the course ids from the info file 
    processed_assignments = [] # list of tuples containing title strings and properties lists 

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

            processed_assignments.append((a['name'], properties))

    print("Waiting for notion database...")

    try:
        thread.join()
    # TODO: Handle specific errors 
    except ne.DatabaseQueryError as e:
        print(f"=== Failed to query Notion database! ===\n{e}")
        return
    except Exception as e:
        print(e)

    print("Writing to notion Database...")
    for a in processed_assignments:
        try:
            writer.update_or_append(a[0], a[1])
        except ne.DatabaseQueryError as e:
            print(f"=== Failed to query Notion database! ===\n{e}")
            return

    end = time.time()
    print(f"\nSuccess! Took {round(end - start, 2)} second(s)\n")