import time
from openai import OpenAI
from pathlib import Path
import os
import json
from .ai_functions import *
from .ai_roles import *
from termcolor import colored

_ai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

thread = _ai_client.beta.threads.create()

my_assistant = _ai_client.beta.assistants.create(
        instructions=Roles.DETERMINE_CRUD.value,
        name="Crud Interpretor",
        tools=all_functions,
        model="gpt-4o",
    )


def send_operation_outcome(run_id, thread_id, tool_call_id, outcome):

    _ai_client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=[
            {
            "tool_call_id": tool_call_id,
            "output": outcome,
            }
        ]
    )


def determine_crud(message):
    try:
        if not message:
            return ""
        print('determining crud operation...')

        user_message= _ai_client.beta.threads.messages.create(
            thread.id,
            role="user",
            content=message,
        )
        run = _ai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=my_assistant.id,
        )

        while True:
            run_status = _ai_client.beta.threads.runs.retrieve(run.id, thread_id=thread.id)
            print(colored('run', 'light_yellow'))
            print(run_status)
            print()

            if run_status.status == 'completed':
                all_messages=_ai_client.beta.threads.messages.list(thread_id=thread.id)
                print(colored('All messages', 'green'))
                print(all_messages)
                ai_response = all_messages.data[0].content[0].text.value
                print(ai_response)
                return ai_response

            elif run_status.status == 'requires_action':
                print(run_status.required_action.submit_tool_outputs.tool_calls)


                all_functions = run_status.required_action.submit_tool_outputs.tool_calls

                for function in all_functions:

                    function_arguments = json.loads(function.function.arguments)
                    tool_call_id = run_status.required_action.submit_tool_outputs.tool_calls[0].id

                    match function.function.name.upper():

                        case "GET_CLIENT_INFO":

                            print(colored(function_arguments, 'blue'))
                            break

                        case "GET_SALES_REPORT":

                            print(colored(function_arguments, 'blue'))
                            break
                        case "GET_INVENTORY_REPORT":

                            print(colored(function_arguments, 'blue'))
                            break
                        case "UPDATE_CLIENT_INFO":

                            print(colored(function_arguments, 'blue'))
                            break
                        case "UPDATE_INVENTORY":

                            print(colored(function_arguments, 'blue'))
                            break
                        case "ADD_CLIENT":

                            print(colored(function_arguments, 'blue'))
                            send_operation_outcome(run.id, thread.id, tool_call_id, "{success: true, message: client added}" )
                            break
                        case "ADD_TO_INVENTORY":

                            print(colored(function_arguments, 'blue'))
                            break

                        case "DELETE_CLIENT":

                            print(colored(function_arguments, 'blue'))
                            break

                        case "DELETE_INVENTORY":

                            print(colored(function_arguments, 'blue'))
                            break

                    run_status = _ai_client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[
                                {
                                "tool_call_id": run_status.required_action.submit_tool_outputs.tool_calls[0].id,
                                "output": "{success: true, message: crud operation determined, continue gathering the following information}"
                                }
                            ]
                        )
                    
            elif run_status.status == 'failed':
                raise Exception("Run failed")
            
            time.sleep(1)  # Wait before polling again
    except:
        
        print('failed to add the things')
        return "unable to proccess your request please try again"

def transcribe_audio(audio_path):
    response = {"message": "",
                "is_success": True,
                }
    audio_file = Path(audio_path)
    try:
        transcription = _ai_client.audio.transcriptions.create(
			model="whisper-1", 
			file=audio_file
		)
        response['message'] = transcription.text
    except Exception as e:
        response['is_success'] = False
        response['message'] = str(e)
    finally:
        return response
    

def text_to_audio(text:str):
    response = _ai_client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text,
)

    response.write_to_file("response2.mp3")

    return "response.mp3"