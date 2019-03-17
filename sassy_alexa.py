"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def responses(p_name, spe_recy, common_recy, sp_trash, common_trash):
    rr_t = [p_name + ", belongs in the trash", p_name + " goes in the trash can", "That is garbage", "That does not go into recycling", "Not recyclable"]
    rr_r = [p_name + ", belongs in the recycling", p_name + " that goes in the recycling", "Help the environment by recycling that", "Recyclable"]
    sr_t = ['Am I a joke to you?', 'That was cute. Try again.', 'Take that to the trash along with your question.', 
    'What are you five?', 'Really?', 'I can recite pi to a thousand decimal places and you ask me this?', 
    'Do me a favour and do not recycle that question.', 'You are the reason why robots will take over the world one day.', 
    'one zero zero one one one one zero one zero zero zero. Hang on. You do not understand that. Never mind.', 'Go ask siri that.']
    sr_r = ['Take that to recycling and take your question to the trash.','Am I a joke to you?', 'That was cute. Try again.', 
    'What are you five?', 'Really?', 'I can recite pi to a thousand decimal places and you ask me this?', 'You are the reason why robots will take over the world one day.', 
    'one zero zero one one one one zero one zero zero zero. Hang on. You do not understand that. Never mind.', 'Go ask siri that.']
    g_r = ['I don\'t think I recognize that']
    
    if spe_recy == 1:
        index = random.randint(0, len(rr_r)-1)
        return rr_r[index]
    elif common_recy == 1:
        index = random.randint(0, len(sr_r)-1)
        return sr_r[index]
    elif sp_trash == 1:
        index = random.randint(0, len(rr_t)-1)
        return rr_t[index]
    elif common_trash == 1:
        index = random.randint(0, len(sr_t)-1)
        return sr_t[index]
    else:
        return g_r[0]

def get_recycle_this_response(intent):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    product_name = intent['slots']['product']['value']
    card_title = "response for recycle"
    special_recycle = ["envelope", "craft paper", "egg cartons", "foil", "aluminium foil", "tires", "crayons", "rubber"]
    regular_recycle = ["paper", "furniture", "water", "magazines", "cardboard", "glass", "plastic", "metal", "can"]
    special_trash = ["pizza boxes", "diaper", "diapers", "styrofoam", "compost", "yard waste", "electronics", "clothes",
            "cord", "cords", "rope", "hoses", "cable", "bubble wrap", "mirror", "ceramics"]
    regular_trash = ["food", "plastic", "polybags",  "egg shells", "shopping bag", "wrapper", "comic sans"]
    
    print(product_name)
    y = 0
    for x in special_recycle:
        if product_name == x:
            print("here")
            speech_output = responses(product_name.lower(), 1, 0, 0, 0)
            y = 1
            break
    for x in regular_recycle:
        if product_name == x:
            speech_output = responses(product_name.lower(), 0, 1, 0, 0)
            y = 1
            break
    for x in special_trash:
        if product_name == x:
            speech_output = responses(product_name.lower(), 0, 0, 1, 0)
            y = 1
            break
    for x in regular_trash:
        if product_name == x:
            speech_output = responses(product_name.lower(), 0, 0, 0, 1)
            y = 1
            break
    if y == 0:
        speech_output = responses(product_name.lower(), 0, 0, 0, 0)
    
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Don't tell me what to do."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "I thought this would never end. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "recycle_this":
        return get_recycle_this_response(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])