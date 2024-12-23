import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import load_dotenv
from functions import rag_lookup

# from slack_sdk.errors import SlackApiError
# from slackeventsapi import SlackEventAdapter
# import slack


load_dotenv('./.env')

#### Intialize application with Slack Bot Credentials stored in environment variables ####
app = App(token=os.environ['SLACK_BOT_TOKEN'])  


#### Initialize Flask App ####
flask_app = Flask(__name__) 

#### Initialize Slack Events Handler ####
handler = SlackRequestHandler(app)

#### Connect to Slack WebClient API ####
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


#### Handle requests made to /slack/events ####
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


#### If event is a mention of the bot run cutom function ####
@ app.event('app_mention')
def app_mention(body):
    
    channel_id = body["event"]["channel"]                                # Channel where the event was triggered
    user_id = body["event"]["user"]                                      # User who triggered the event
    text = body["event"]["text"]                                        # Text of the message that triggered the event      

    response = rag_lookup(text)                                      # Calling RAG function from functions file to trigger AI powered response

#### Post Response ####
    client.chat_postEphemeral(channel=channel_id, user=user_id, text=response)  
    

if __name__ == "__main__":
    flask_app.run(port=5002, debug=True)