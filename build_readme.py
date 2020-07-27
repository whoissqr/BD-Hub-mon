from python_graphql_client import GraphqlClient
import feedparser
import httpx
import json
import pathlib
import re
import os
import datetime
from blackduck.HubRestApi import HubInstance
import json
import pprint


root = pathlib.Path(__file__).parent.resolve()


if __name__ == "__main__":


    urlbase = "https://poc94.blackduck.synopsys.com/"
    TOKEN = os.environ.get("HUB_94_TOKEN", "")
    hub = HubInstance(urlbase, api_token=TOKEN, insecure=True)

    projects = hub.get_projects(5)

    print(json.dumps(projects.get('items', [])))



    readme = root / "README.md"
    pp = pprint.PrettyPrinter(indent=4)

    rewritten = "demo hub status === \n"
    rewritten += pp.pprint(json.dumps(projects.get('items', [])))

    readme.open("w").write(rewritten)
