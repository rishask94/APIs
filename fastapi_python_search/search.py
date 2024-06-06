"Uses Google's site-specific search API to look for the specified term on a website"
import json
from collections import defaultdict

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found")
  
data = defaultdict(list)
term_and_link = defaultdict(list)
all_urls = []

def siteSpecificSearch(url, term):                   
    data['url'] = url
    data['content_present_bool'] = False
    data['content_present'] = "-"
    data['links'] = []
    unique_terms = []
    specificSearch = "site:" + url
    
    newQuery = specificSearch + " \""+term+"\""
    print(newQuery)

    for newSearch in search(newQuery, tld="com", num=10, stop=10, pause=2):
        data['content_present_bool'] = True
        if term not in unique_terms:
            unique_terms.append(term)
        data['content_present'] = term
        term_and_link[term].append(newSearch)
        all_urls.append(newSearch)
        
        data['links']= all_urls
        print(data)

    json_object = json.dumps(data, indent=4)
    
    # Writing to sample.json
    """
    with open("sample_term.json", "w") as outfile:
        outfile.write(json_object)
    """
    return data

