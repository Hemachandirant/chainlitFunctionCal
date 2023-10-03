from requests.auth import HTTPBasicAuth
from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
import requests
import json
import os



class OpenAIFunctions:
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

        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

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
        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

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
        auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")

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
    # @staticmethod
    # def add_comment_to_incident(incident_number, comment):

    #     contentdump = OpenAIFunctions.get_incident_status_by_number(incident_number)

    #     content =json.loads(contentdump)

    #     status = content["result"]["state"]
    #     incident_number = content["result"]["number"]
    #     short_description = content["result"]["short_description"]
    #     comments = content["result"]["comments"]
    #     description = content["result"]["description"]
    #     sys_id = content["result"]["sys_id"]

    #     auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")
    #     uri = f"https://wiprodemo4.service-now.com/api/now/table/incident/{sys_id}?sysparm_display_value=true"
    #     headers = {
    #         "Accept": "application/json;charset=utf-8",
    #         "Content-Type": "application/json",
    #     }
    #     payload = {
    #         # "comments_and_work_notes": comment,
    #         "comments" : comment
    #     }
    #     r = requests.patch(url=uri, auth=auth, verify=False, headers=headers, json=payload)
    #     content = r.json()
    #     print("Response Status Code: " + str(content))
    #     return json.dumps(content)

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

            auth = HTTPBasicAuth("adarsh.talinki@wipro.com", "Demo@1234")
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
    def get_access_token():
        # Define the token endpoint and your Azure AD application credentials
        token_url = "https://login.microsoftonline.com/fd50ca56-92c4-4a17-8397-ca4cf2991191/oauth2/v2.0/token"
        client_id = "30296a67-052d-4217-8a6c-c8c984cb98c6"
        client_secret = "_Ot8Q~2bhZloCgOChrwIVrO0l_nIEZ01hI0OPcMY"
        scope = "https://graph.microsoft.com/.default"

        # Create the request payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope
        }

        try:
            # Send the POST request to obtain the access token
            response = requests.post(token_url, data=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                token_data = response.json()

                # Extract the access token from the response
                access_token = token_data.get("access_token")

                return access_token
            else:
                print("Failed to obtain access token. Status code:", response.status_code)
                return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None


    @staticmethod
    def send_email_via_graph_api(access_token, recipient_email, subject, message_body):
        try:
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
                "Authorization": f"Bearer {access_token}",
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
        

        


    # @staticmethod
    # def send_email_via_graph_api(recipient_email, subject, message_body):
    # # Define the token endpoint
    #     token_url = "https://login.microsoftonline.com/fd50ca56-92c4-4a17-8397-ca4cf2991191/oauth2/v2.0/token"

    #     client_id = "30296a67-052d-4217-8a6c-c8c984cb98c6"
    #     client_secret = "_Ot8Q~2bhZloCgOChrwIVrO0l_nIEZ01hI0OPcMY"
    #     scope = "https://graph.microsoft.com/.default"

    #     # Create the request payload for obtaining the access token
    #     token_payload = {
    #         "grant_type": "client_credentials",
    #         "client_id": client_id,
    #         "client_secret": client_secret,
    #         "scope": scope
    #     }

    #     try:
    #         # Send the POST request to obtain the access token
    #         token_response = requests.post(token_url, data=token_payload)

    #         # Check if the request was successful (status code 200)
    #         if token_response.status_code == 200:
    #             # Parse the JSON response to extract the access token
    #             token_data = token_response.json()
    #             access_token = token_data.get("access_token")

    #             if access_token:
    #                 # Microsoft Graph API endpoint for sending emails
    #                 api_url = "https://graph.microsoft.com/v1.0/me/sendMail"

    #                 # Create the email message payload
    #                 email_data = {
    #                     "message": {
    #                         "subject": subject,
    #                         "body": {
    #                             "contentType": "Text",
    #                             "content": message_body
    #                         },
    #                         "toRecipients": [
    #                             {
    #                                 "emailAddress": {
    #                                     "address": recipient_email
    #                                 }
    #                             }
    #                         ]
    #                     }
    #                 }

    #                 headers = {
    #                     "Authorization": f"Bearer {access_token}",
    #                     "Content-Type": "application/json"
    #                 }

    #                 # Send the email using the Graph API
    #                 email_response = requests.post(api_url, headers=headers, data=json.dumps(email_data))

    #                 if email_response.status_code == 202:
    #                     return {"status": "Email sent successfully!"}
    #                 else:
    #                     error_message = f"Failed to send email. Status code: {email_response.status_code}"
    #                     return {"error": error_message, "response": email_response.text}

    #             else:
    #                 return {"error": "Failed to obtain access token."}

    #         else:
    #             error_message = f"Failed to obtain access token. Status code: {token_response.status_code}"
    #             return {"error": error_message, "response": token_response.text}

    #     except Exception as e:
    #         return {"error": f"An error occurred: {str(e)}"}



    
    


FUNCTIONS_MAPPING = {
    "get_search_results": OpenAIFunctions.get_search_results,
    "get_current_weather": OpenAIFunctions.get_current_weather,
    "search_images": OpenAIFunctions.search_images,
    "service_now_ticket_creation":OpenAIFunctions.service_now_ticket_creation,
    "get_incident_status_by_number":OpenAIFunctions.get_incident_status_by_number,
    "get_recent_incidents_status":OpenAIFunctions.get_recent_incidents_status,
    "add_comment_to_incident":OpenAIFunctions.add_comment_to_incident,
    "get_access_token":OpenAIFunctions.get_access_token,
    "send_email_via_graph_api":OpenAIFunctions.send_email_via_graph_api
}
