# Perforce-Triggers

Python scripts to automate `Perforce` version control system trigger scripts deployment.
If you are a `perforce` administrator, this tool is for you, it does the following:
- Submits trigger scripts from a local directory to `perforce` server.
- Automatically adds the scripts to the list of `perforce` triggers.

## How to configure perforce-triggers:

### 1- Create perforce-triggers dir :

##### Linux

/etc/perforce-triggers/

##### Windows

c:\appdata\perforce-triggers\

#### 2- create config file :

##### Linux

/etc/perforce-triggers/config.json 

##### Windows

c:\appdata\perforce-triggers\config.json 

##### Perforce auth 

Add `perforce` server authentication details to the config file:

```json
{
    "auth": {
        "p4_port": "perforce:1666",
        "p4_user": "perforce",
        "p4_tickets": "/home/perforce/.p4tickets"
    },
}
```

- **p4_port** : `perforce` port formatted as <server>:<port>.
- **p4_user** : A `perforce` user with admin permissions.
- **p4_tickets** : local path to `perforce` tickets file containing the user's ticket to `p4_port`.

##### Triggers source and destination

Add the trigger scripts local directory and the destination `perforce` path to submit the scripts to.

```json
{
    "location": {
        "local": "/opt/perforce/triggers/",
        "remote": "//depot/triggers/..."
    },
}
```

- **local** : Local path pointing to trigger scripts location.
- **remote** : perforce path to submit to, if depot does not exist it will be created as depot of type `local`.

##### Configure triggers

This part of the configuration controls how the scripts are deployed as `perforce` triggers.

There are 2 types of triggers :
- script trigger: fired on `perforce` event i.e `change-commit`, `change-submit`.
- command trigger: fired on user-command event i.e `pre-user-move`.

###### Script trigger

```json
{
    "triggers": [
        {
            "name": "my_trigger",
            "type": "script",
            "event": "change-commit",
            "include_paths": ["//depot/frontend/..."],
            "exclude_paths": ["//depot/backend/..."],
            "command": "/usr/bin/python3.6 %//triggers/on_submit.py%",
            "args": ["--verbose", "--notify", "frontend-coders@app.com"]
        },
    ]
}
```
The config above would add the following lines to `perforce` trigger list:

```
Triggers:
    my_trigger change-commit //depot/frontend/... "/usr/bin/python3.6 %//triggers/on_submit.py% --verbose --notify frontend-coders@app.com"
    my_trigger change-commit -//depot/backend/... "/usr/bin/python3.6 %//triggers/on_submit.py% --verbose --notify frontend-coders@app.com"
```

- **name (required)**: `perforce` trigger's name.
- **type (required)**: `script` or `command`.
- **event (required)**: `perforce` event i.e `change-commit`.
- **include_paths (required)**: list of p4 paths in depot syntax. When a user submits a changelist that contains files that match a file in the lsit, the trigger script executes.
- **exclude_paths (optional)**: list of p4 paths to exclude from the trigger.
- **command (required)**: command or script to execute when the event happens.
- **args (optional)**: list of the command arguments. 

###### Command trigger

```json
{
    "triggers": [
        {
            "name": "my_trigger",
            "type": "script",
            "event": "pre-user-sync",
            "command": "/usr/bin/python3.6 %//triggers/on_sync.py%",
            "args": ["--quit"]
        },
    ]
}
```

The config above would add the following lines to `perforce` trigger list:

```
Triggers:
    my_trigger command pre-user-sync "/usr/bin/python3.6 %//triggers/on_sync.py% --quit"
```

- **name (required)**: `perforce` trigger's name.
- **type (required)**: `command`.
- **event (required)**: `perforce` user-command event i.e `(pre|post)-user-move`.
- **command (required)**: command or script to execute when the event happens.
- **args (optional)**: list of the command arguments. 
