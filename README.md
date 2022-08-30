# canvas-to-notion

## What is it? 

Automatically reads in Canvas assignments and writes them into a Notion Database. 


## How do I use it? 

The program reads a file called `info.json` to get all the information it needs. You will need to create this and place it in the correct directory. 

1. Create `info.json` 
2. Provide info in the correct format 
3. Run the program and profit 

## `info.json` format 

This is important so listen up. `json` does not need to be in any particular order but does need to be the exact same spelling. Angle brackets (`<>`) will mean something is required while parentheses (`()`) will mean that something is optional. `...` will mean you can repeat the above line as many times as needed (just make sure there is a comma after each entry except for the last one). I will provide sections on how to find each ID and key. 

`course_ids` is where you specify which courses you want to read from. `"name"` is only used to inform you the user which class is being read and as such you could put anything you want there. It will not show up in Notion at all. 

As for `property_formats`, this is where you specify what infomation you want to take from each canvas assignment and where to place it into your database. `notion_name` is the name of the property as you define it in Notion and MUST match exactly. 

Possible `assignment_value`s are: `"id", "name", "desc", "created_at", "updated_at", "due_date", "unlock_at", "course_name", "url", "points"`. 

Possible `notion_type`s are: `"title", "rich_text", "number", "select", "date", "checkbox", "url", "email", "phone_number","created_time", "created_by", "last_edited_time", "last_edited_by", "status"` (Note that `"multi_select", "formula", "relation", "rollup", "people", "files"` are all currently unsupported.)

There is also a section for ignoring assignments. For example, a professor put an in-class powerpoint as an assignment and you don't want that importing into your notion. You can provide the assignment id of the that assignment and it will be ignored. 

For your convenience, you can add additional information anywhere you'd like (for example the name of an assignment or the course it belongs to) as long as it follows json syntax. 

```
{
    "notion_token": "<SECRET NOTION KEY GOES HERE>",
    "notion_database_id": "<NOTION DATABASE ID GOES HERE>",
    "canvas_key": "<CANVAS ID GOES HERE>",

    "course_ids":
    [
        { "id": <COURSE ID>, "name": "<COURSE NAME>" },
        { "id": <COURSE ID>, "name": "<COURSE NAME>" }
        ...
    ],

    "property_formats":
    [
        { "notion_name": "<PROPERTY NAME>", "notion_type": "<SEE ABOVE FOR POSSIBLE TYPES>", "assignment_value": "<SEE ABOVE FOR POSSIBLE VALUES>" },
        { "notion_name": "<PROPERTY NAME>", "notion_type": "<SEE ABOVE FOR POSSIBLE TYPES>", "assignment_value": "<SEE ABOVE FOR POSSIBLE VALUES>" }
        ...
    ],

    "assignment_ignore_list":
    [
        { "id": <ASSIGNMENT ID> },
        { "id": <ASSIGNMENT ID> }
        ...
    ]
}
```

### Example `info.json`
For obvious reasons these keys are fake. 
```
{
    "notion_token": "secret_abcdefghijklmnopqrstuvwxyz123457890ABCDEFGH",
    "notion_database_id": "qwertyuiopasdFGHJKLZXCVBNM123456",
    "canvas_key": "3~mnbvcxzlkjhgfdsapoiuytrewq1234567890QWERTYUIOPASDFGHJKLZXCVBNM12",

    "course_ids":
    [
        { "id": 1921014, "name": "Place" },
        { "id": 1921028, "name": "City" },
        { "id": 1922026, "name": "Portfolio" },
        { "id": 1922122, "name": "GTechII" },
        { "id": 1922126, "name": "Ludo" },
        { "id": 1921142, "name": "Graphics" }
    ],

    "property_formats":
    [
        { "notion_name": "Name", "notion_type": "title", "assignment_value": "name" },
        { "notion_name": "Course", "notion_type": "select", "assignment_value": "course_name" },
        { "notion_name": "Due Date", "notion_type": "date", "assignment_value": "due_date" },
        { "notion_name": "Canvas Link", "notion_type": "url", "assignment_value": "url" },
        { "notion_name": "Points", "notion_type": "number", "assignment_value": "points"}
    ],

    "assignment_ignore_list":
    [
        { "id": 27507612, "name": "ppt and readings" },
        { "id": 27507662 }
    ]
}
```

# Where are these keys and ids? 

## Notion token 
This is essentially your login so keep this secret! Anyone with this key can act as you can like steal your shit. You can deactivate keys though so don't worry too much. 

Follow steps 1 and 2 [here](https://developers.notion.com/docs/getting-started#step-1-create-an-integration) to create your integration and get your token. You will:
1. Create an integration 
2. Get the token from that integration 
3. Share the integration with the database you want to edit 

## Canvas Key 
Same warning as the Notion Token. This is essentially your login so don't go sharing this. 
1. Go to your settings (Click on Account then Settings) 
2. Scroll until you see "Approved Integrations" 
3. Click "New Access Token" and input purpose and, if desired, an expiration date (for safty I would recomend adding an expiration date) 
4. Snag that token and stick it in `info.json` 

## Notion Database ID 
1. Navagate to your database page that you shared with your integration 
2. The database id is in the url to that page 
[https://www.notion.so/](https://www.youtube.com/watch?v=dQw4w9WgXcQ)**qwertyuiopasdFGHJKLZXCVBNM123456**?v=awsddeggdbbrhers3325regfst3wt560
It's between the '/' and the '?' as seen above. 