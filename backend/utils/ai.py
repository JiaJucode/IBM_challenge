
from textwrap import dedent
from ai_config import get_ai_response
from helpers import markdown_to_html


def paraphrase_lookup(query: str, sentences: list[str]):
    '''TODO
    Find through a set of sentences, which one means exactly the same as the input sentence?
    e.g. Cook dinner by myself = Prepare dinner on my own
    May use Transforers or other light-weight models
    '''
    pass

def process_search_query(query: str) -> str:
    '''
    Modifies search query to be optimized for Google Search
    For now it just returns the query as is
    '''
    system_prompt = dedent(
        """Your role is to extract key information from long sentences and paragraphs. You help users communicate their questions, 
        requirements, and needs with Internet search engine. Users want their requests to be summarized into search terms. 
        Both the conciseness and relavance of your summary are important factors. 
        To achieve the goal, you first need to know the topic or academic field related to what the user asks. 
        Then, consider user's expectations, like the format of answers they with to receive. Based on these, you tell the user 
        what words to put in the Internet search that best summarizes their needs.
        """
    )
    user_prompt = dedent(
        f"""I'm now searching the Internet to find some information or solution about this: "{query}". Please summarize 
        my needs into search terms that contain fewer words and cover all my requirements. 
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