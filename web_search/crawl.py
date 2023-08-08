from website_crawler_source import TrafilaturaCrawlerConfig, TrafilaturaCrawlerSource

def get_website_content(urls):
    
    try:
        config = TrafilaturaCrawlerConfig(urls=urls)
        response = TrafilaturaCrawlerSource()
        response_list = response.lookup(config)

        for item in range(len(response_list)):
            response_list[item] = dict(response_list[item])
            content = response_list[item]["meta"]["raw_text"]

    except:
        raise ValueError("Your configuration is not valid!")
        
    return content