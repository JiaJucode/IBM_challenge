
from textwrap import dedent
from ai_config import get_ai_response
from helpers import markdown_to_html


def modify_search_query(query: str) -> str:
    '''
    Modifies search query to be optimized for Google Search
    For now it just returns the query as is
    '''
    return query


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