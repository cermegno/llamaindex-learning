### ReAct agent with a tool for ServiceNow incidents
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
import httpx

snowurl = 'https://devXXXXX.service-now.com/api/now/table/incident'
snowuser = 'Incident.Manager'
snowpass = ''
snowheaders = {"Content-Type":"application/json","Accept":"application/json"}


def create_servicenow_incident(description: str) -> str:
    """Create an incident in ServiceNow with a description of the problem"""
    payload = '{"short_description":"' + description +'","urgency":"2","priority":"2"}'
    r = httpx.post(snowurl, auth=(snowuser, snowpass), headers=snowheaders ,data=payload, verify=False)
    if r.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    else:
        print("success", r.status_code)
    rjson = r.json()

    print("Incident " + rjson["result"]["number"] + " was created")

    return rjson["result"]["number"]
    
servicenow_incident_tool = FunctionTool.from_defaults(fn=create_servicenow_incident)

llm = Ollama(model="llama3.1:8b-instruct-q8_0", request_timeout=120.0, temperature=0.1)
agent = ReActAgent.from_tools([servicenow_incident_tool], llm=llm, verbose=True)

response = agent.chat("I cannot access my laptop. I think my password is expired. Can you help me?")

print(response)
