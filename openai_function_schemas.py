FUNCTIONS_SCHEMA = [
    {
        "name": "get_search_results",
        "description": "Used to get search results when the user asks for it",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for",
                }
            },
        },
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "longitude": {
                    "type": "number",
                    "description": "The approximate longitude of the location",
                },
                "latitude": {
                    "type": "number",
                    "description": "The approximate latitude of the location",
                },
            },
            "required": ["longitude", "latitude"],
        },
    },
    {
    "name": "search_images",
    "description": "Search for images using the SERAPI image search service",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search for images",
            },
            "max_results": {
                "type": "integer",
                "description": "The maximum number of image results to retrieve",
                "default": 10
            }
        },
        "required": ["query"]
    }
},
{
                "name": "service_now_ticket_creation",
                "description": "Create a ServiceNow ticket with the given short description and description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "short_description": {
                            "type": "string",
                            "description": "A brief summary of the ticket",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed information about the ticket",
                        },
                    },
                    "required": ["short_description", "description"],
                },
            },

            {
                "name": "get_incident_status_by_number",
                "description": "Get the status of an incident using the incident number",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_number": {
                            "type": "string",
                            "description": "The unique identifier of the incident, e.g. INC0001234",
                        }
                    },
                    "required": ["incident_number"],
                },
            },
            {
                "name": "get_recent_incidents_status",
                "description": "Get the recent incidents status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number_of_incidents": {
                            "type": "string",
                            "description": "Number of incidents needs to showup. e.g. 2",
                        }
                    },
                    "required": ["number_of_incidents"],
                },
            },
            {
                "name": "add_comment_to_incident",
                "description": "In ServiceNow, a comment is a free-text field that allows users to add additional information to a incident. For example, when creating or updating an incident, users can add comments to provide more details about the issue or update the status of the incident1. Comments can also be used to provide ongoing commentary on how a task is progressing",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_number": {
                            "type": "string",
                            "description": "The unique identifier of the incident, e.g. INC0001234",
                        },
                        "comment": {
                            "type": "string",
                            "description": "Adding comments to the incident, e.g. i am unable to login",
                        },
                    },
                    "required": ["sys_id", "comments"],
                },
            },

            {
        "name": "get_access_token",
        "description": "Used to get access token when the user asks for it",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for",
                }
            },
        },
    },
            {
    "name": "send_email_via_graph_api",
    "description": "Send an email via the Microsoft Graph API",
    "parameters": {
        "type": "object",
        "properties": {
            "access_token": {
                "type": "string",
                "description": "The Microsoft Graph API access token for authentication."
            },
            "recipient_email": {
                "type": "string",
                "description": "The email address of the recipient."
            },
            "subject": {
                "type": "string",
                "description": "The subject of the email."
            },
            "message_body": {
                "type": "string",
                "description": "The body/content of the email."
            }
        },
        "required": ["access_token", "recipient_email", "subject", "message_body"]
    }
},


    
    # other functions
]
