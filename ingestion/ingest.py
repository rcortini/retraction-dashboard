import os, sys
import pandas as pd
import requests

from shared.db import create_connection, get_last_update_ts, upsert_records
from shared.models import works

# a handy function to execute queries
def send_query(q, params={}, print_query=False):
    if print_query:
        print(q)
    response = requests.get(q, params=params)
    response.raise_for_status()
    return response.json()

def send_oa_query_full_results(q, print_query=False, max_results=None):
    # initialise the results and the cursor
    all_results = []
    cursor = '*'
    n_results = 0

    # loop until the cursor is None
    while cursor:

        # this stops the iteration if we reached the maximum
        if max_results:
            if n_results >= max_results:
                break

        # set cursor value and request page from OpenAlex
        these_results = send_query(q, params={'cursor' : cursor}, print_query=print_query)

        # update cursor to meta.next_cursor
        cursor = these_results['meta']['next_cursor']

        # add these results to all the results
        all_results.append(these_results)

        # keep track of the number of results
        n_results += len(these_results['results'])

    return all_results

def process_oa_results(oa_data,
        requested_fields=['id', 'title', 'publication_date', 'abstract_inverted_index']):
    """Convert a list of json-like dictionary objects that are retrieved from the OpenAlex API
    to a pandas dataframe with given columns.
    
    Parameters:
    - results[list or dict]: list of json-like dictionary objects, or single json-like dictionary
    object that contains the data retrieved from the OpenAlex API
    - requested_fields[list] (optional): list of strings specifying the values to extract from the
    data retrieved from OpenAlex
    
    Returns:
    - pandas.DataFrame: containing one row per record with specified columns"""
    
    # internal helper function to iterate results
    def iterate_results(page_results):
        processed_papers = []
        for paper in page_results:
            d = {}
            for field in requested_fields:
                d[field] = paper[field]
            processed_papers.append(d)
        return processed_papers

    # if the data type is a dictionary, proceed to process the results directly  
    if type(oa_data) == dict:
        return pd.DataFrame(iterate_results(oa_data['results']))
   
    # if it is a list, then process each page
    elif type(oa_data) == list:
        
        # initialise output data structure
        all_results = []
        for page in oa_data:
            d = iterate_results(page['results'])
            all_results.extend(d)
            
        return pd.DataFrame(all_results)

    else:
        raise ValueError("oa_data must be either dict or list")

# this function reconstructs an abstract from the inverted index that OA returns
def reconstruct_abstract(abstractInvertedIndex):
    """Reconstruct an abstract from an abstract_inverted_index object from
    OpenAlex
    
    Parameters:
        - abstractInvertedIndex[str]: an object coming directly from an OpenAlex
        query
        
    Returns:
        - abstract[str]: the reconstructed abstract"""

    # check if NaN
    if pd.isna(abstractInvertedIndex):
        return ""

    word_index = []
    for k,v in abstractInvertedIndex.items():
        for index in v:
            word_index.append([k,index])
    word_index = sorted(word_index, key = lambda x : x[1])
    return ' '.join([w[0] for w in word_index])

def fix_doi(doi):
    return doi.replace("https://doi.org/", "").lower()

def fix_openalex_url(url, concept=''):
    return url.replace(f"https://openalex.org/{concept}", "")

def main():
    # initialize a connection to the database
    engine = create_connection()

    # get timestamp of last update.
    # NOTE: when the app is built for the first time, an artificial
    # timestamp is written in the database, corresponding to 1/1/1900
    last_update_ts = get_last_update_ts(engine)
    
    OA_API_URL = os.getenv("OA_API_URL")
    OA_API_KEY = os.getenv("OA_API_KEY")
    OA_PER_PAGE = os.getenv("OA_PER_PAGE")
    EXEC_MODE = os.getenv("EXEC_MODE")
    if not OA_API_KEY:
        raise ValueError("OA_API_KEY is not set. You must obtain a valid API key to run\nSee https://developers.openalex.org/guides/authentication")

    # build the URL for the request
    URL = f"{OA_API_URL}/works?filter=is_retracted:true,from_updated_date:{last_update_ts}&per_page={OA_PER_PAGE}&api_key={OA_API_KEY}"

    # execute the request in a loop
    if EXEC_MODE == "test":
        data_raw = send_oa_query_full_results(URL, max_results=400)
    elif EXEC_MODE == "no_ingestion":
        print("LOG: ingestion exiting in `no_ingestion` mode")
        return
    else:
        data_raw = send_oa_query_full_results(URL)

    # insertion in the database
    df = process_oa_results(data_raw)
    
    fields = [
        'id',
        'doi',
        'title',
        'publication_year',
        'publication_date',
        'updated_date'
    ]

    data_df = process_oa_results(data_raw, requested_fields=fields)
    records = list(data_df.itertuples(index=False, name=None))
    upsert_records(engine, records)

if __name__ == "__main__":
    main()