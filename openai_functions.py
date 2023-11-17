from datetime import datetime
import pytz
from requests.auth import HTTPBasicAuth
from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from datetime import datetime, timedelta
import pytz     
import requests
import json
import os
import re



class OpenAIFunctions:
    accessToken = "EwB4A8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAbbOpdy02fizvO6P4bAajN735LjBbxuu1X0mqERUkcyFc8DduW3KbMOO+u5HCLfp7wZlR7jfVk4+OCvjG+1KUnVm6KjrItTnqg/GKJzSvXHTBtrToTQGglw1gRf+LJp25yuO7ZUdUV6OIGnTfjjax8xFyvIiBPQbdQQAWlQaDYklpeimuenDOwA2+J7iLtMYHW21nby5pwx8JAtJ5xVmXenw0zj+0lHTBGQ33pMXCXRGbVbDuysx9DbTjbDdOeGfu09kzw61je5iQL38l/bbHR4VIFf7Y9OEKt7ifcx+3yODdBkSkqURr96gU6jV3mgVeLeWj6ISGy08L2n2eu/6OjUDZgAACJGDDIdLNd1cSAK70moU8TZ6OHklztLi+rR2Ta1x23aKErVkZeiKHZBY/l4qQ94fuHqUOOrLMsijRMdS69l0+6xqA0f9gGe7ctPWqj+DluJwUSmhkrlFfbp6C1JX7CDCnQIg0WTazoQlYSwvPvy3OC9UhSxaDbnYUqNJHczm6DA9/8fdOSJMUIaUTOkO1OnAm7uFDlCSo8C9F06mi13niVcr7EzjmKvC4URTGdrqLWnbUyHaoucaIc2mGGg4mN2vlCSyP3Czipq8r6c2+qaIhO3253qYatzTIzADjX/jSO1CfhXQ8tVMJmRJDYSvIIa8CtBtDLAzzQT2zASyVa/4qX2HBS+tF8fdLllc7ooT7POtcXsqY5AnOIn8NsXpzoI0vKcfozIHurybrByh95E91pCxvdYSA8Qaw8ZYgZWObEcowbifL838TfNIIiGy0bQ58C83rKPH3mhU2lvSXxdn0ECG9YwLOXT3sU+f6MbLqqoZttMCasLA7d/Rt8r7pBl/6vvAH250mkvVVTEhzM0ON81RAQKUV0euJ1+6xcJrl8HYbhaweJTtDutznonzYPk/RPFVRzzQwbfJx+XIteAdsgb7Ia8DO1Vl8oo4H9goXrN+6HkXDvM1Hw8LUqNfjXYAVeIT+mZehCGb9QpviGRu179P7xdR7zUCpvdpRFAoUwrMwI8kLPOlBtCTpRIpOGTXcFch0AaIdZ5vwmvv+VCZAsC+2x3ealxJBIKyuFKXIezdtLFwGX7yOrrwRiy2nNe+V4Ssq0vUhiXh/LK8c1Oko1WXEIYC"
    meeting = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Imtuc0Z2NUxTb013WlBiTzVwenI3WV8zc2NCMHRmdnNQeWdTWU1lMzA4LUEiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQvIiwiaWF0IjoxNjk4Mjk4MDUxLCJuYmYiOjE2OTgyOTgwNTEsImV4cCI6MTY5ODM4NDc1MSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQThyUmxlU1ZkSXV1eU43bXF2ekkyaUdDaEVXdWpvcE9ieUdjT1kyNEQyeFJMY0JCaFZGOEhSK1d1dTRObHVJS3ZZOWlRTXNpcjlBbzVIUlVCTlR4WTlid1Jmak5wUldHVENrbUY0SWVsNm1zPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJIZW1hY2hhbmRpcmFuIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTA2LjE5Ny4zNi4xOTMiLCJuYW1lIjoiSGVtYWNoYW5kaXJhbiBUIiwib2lkIjoiYmEwMGZiNzYtNGEzZi00YjliLTk5MmEtNWRlMDE5Yjc0NTFmIiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAyRjg1NkFGNUUiLCJyaCI6IjAuQWIwQUs5NzdvQ3ZlNmstRElETnp3aWVGZEFNQUFBQUFBQUFBd0FBQUFBQUFBQURMQUc0LiIsInNjcCI6IkNhbGVuZGFycy5SZWFkLlNoYXJlZCBDYWxlbmRhcnMuUmVhZFdyaXRlLlNoYXJlZCBEZXZpY2VNYW5hZ2VtZW50QXBwcy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50QXBwcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRDb25maWd1cmF0aW9uLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRDb25maWd1cmF0aW9uLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudE1hbmFnZWREZXZpY2VzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWRXcml0ZS5BbGwgRGlyZWN0b3J5LlJlYWQuQWxsIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6IldDYWs1WnQ1cjNGSDJ6eDBWVGEwcHc1VkJ0YTFZSWhoaXhYWWQyd3lWVFEiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiTkEiLCJ0aWQiOiJhMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQiLCJ1bmlxdWVfbmFtZSI6IkhlbWFjaGFuZGlyYW5AOGswZ2YxLm9ubWljcm9zb2Z0LmNvbSIsInVwbiI6IkhlbWFjaGFuZGlyYW5AOGswZ2YxLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6IkYwN2R2NDZhU0U2MXp3WGpwckEyQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2MiOlsiQ1AxIl0sInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6InpyNU92SWxXcXc4Tms0SzdfWEVlZWVtSFJQcU52T3YwenRQRFpZU3BkaWMifSwieG1zX3RjZHQiOjE2OTU1MTAzNjl9.Tb91VHwelMjAGYOsfcccQqXGG3F1RfOsTF16GEV2ibXclAJcqBD1QggxuNRAq8SMvXrAcOYQvIc_i-DP5I3RUxfeZ-cDGzmUb3kuMMrcqP4A-AbU0gQdNsPw86cs_ekg39-tpdrnYJ58mWcKOvq285ojVSaw34F9snyCogwocoyb1TxlKNALbB6NF03qvzWmcxkMeeKX4-aSdMDofc4yZK8sAidjrdLSsVsrzp0dwcF-ZyIw4K7xNX7gvfqGw7XnSgtbYR96MfnCQWBNuYBlHts1qTrleYHTZ7zf5883Xtsn-WMIW9_nVIAu7ebdcZNdqIOvfqV2--7jAVgPpoBMEQ"
    getEvents ="EwCYA8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAXyRdIQJ+N4AT9gWcR9jB3jU8qrjn7e3fD9DlX8o4kVbQ1y2JFQjEoxv6Vxomc5l4MZJB1mog+kztOMPWablFSpktubqQJGdmAUV+tgBPPu4lxH6ZLOn4axiGsxyJjb7C+43hC33IcWCVmEM/9gEoCE48vOb1hZ1oFRdGP8bZebBjtgXrlCMa3OViJJd+xVLNiH/PTFFuY0zkLnIFwON3ErpV9j0HG8XMm0zVxcONjdyfy5VRUMKtrs6YgYDISmzFDpCr8XEwNhJ18bycgfd6ZhHoanWtDBPvF3z56DyvVHvn7Wq4MGajXlCJmLDSIXLGuVD69rPmVjlyvYnRxqf4yYDZgAACHBqa/Ko6tTJaAIB+4cS9VWLYvH7cvYR0PIQGC+DXNiz0Je7s/PwiFKwxRwDlivFClGYXcimcnZ/jofwnEXzHH5g59siqcKqNNNyDApK9huhi+peTiBm2INMlUuby4qX7dBsOkcMWnQ9XHxPnqnRS/tK+edCI1N1rujfztOAu9y/ur6qfJGA4ET8mSqlRILRit9x9dGQsFaaNFy74IOZFErHT2HNf8mVVAlLnVponyT9AFsqFGdYESU9WPheei/SegI0So8ot5nZAZsXJsRLdPbrxX+ObgDONlJyvv0On7CE9F3k9nCMaQBRSiYPiuqtkYNRB313+1uQUzH7f9cW9YpH3gkvCkSHpTwgY573CeKCXbiqhQj06hNGLOxHd57+VuOWCT9suF0lnsAqZQNAUqM46FJcd6bqNZw9coT8vG1fA+rscTYN0xzjD69RTBOqNeWvjWIGEj3tp+x9cgTelBful6kADmdOkTk+h6V3YsqvKL1nz/VxZPx5tXp3fK3YzbUW31HLYSpIwi7wj3mKZimwUv99eXA96OChuLd7FGyKfORvWDfzUUoZJ/8VisyHbleqkDAsJmUJrmoQNGWrnbOPiBkiO8eZ6VFtz1Ewu+UXvoxnPlPADAB7yRYTet7TldPLvPIq1VJ7b9jiXXvC57C1SAIXUiXtLAbeKYGVl92gR7Vfz4VmOhzJ0dpp4OYV+cZyjLok/61HS01Yy71btDT5JW5h8kLNo2ReXqYQxH1fj+Z8eK9lps4+DNuTXQ2DowgHDhpAPdTDnN9BcbWykYhUZJYucdQxIJjphXDs8r9xS/Pw+b80IMA/ZWMJqOhwHSV5pgI="

    @staticmethod
    def get_current_weather(longitude, latitude):
        """Get the current weather for a location"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "timezone": "Europe/Berlin",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return json.dumps(data["current_weather"])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return json.dumps({"error": "Failed to get weather"})

    @staticmethod
    def get_search_results(query):
        """Get search results for a query"""
        try:
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
            search = SerpAPIWrapper(
                serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            )
            tools = [
                Tool(
                    name="Search",
                    func=search.run,
                    description="useful for when you need to answer questions about current events. You should ask targeted questions",
                )
            ]
            agent = initialize_agent(
                tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
            )
            res = agent.run(query)
            return json.dumps(res)
        except Exception as e:
            print(f"Error getting search results: {e}")
            return json.dumps({"error": "Failed to get search results"})
        
    @staticmethod
    def search_images(query, max_results=10):
        """Search for images using the SERPAPI image search service"""
        try:
            # Initialize SERPAPI client with your API key
            serpapi_api_key = os.getenv("SERPAPI_API_KEY")
            search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

            # Define the parameters for the image search
            params = {
                "q": query,
                "tbm": "isch",  # Image search
                "num": max_results,  # Number of results to retrieve
            }

            # Perform the image search
            response = search.run(params)

            return json.dumps(response)
        except Exception as e:
            print(f"Error searching images: {e}")
            return json.dumps({"error": "Failed to search for images"})
        
    @staticmethod
    def service_now_ticket_creation(short_description, description):
        """Create a new servicenow ticket"""

        auth = HTTPBasicAuth("", "")

        uri = "https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_display_value=true"

        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        # define payload for request, note we are passing the sysparm_action variable in the body of the request

        payload = {"short_description": short_description, "description": description}

        r = requests.post(
            url=uri, data=json.dumps(payload), auth=auth, verify=False, headers=headers
        )

        content = r.json()

        return json.dumps(content)
    
    @staticmethod
    def get_incident_status_by_number(incident_number):
        auth = HTTPBasicAuth("", "")

        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=numberLIKE{incident_number}^ORDERBYDESCsys_created_on&sysparm_display_value=true"

        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        r = requests.get(url=uri, auth=auth, verify=False, headers=headers)

        content = r.json()

        return json.dumps(content)
    @staticmethod
    def get_recent_incidents_status(number_of_incidents):
        auth = HTTPBasicAuth("", "")

        uri = f"https://wiprodemo4.service-now.com/api/now/table/incident?sysparm_query=sys_created_bySTARTSWITHadarsh^ORDERBYDESCsys_updated_on^active=true&sysparm_limit={number_of_incidents}"
        headers = {
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        r = requests.get(url=uri, auth=auth, verify=True, headers=headers)

        content = r.json()

        incidents = []
        for incident in content["result"]:
            status = incident["state"]
            incident_number = incident["number"]
            short_description = incident["short_description"]
            comments = incident["comments"]
            description = incident["description"]
            sys_id = incident["sys_id"]

            # Storing the extracted fields in a dictionary
            incident_dict = {
                "status": status,
                "incident_number": incident_number,
                "short_description": short_description,
                "comments": comments,
                "description": description,
                "sys_id": sys_id
            }

            # Adding the dictionary to a list of incidents
            incidents.append(incident_dict)


        print("Response Status Code: " + str(content))

        return json.dumps(incidents)

    @staticmethod
    def add_comment_to_incident(incident_number, comment):
        content_list = OpenAIFunctions.get_incident_status_by_number(incident_number)

        # Ensure content_list is a list and not a JSON string
        if isinstance(content_list, list):
            content = content_list[0]  # Assuming the list contains a single dictionary
            status = content.get("result", {}).get("state")
            incident_number = content.get("result", {}).get("number")
            short_description = content.get("result", {}).get("short_description")
            comments = content.get("result", {}).get("comments")
            description = content.get("result", {}).get("description")
            sys_id = content.get("result", {}).get("sys_id")

            auth = HTTPBasicAuth("", "")
            uri = f"https://wiprodemo4.service-now.com/api/now/table/incident/{sys_id}?sysparm_display_value=true"
            headers = {
                "Accept": "application/json;charset=utf-8",
                "Content-Type": "application/json",
            }
            payload = {
                "comments": comment
            }
            r = requests.patch(url=uri, auth=auth, verify=True, headers=headers, json=payload)
            content = r.json()
            print("Response Status Code: " + str(content))
            return json.dumps(content)
        else:
            # Handle the case where content_list is not a list (e.g., an error response)
            return "Invalid content data"
        

    @staticmethod
    def send_email_via_graph_api(recipient_email, subject, message_body):
        try:
            access = OpenAIFunctions.accessToken
        # Microsoft Graph API endpoint for sending emails
            api_url = "https://graph.microsoft.com/v1.0/me/sendMail"

            # Create the email message payload
            email_data = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "Text",
                        "content": message_body
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": recipient_email
                            }
                        }
                    ]
                }
            }

            headers = {
                "Authorization": f"Bearer {access}",
                "Content-Type": "application/json"
            }

            # Send the email using the Graph API
            response = requests.post(api_url, headers=headers, data=json.dumps(email_data))

            if response.status_code == 202:
                # Return a valid JSON response even in the case of success
                return json.dumps({"status": "Email sent successfully!"})
            else:
                error_message = f"Failed to send email. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
    
    @staticmethod
    def schedule_meeting_via_graph_api( recipient_email, subject, start_time, end_time, location):
        try:
        # Microsoft Graph API endpoint for scheduling meetings
            api_url = "https://graph.microsoft.com/v1.0/me/events"
            access_token = OpenAIFunctions.meeting
            
            ist = pytz.timezone('Asia/Kolkata')

            # Convert start_time and end_time to naive datetime objects
            start_time_naive = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            end_time_naive = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

            # Set the timezone to IST
            start_time_ist = ist.localize(start_time_naive, is_dst=None)
            end_time_ist = ist.localize(end_time_naive, is_dst=None)

            # Format the datetime objects in UTC format
            start_time_utc_str = start_time_ist.astimezone(pytz.UTC).isoformat()
            end_time_utc_str = end_time_ist.astimezone(pytz.UTC).isoformat()

            # Create the meeting request payload
            meeting_data = {
                "subject": subject,
                "start": {
                    "dateTime": start_time_utc_str,
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time_utc_str,
                    "timeZone": "UTC"
                },
                "location": {
                    "displayName": location
                },
                "attendees": [
                    {
                        "emailAddress": {
                            "address": recipient_email
                        }
                    }
                ],
                "isOnlineMeeting":True,
                "allowNewTimeProposals": True,
                # "onlineMeetingProvider": "teamsForPersonal"
            }

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            # Send the meeting request using the Graph API
            response = requests.post(api_url, headers=headers, data=json.dumps(meeting_data))

            if response.status_code == 201:
                # Return a valid JSON response even in the case of success
                return json.dumps({"status": "Meeting scheduled successfully!"})
            else:
                error_message = f"Failed to schedule meeting. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
        
    @staticmethod
    def cancel_meeting_by_name_via_graph_api(meeting_name):
        try:
            # Microsoft Graph API endpoint for retrieving events (meetings)
            api_url = "https://graph.microsoft.com/v1.0/me/events"

            access_token = OpenAIFunctions.meeting

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            # Send a GET request to retrieve the user's events (meetings)
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                events = response.json().get("value", [])

                # Find the meeting with the specified name
                for event in events:
                    if event.get("subject") == meeting_name:
                        meeting_id = event.get("id")
                        
                        # Use the meeting ID to cancel the meeting
                        cancel_url = f"https://graph.microsoft.com/v1.0/me/events/{meeting_id}"
                        cancel_response = requests.delete(cancel_url, headers=headers)

                        if cancel_response.status_code == 204:
                            return json.dumps({"status": "Meeting canceled successfully!"})
                        else:
                            error_message = f"Failed to cancel meeting. Status code: {cancel_response.status_code}"
                            return json.dumps({"error": error_message, "response": cancel_response.text})

                # If the meeting with the specified name is not found
                return json.dumps({"error": f"Meeting with name '{meeting_name}' not found."})
            else:
                error_message = f"Failed to retrieve events. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
        

    @staticmethod
    def find_free_meeting_times( participants, start_time, end_time):
        # Replace this with your own access token and API endpoint
        access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InBGcDBBVDdGYjh1aGtmUDhOT0E0a01hZklzSjcwelROeXpUMmswS2F4SHMiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQvIiwiaWF0IjoxNjk4MDcxNjIzLCJuYmYiOjE2OTgwNzE2MjMsImV4cCI6MTY5ODE1ODMyMywiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQXVJUkx1bmkvY214REtRdTM0MnJBTlI0QTdta1JFMW51dlNlT2krb2hjRkpGa3IwOGZhVDdodEpEbFJzeWdaVXdja2JRb1YxdTdzV2VJMGVtaHE0MzJ2ZGdrc2VyYjYzYnM4Lzg0aUYvb2lvPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJIZW1hY2hhbmRpcmFuIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTAzLjEzMC45MS4yMzMiLCJuYW1lIjoiSGVtYWNoYW5kaXJhbiBUIiwib2lkIjoiYmEwMGZiNzYtNGEzZi00YjliLTk5MmEtNWRlMDE5Yjc0NTFmIiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAyRjg1NkFGNUUiLCJyaCI6IjAuQWIwQUs5NzdvQ3ZlNmstRElETnp3aWVGZEFNQUFBQUFBQUFBd0FBQUFBQUFBQURMQUc0LiIsInNjcCI6IkNhbGVuZGFycy5SZWFkLlNoYXJlZCBDYWxlbmRhcnMuUmVhZFdyaXRlLlNoYXJlZCBEZXZpY2VNYW5hZ2VtZW50QXBwcy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50QXBwcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRDb25maWd1cmF0aW9uLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRDb25maWd1cmF0aW9uLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudE1hbmFnZWREZXZpY2VzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWRXcml0ZS5BbGwgRGlyZWN0b3J5LlJlYWQuQWxsIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6IldDYWs1WnQ1cjNGSDJ6eDBWVGEwcHc1VkJ0YTFZSWhoaXhYWWQyd3lWVFEiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiTkEiLCJ0aWQiOiJhMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQiLCJ1bmlxdWVfbmFtZSI6IkhlbWFjaGFuZGlyYW5AOGswZ2YxLm9ubWljcm9zb2Z0LmNvbSIsInVwbiI6IkhlbWFjaGFuZGlyYW5AOGswZ2YxLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6IjlCbjg1R1JOTmt5djd3bDctTC1IQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2MiOlsiQ1AxIl0sInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6InpyNU92SWxXcXc4Tms0SzdfWEVlZWVtSFJQcU52T3YwenRQRFpZU3BkaWMifSwieG1zX3RjZHQiOjE2OTU1MTAzNjl9.QWJyRDKkgmobDGzCwpNGsY2nJVTXzIYfxxMlBxRMI3XnR7_kvj0RIt4wMLZIradxHfAm8psd8JQU8ENv0ZGlh8y-jO9GoyZYKCNIdiDQ5fi9zR3N1fYJ3-frSmvF-mv-LIsRrltQDIaUF8o5QyOIc9TfjsxVMPvb6WcuLtq0dhAdM7cNKf-sxBmWKjO3CNMrA7A-5tLLHiZVJe4epgw1XgvudgGvBKabRTfH-Utxos4zvFDnfOkPnN2OS59hHhIvq41dFa0migOG1if23UEtyuozCSu-Hl6aC_LzZZld5q63hSGNnRjLptFx8q_ExzYDLLNIN8fvWt5zKTCUNkH9GQ"
        api_endpoint = "https://graph.microsoft.com/v1.0/me/findMeetingTimes"

        participants_list = [{"emailAddress": {"address": email}} for email in participants]

        # Convert input timestamps to UTC format
        start_time_utc = datetime.fromisoformat(start_time)
        end_time_utc = datetime.fromisoformat(end_time)

        formatted_payload = {
            "attendees": participants_list,
            "timeConstraint": {
                "timeslots": [
                    {
                        "start": {
                            "dateTime": start_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "timeZone": "UTC"
                        },
                        "end": {
                            "dateTime": end_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "timeZone": "UTC"
                        }
                    }
                ]
            },
            "locationConstraint": {
                "isRequired": False,
                "suggestLocation": True,
                "locations": [
                    {
                        "displayName": "Conference Room",
                        "locationEmailAddress": "conference-room@example.com"
                    }
                ]
            },
            "meetingDuration": "PT1H"  # Meeting duration of 1 hour
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(api_endpoint, json=formatted_payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            availability_timings = []

            for suggestion in data.get("meetingTimeSuggestions", []):
                start_time_utc = suggestion.get("meetingTimeSlot", {}).get("start", {}).get("dateTime", "")
                end_time_utc = suggestion.get("meetingTimeSlot", {}).get("end", {}).get("dateTime", "")

                if start_time_utc and end_time_utc:
                    availability_timings.append((start_time_utc, end_time_utc))

            availability_json = []

            for start_time, end_time in availability_timings:
                availability_json.append({
                    "Start Time (UTC)": start_time,
                    "End Time (UTC)": end_time,
                })

            return json.dumps(availability_json)
        else:
            return json.dumps({"Error": f"{response.status_code} - {response.text}"})
        
    # def find_meeting_times(participants, start_time, end_time):

    # # Define the API endpoint
    #     api_endpoint = "https://graph.microsoft.com/v1.0/me/findMeetingTimes"
    #     access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IlF6cjJldXJPNUlfLXdmeVdZU3pGazAzMDdjRDhMdWxhOHNfN0hqWVI0TG8iLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMGZiZGUyYi1kZTJiLTRmZWEtODMyMC0zMzczYzIyNzg1NzQvIiwiaWF0IjoxNjk3NTE3NjcxLCJuYmYiOjE2OTc1MTc2NzEsImV4cCI6MTY5NzYwNDM3MSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQWcwbElkWGdzQkI5TWxoSGM4eTQ5NWl2aWhwMXVKYTNnWDFWQWxZenpqek83WWU3U29tVCtuV3VZc1BrTzM2M3FCZ0pJbFBSRXlvRjVTdU9YL2RPVGFYTWRpZU5JTUM3YmxCdmFkS09EbFY0PSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiVCIsImdpdmVuX25hbWUiOiJIZW1hY2hhbmRpcmFuIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTA2LjIxMS4yMjkuMTE2IiwibmFtZSI6IkhlbWFjaGFuZGlyYW4gVCIsIm9pZCI6ImJhMDBmYjc2LTRhM2YtNGI5Yi05OTJhLTVkZTAxOWI3NDUxZiIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwMkY4NTZBRjVFIiwicmgiOiIwLkFiMEFLOTc3b0N2ZTZrLURJRE56d2llRmRBTUFBQUFBQUFBQXdBQUFBQUFBQUFETEFHNC4iLCJzY3AiOiJDYWxlbmRhcnMuUmVhZC5TaGFyZWQgQ2FsZW5kYXJzLlJlYWRXcml0ZS5TaGFyZWQgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50TWFuYWdlZERldmljZXMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50U2VydmljZUNvbmZpZy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50U2VydmljZUNvbmZpZy5SZWFkV3JpdGUuQWxsIERpcmVjdG9yeS5SZWFkLkFsbCBvcGVuaWQgcHJvZmlsZSBVc2VyLlJlYWQgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJXQ2FrNVp0NXIzRkgyengwVlRhMHB3NVZCdGExWUloaGl4WFlkMnd5VlRRIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik5BIiwidGlkIjoiYTBmYmRlMmItZGUyYi00ZmVhLTgzMjAtMzM3M2MyMjc4NTc0IiwidW5pcXVlX25hbWUiOiJIZW1hY2hhbmRpcmFuQDhrMGdmMS5vbm1pY3Jvc29mdC5jb20iLCJ1cG4iOiJIZW1hY2hhbmRpcmFuQDhrMGdmMS5vbm1pY3Jvc29mdC5jb20iLCJ1dGkiOiJwcjltVnc4RlZVeVhSNDR5TjZsN0FBIiwidmVyIjoiMS4wIiwid2lkcyI6WyI2MmU5MDM5NC02OWY1LTQyMzctOTE5MC0wMTIxNzcxNDVlMTAiLCJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJ6cjVPdklsV3F3OE5rNEs3X1hFZWVlbUhSUHFOdk92MHp0UERaWVNwZGljIn0sInhtc190Y2R0IjoxNjk1NTEwMzY5fQ.Crr444pPLt-WeZnDWr1NTN7Ag93lEoo4AWIN1dFXLFrWliutDckwOWqky25GVQ0OqZuruP5b9L-Qf84p0xcdd1FRlifwzEhrfuyCF4Cbv0otBOwJ8dukLOflxw0dxy0fiCszi2ud81dSDxQRJhXw8B02qM0Hagthlm2FuIwF4aj3iVxkvOUPSKhlyk8Hq1Q-FbFOxze4bS7j0ppak3uVAWc_aYJ_pi_SVBLL7C5J07kYNxQwt7jr8HxdrrypMDa1PLtlwn4lbIqDz14Xd9PW_PiXlP2ADwBN8EodInnpxOLGLsR5tvubJK6EzGrHhEcphdAqFOCjor8-vn7cqbknxw"
    #     print(start_time, end_time)
    #     # now = datetime.now(pytz.timezone('Asia/Kolkata'))
    #     # ist_timezone = pytz.timezone('Asia/Kolkata')

    #     # # Calculate the start of the current day in IST
    #     # start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    #     # start_time = start_of_day.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    #     # print("start time" ,start_time)

    #     # ist_timezone = pytz.timezone('Asia/Kolkata')
    #     # now = datetime.now(ist_timezone)
    #     # current_date_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    #     # # Calculate the end of the current day in IST
    #     # end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    #     # end_time = end_of_day.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    #     # print("endTime", end_time)

    #     # Define the request headers
    #     headers = {
    #         "Authorization": "Bearer " + access_token,
    #         "Content-Type": "application/json",
    #     }

    # # Define a list of email addresses of participants
    #     participants = [
    #         # "AdeleV@8k0gf1.onmicrosoft.com",
    #         "AlexW@8k0gf1.onmicrosoft.com",

    #         # Add more email addresses as needed
    #     ]

    #     # Create the attendees list for the request payload
    #     attendees = [{"emailAddress": {"address": email}, "type": "required"} for email in participants]

    #     # Define the request payload
    #     payload = {
    #         "attendees": attendees,
    #         "timeConstraint": {
    #             "activityDomain": "work",
    #             "timeslots": [
    #                 {
    #                     "start": {
    #                         "dateTime": "start_time",
    #                         "timeZone": "UTC"
    #                     },
    #                     "end": {
    #                         "dateTime": "end_time",
    #                         "timeZone": "UTC"
    #                     }
    #                 }
    #             ]
    #         }
    #     }

    #     # Make the API request
    #     response = requests.post(api_endpoint, json=payload, headers=headers)

    #     # Check for a successful response
    #     if response.status_code == 200:
    #         data = response.json()

    #         # Extract and print availability timings in IST
    #         availability_timings = []

    #         for suggestion in data.get("meetingTimeSuggestions", []):
    #             start_time_utc = suggestion.get("meetingTimeSlot", {}).get("start", {}).get("dateTime", "")
    #             end_time_utc = suggestion.get("meetingTimeSlot", {}).get("end", {}).get("dateTime", "")

    #             if start_time_utc and end_time_utc:
    #                 # Remove the fractional part of seconds
    #                 start_time_utc = re.sub(r'\.\d+', '', start_time_utc)
    #                 end_time_utc = re.sub(r'\.\d+', '', end_time_utc)

    #                 # Convert UTC times to IST
    #                 ist = pytz.timezone('Asia/Kolkata')
    #                 start_time_ist = datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%S")
    #                 end_time_ist = datetime.strptime(end_time_utc, "%Y-%m-%dT%H:%M:%S")
    #                 start_time_ist = ist.localize(start_time_ist).astimezone(ist)
    #                 end_time_ist = ist.localize(end_time_ist).astimezone(ist)

    #                 availability_timings.append((start_time_ist, end_time_ist))

    #         # Print the availability timings in IST
    #         for start_time, end_time in availability_timings:
    #             return json.dumps(f"Start Time (IST): {start_time}, End Time (IST): {end_time}")
    #     else:
    #         return json.dumps(f"Error: {response.status_code} - {response.text}")
            
    

    @staticmethod   
    def get_events():
        try:
            access_token = OpenAIFunctions.getEvents

            # Microsoft Graph API endpoint for retrieving events (meetings)
            api_url = "https://graph.microsoft.com/v1.0/me/events"

            headers = {
                "Authorization": f"Bearer {access_token}",
            }

            # Send a GET request to retrieve the user's events (meetings)
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                events = response.json().get("value", [])
                
                # Extract subject, start time, end time, and location for each event
                event_info = []
                for event in events:
                    subject = event.get("subject", "")
                    start_time = event.get("start", {}).get("dateTime", "")
                    end_time = event.get("end", {}).get("dateTime", "")
                    location = event.get("location", {}).get("displayName", "")
                    
                    event_info.append({
                        "subject": subject,
                        "start_time": start_time,
                        "end_time": end_time,
                        "location": location
                    })
                
                # Convert the event_info list to a JSON string
                event_info_json = json.dumps(event_info)
                
                return event_info_json
            else:
                error_message = f"Failed to retrieve events. Status code: {response.status_code}"
                return json.dumps({"error": error_message, "response": response.text})

        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"})
                




    
    


FUNCTIONS_MAPPING = {
    "get_search_results": OpenAIFunctions.get_search_results,
    "get_current_weather": OpenAIFunctions.get_current_weather,
    "search_images": OpenAIFunctions.search_images,
    "service_now_ticket_creation":OpenAIFunctions.service_now_ticket_creation,
    "get_incident_status_by_number":OpenAIFunctions.get_incident_status_by_number,
    "get_recent_incidents_status":OpenAIFunctions.get_recent_incidents_status,
    "add_comment_to_incident":OpenAIFunctions.add_comment_to_incident,
    #"get_access_token":OpenAIFunctions.get_access_token,
    "send_email_via_graph_api":OpenAIFunctions.send_email_via_graph_api,
    "schedule_meeting_via_graph_api":OpenAIFunctions.schedule_meeting_via_graph_api,
    "cancel_meeting_by_name_via_graph_api":OpenAIFunctions.cancel_meeting_by_name_via_graph_api,
    "get_events":OpenAIFunctions.get_events,
    #"get_free_time_slots":OpenAIFunctions.get_free_time_slots,
    "find_free_meeting_times":OpenAIFunctions.find_free_meeting_times
}
