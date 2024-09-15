import os
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Load environment variables
load_dotenv()  
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_project_id = os.getenv("IBM_PROJECT_ID")

MODEL_ID = ModelTypes.GRANITE_13B_CHAT_V2

model = Model(
    model_id=MODEL_ID,
    params={
        GenParams.MAX_NEW_TOKENS: 900,
        GenParams.RETURN_OPTIONS: {
            'input_text': True,
            'generated_tokens': True,
        },
    },
    credentials=Credentials(
        api_key=ibm_api_key,
        url="https://us-south.ml.cloud.ibm.com",
    ),
    project_id=ibm_project_id,
)


base_prompt_template = \
"""<|system|>
{system_message}

<|user|>
{user_message}

<|assistant|>
"""


def get_ai_response(system_prompt, user_prompt):
    prompt = base_prompt_template.format(system_message=system_prompt, user_message=user_prompt)
    generated_response = model.generate(prompt=prompt)
    
    response_text = generated_response['results'][0]['generated_text']
    response_text = response_text[response_text.index('<|assistant|>') + len('<|assistant|>'):].strip()
    
    return response_text

# trying out
if __name__ == "__main__":

    system_prompt = "You are a helpful assistant that replies very briefly in the fewest words possible. You are extremely succint and use small words and few words."

    user_prompt = "What's the best laptop brand these days?"
    response = get_ai_response(system_prompt, user_prompt)
    print(f"{user_prompt}\n{response}\n\n")

    user_prompt = "Summarize Naval Ravikant's thoughts on wealth creation."
    response = get_ai_response(system_prompt, user_prompt)
    print(f"{user_prompt}\n{response}\n\n")
