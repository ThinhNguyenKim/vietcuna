from obsei.source.website_crawler_source import TrafilaturaCrawlerConfig, TrafilaturaCrawlerSource
from googlesearch import search
import warnings
import os

# Redirect warnings to a null device
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)


# text = input('Input your query: ')


def search_url(query):
    search_results = search(query, num_results=8)
    
    for result in search_results:
        if not result.endswith(".aspx"):
            return result
    
    return None


def get_context(url):

    try:
        config = TrafilaturaCrawlerConfig(urls=[url])
        response = TrafilaturaCrawlerSource()
        response_list = response.lookup(config)

        for item in range(len(response_list)):
            response_list[item] = dict(response_list[item])
            content = response_list[item]["meta"]["raw_text"]
    except:
        raise ValueError("Your configuration is not valid!")
        
    return content


def create_instruction(input):
    url = search_url(input)
    context = get_context(url)
    instruction = f"""Cho đoạn văn sau: {context}
                      Theo đoạn văn trên: {input}"""
    return instruction

