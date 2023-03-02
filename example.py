from config import settings
from NexusAPIWrapper import NexusAPI
import json

if __name__ == "__main__":
    api = NexusAPI()
    res = api.getHomeRessource()
    print(json.dumps(res, indent=4))
