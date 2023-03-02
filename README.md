# Python wrapper for KMD Nexus API
En enkel wrapper-class for Nexus APIet. Klassen håndterer automatisk status på auth- og refresh-token og sørger for at forny disse, ved behov. Klassen kan pr. i dag kun benyttes med `client_credentials` som `grant_type` ved autorisering mod Nexus.

En instans af klassen genereres med `api = NexusAPI()`. Dette kalder `/auth_v2/realms/INSTANCE/protocol/openid-connect/token` i Nexus-APIet, og håndtering af responsen med auth- og refresh-token, sker automatisk.


## Konfiguration
I dette repository er [Poetry](https://python-poetry.org/) brugt til pakke-håndtering og [Dynaconf](https://www.dynaconf.com/) er brugt til håndtering af konfigurations-indstillinger. Der benyttes to konfigurationsfiler; `settings.toml` og `secrets.toml`. Førstnævnte indeholder ikke-sensitive indstillinger, mens sidstnævnte indeholder credentials til Nexus-APIet. 

## Direkte adgang til auth-tokens
Ved behov kan både access- og refresh-token hentes fra klasse-instansen med henholdsvis `api.access_token` og `api.refresh_token`.

## Tilgængelige klasse-funktioner
Alle klasse-funktioner returnerer JSON. Følgende funktioner er implementeret:

`getHomeRessource()`

`getOrganizationsTree()`

`findProfessionals(search_string)`

`getProfessional(user_id)`

`getProfessionalPrototype()`

`getProfessionalPermissionAssignments(user_id)`

`getProfessionalPermissionsTree(user_id)`

`getProfessionalRoles(user_id)`

`createProfessional(user_prototype)`

`getProfessionalConfiguration(user_id)`

## Eksempler
Det efterfølgende viser et par eksempler på hvordan klassen kan benyttes.

#### Hente HomeRessource
```
from config import settings
import json
from NexusAPIWrapper import NexusAPI

api = NexusAPI()
res = api.getHomeRessource()
print(json.dumps(res, indent=4))
```

#### Søge efter Nexus-bruger
```
from config import settings
import json
from NexusAPIWrapper import NexusAPI

api = NexusAPI()
search_term = "Bente"
res = api.findProfessionals(search_term)
print(json.dumps(res, indent=4))
```

#### Oprette ny bruger i Nexus
```
from config import settings
import json
from NexusAPIWrapper import NexusAPI

api = NexusAPI()

# For at undgå at skulle lave hele brugerobjektet manuelt,
# hentes det som en dictionary, via:
prototype = api.getProfessionalPrototype()

# Herefter kan vi ændre de felter i brugerobjektet som 
# vi ønsker:
prototype["firstName"] = "Test"
prototype["lastName"] = "Bruger"
prototype["initials"] = "TBB"
prototype["primaryIdentifier"] = "TESTBRUGERTBB"
prototype["user"]["username"] = "testbruger"
prototype["user"]["password"] = "SecretPassword1234"

# Til sidst kalder vi endpoint for oprettelse af brugeren,
# med bruger-objektet som parameter:
res = api.createProfessional(prototype)
print(json.dumps(res, indent=4))
```