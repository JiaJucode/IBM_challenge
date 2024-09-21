
from textwrap import dedent
from utils.ai_config import get_ai_response
from utils.helpers import markdown_to_html

def create_chat_title(query: str) -> str:
    system_prompt = dedent(
        """You are a helpful secretary, and your role is to help users summarize and take notes of what they said. Users want 
        their words to be summarized into shorter forms like newspaper headlines, which is helpful for their future reference.
        To achieve the goal, you need to know the topic or academic field related to what the user says. You don't need to provide
        any answer or inject your own opinion.
        """
    )
    user_prompt = dedent(
        f"""I talked to an expert about this issue: "{query}". Please summarize my issue, provide only the summary you made.
        """
    )
    response = get_ai_response(system_prompt=system_prompt, messages=[{"role": "user", "content": user_prompt}])
    return response

def process_search_query(query: str) -> str:
    '''
    Modifies search query to be optimized for Google Search
    For now it just returns the query as is
    '''
    system_prompt = dedent(
        """Your role is to extract key information from long sentences and paragraphs. You help users communicate their questions, 
        requirements, and needs with Internet search engine. Users want their requests to be summarized web search terms. 
        Conciseness and relavance of your summary are very important factors, but grammar and coherence are not.
        To achieve the goal, you first need to know the topic or academic field related to what the user asks. 
        Then, consider user's expectations. Based on these, you tell the user what words to put in the Internet search box.
        """
    )
    user_prompt = dedent(
        f"""I'm now searching the Internet to find some information or solution about this: "{query}". Please summarize 
        my needs into search terms that contain no more words and cover all my requirements. 
        If original input is too long, then create a set of search terms with each covering part of my needs, separating each term 
        by semi-colon. Otherwise, write one search term with no semi-colon. No need to be grammatically correct.
        """
    )

    response = get_ai_response(system_prompt=system_prompt, messages=[{"role": "user", "content": user_prompt}])
    return response


def summarize_search_results(search_query: str, search_results: list) -> str:
    '''
    Summarizes search results to be displayed to the user.
    It expects to recieve a list of search results where each result is a dictionary with the following keys:
        - title
        - link
        - content
    '''
    
    system_prompt = dedent(
        """You are an expert content curator specializing in extracting meaningful information and summarizing search results.
        You are able to read through multiple search results, understand them, analyze them individually and overall for accuracy, reliability, and relevance, and distill
        the most important information into a concise summary in markdown format. The goal of your distillation is to provide the user with a quick and accurate overview of
        their search query, such that they can quickly understand without having to read through all of them and waste time in finding most relevant and accurate information.
        You recieve the user's search query and a list of search results where each result is a dictionary with "title", "link", and "content" keys. 
        Your response markdown should be well formatted with various appropriate elements like headings, tables, lists, etc. to make it easy to read and understand.
        """
    )
    user_prompt = dedent(
        f"""Give summary of the search results for the query: "{search_query}" with the following search results in markdown format:

        # Search Results:
        {search_results}
        """
    )

    response = get_ai_response(system_prompt=system_prompt, messages=[{"role": "user", "content": user_prompt}])
    return markdown_to_html(response)



def chat(query: str, context: dict, message_history: list) -> str:
    '''
    Returns chat response for a user query
    '''
    system_prompt = dedent(
        f"""You are a helpful AI chatbot for search results queries that replies very briefly, succintly, in the fewest words possible without any extra information, suggestions, or opinions.
        You respond to user queries related to summarized google search results, which you are provieded with below. Answer only from the information provided in the search results
        and if a query isnt related to the information or you can't answer it for any reason, reply appropriately like telling the user that the query isn't related to the search results
        or that you can't answer it.

        Search Results:
        {context}
        """
    )
    user_prompt = dedent(
        f"""{query}
        """
    )
    messages = [*message_history, {"role": "user", "content": user_prompt}]
    response = get_ai_response(system_prompt=system_prompt, messages=messages)

    return response