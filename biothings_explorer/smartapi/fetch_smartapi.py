from pathlib import Path
import json
import requests

CURRENT_PATH = Path(__file__)
SPECS_FOLDER_PATH = Path.joinpath(CURRENT_PATH.parent, 'specs')
SMARTAPI_URL = 'http://smart-api.info/api/query/?q=tags.name:translator&size=200'

def create_specs_folder():
    """Create an empty folder storing smartapi specs."""
    if Path(SPECS_FOLDER_PATH).exists():
        # remove existing docs in the folder
        for x in Path(SPECS_FOLDER_PATH).iterdir():
            Path.unlink(x)
    else:
        Path.mkdir(SPECS_FOLDER_PATH)
        print("'{}' folder has been created!".format(SPECS_FOLDER_PATH))

def check_if_exists_x_bte_kgs_operation(specs):
    """Check if x-bte-kgs-operation field presents in smartapi specs.

    :param: specs: the JSON smartapi specs
    """
    return 'components' in specs and 'x-bte-kgs-operations' in specs['components']
 
def get_api_title(specs):
    """Fetch the API title

    :param: specs: the JSON smartapi specs
    """
    return specs['info']['title']

def write_to_file(title, specs):
    """Write the smartapi json into a file

    :param: tilte: the tile of the API
    :param: specs: the JSON smartapi specs
    """
    file_name = str(title) + '.json'
    file_path = Path.joinpath(SPECS_FOLDER_PATH, file_name)
    with open(file_path, 'w') as outfile:
        json.dump(specs, outfile)

def fetch_smartapi_docs():
    """fetch all smartapi files from smartapi registry with translator tags"""
    try:
        smartapi_docs = requests.get(SMARTAPI_URL).json()
    except ConnectionError:
        print("unable to fetch from smartapi")
        return {}
    return smartapi_docs

def main():
    """pull data from smartapi and write to local files"""
    create_specs_folder()
    smartapi_docs = fetch_smartapi_docs()
    if smartapi_docs:
        for _doc in smartapi_docs['hits']:
            if check_if_exists_x_bte_kgs_operation(_doc):
                title = get_api_title(_doc)
                write_to_file(title, _doc)


if __name__ == '__main__':
    main()
