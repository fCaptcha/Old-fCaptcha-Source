from datetime import datetime, timezone, timedelta
from websocket import create_connection
import urllib.parse
import requests
import json

class binggpt:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'authority': 'copilot.microsoft.com',
            'accept': 'application/json',
            'accept-language': 'en-US;q=0.9,en;q=0.8',
            'referer': 'https://copilot.microsoft.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-ms-client-request-id': '5e2ba668-a315-422e-8bc1-2b699da1b29f',
            'x-ms-useragent': 'azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.12.3 OS/Windows',
        })

    def get_result(self) -> requests.Response:
        return self.session.get('https://copilot.microsoft.com/turing/conversation/create', params={'bundleVersion': '1.1573.4'})

    @staticmethod
    def get_data(result: requests.Response) -> tuple:
        data = result.json()
        return result.headers["X-Sydney-Encryptedconversationsignature"], data["conversationId"], data["clientId"]

    @staticmethod
    def get_time() -> str:
        now = datetime.now().astimezone(timezone(timedelta(hours=1)))
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        return timestamp[:-2] + ':' + timestamp[-2:]

    def ask(self, text: str) -> str:
        text = f"srictly respond to the following question with a single word, number, or phrase. and do not use any emojis: {text}"
        result = self.get_result()
        token, convo_id, client_id = self.get_data(result)
        ws = create_connection(f"wss://sydney.bing.com/sydney/ChatHub?sec_access_token={urllib.parse.quote(token)}")
        ws.send('{"protocol":"json","version":1}\x1e')

        while ws.connected:
            message = ws.recv()
            data = message.split("\x1e")

            for clean in data:
                if clean == "":
                    continue

                j = json.loads(clean)

                if clean == "{}":
                    ws.send('{"type":6}\x1e')
                    timestamp = self.get_time()
                    j2 = {
                        "arguments": [
                            {
                                "source": "cib",
                                "optionsSets": [
                                    "nlu_direct_response_filter", "deepleo", "disable_emoji_spoken_text",
                                    "responsible_ai_policy_235", "enablemm", "dv3sugg", "iyxapbing",
                                    "iycapbing", "h3precise", "clgalileo", "gencontentv3", "storagev2fork",
                                    "papynoapi", "gndlogcf", "gptvnoex"
                                ],
                                "allowedMessageTypes": [
                                    "ActionRequest", "Chat", "ConfirmationCard", "Context",
                                    "InternalSearchQuery", "InternalSearchResult", "Disengaged",
                                    "InternalLoaderMessage", "Progress", "RenderCardRequest",
                                    "RenderContentRequest", "AdsQuery", "SemanticSerp",
                                    "GenerateContentQuery", "SearchQuery", "GeneratedCode"
                                ],
                                "sliceIds": [
                                    "bgstreamcf", "designer2cf", "suppsm240hm", "srchqryfix", "suppsm240-t",
                                    "cmcpupsalltf", "sydtransctrl", "proupsallcf", "0209bicv3", "130memrev",
                                    "116langwbs0", "927storev2fk", "0208papynoa", "sapsgrds0", "1119backoss0",
                                    "enter4nl"
                                ],
                                "verbosity": "verbose",
                                "scenario": "SERP",
                                "plugins": [],
                                "conversationHistoryOptionsSets": [
                                    "autosave", 
                                    "savemem", 
                                    "uprofupd", 
                                    "uprofgen"
                                ],
                                "isStartOfSession": True,
                                "message": {
                                    "locale": "en-US",
                                    "timestamp": timestamp,
                                    "author": "user",
                                    "inputMethod": "Keyboard",
                                    "text": text,
                                    "messageType": "Chat"
                                },
                                "tone": "Precise",
                                "spokenTextMode": "None",
                                "conversationId": convo_id,
                                "participant": {
                                    "id": client_id
                                }
                            }
                        ],
                        "invocationId": "0",
                        "target": "chat",
                        "type": 4
                    }
                    ws.send(json.dumps(j2) + "\x1e")
                    continue

                try:
                    if j["type"] == 2:
                        ws.close()
                        return j["item"]["result"]["message"]
                except KeyError:
                    continue

        return "Milk"