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
import logging

root = pathlib.Path(__file__).parent.resolve()


if __name__ == "__main__":

    readme = root / "README.md"
    pp = pprint.PrettyPrinter(indent=4)

    rewritten = "demo hub status === \n"

    # get list of projects from poc94
    urlbase = "https://poc94.blackduck.synopsys.com/"
    TOKEN = os.environ.get("HUB_94_TOKEN", "")
    hub = HubInstance(urlbase, api_token=TOKEN, insecure=True)
    num_versions_to_keep = 10

    project_list = hub.get_projects()
    for project in project_list['items']:
        rewritten += '* ' + project['name']
        rewritten += '\n'

        # find and delete older versions; keep 10 most recent ones
        project = hub.get_project_by_name(project['name'])

        if project:
            versions = hub.get_project_versions(project, limit=9999)
            sorted_versions = sorted(versions['items'], key=lambda i: i['createdAt'])
            logging.debug("Found and sorted {} versions for project {}".format(
                        len(sorted_versions), project['name']))
            if len(sorted_versions) > num_versions_to_keep:
                versions_to_delete = sorted_versions[:-num_versions_to_keep]

                version_names_being_deleted = [v['versionName'] for v in versions_to_delete]
                logging.debug("Deleting versions {}".format(version_names_being_deleted))

                for version_to_delete in versions_to_delete:
                    hub.delete_project_version_by_name(project['name'], version_to_delete['versionName'])
                    logging.info("Deleted version {}".format(version_to_delete['versionName']))
                else:
                    logging.debug("Found {} versions which is not greater than the number to keep {}".format(
                                len(sorted_versions), num_versions_to_keep))
        else:
            logging.debug("No project found with the name {}".format(project['name']))

    readme.open("w").write(rewritten)
