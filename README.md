# Perforce-Triggers

Python scripts to automate Perforce version control system trigger scripts deployment.
If you are a Perforce administrator, this tool is for you, it does the following:
- Submits trigger scripts from a local directory to Perforce server.
- Automatically adds the scripts to the list of Perforce triggers.

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

###### Perforce auth 

Add Perforce server authentication details to the config file:

```json
{
    "auth": {
        "p4_port": "perforce:1666",
        "p4_user": "perforce",
        "p4_tickets": "/home/perforce/.p4tickets"
    },
}
```

- ** p4_port ** : Perforce port formatted as <server>:<port>.
- ** p4_user ** : A Perforce user with admin permissions.
- ** p4_tickets ** : local path to Perforce tickets file containing the user's ticket to `p4_port`.

###### Triggers source and destination

Add the trigger scripts local directory and the destination Perforce path to submit the scripts to.

```json
{
    "location": {
        "local": "/opt/perforce/triggers/",
        "remote": "//depot/triggers/..."
    },
}
```

- ** local ** : Local path pointing to trigger scripts location.
- ** remote ** : perforce path to submit to, if depot does not exist it will be created as depot of type `local`.

###### Configure triggers

