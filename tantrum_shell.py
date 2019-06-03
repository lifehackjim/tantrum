#!python -i

import urllib3
import tantrum
import tantrum_creds

# disable requests warnings about SSL cert issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# add a log that goes to STDERR for debug level and above
tantrum.utils.logs.add_stderr(lvl="debug")

# setup an HTTP client for communicating with the server
http_client = tantrum.http_client.HttpClient(
    url=tantrum_creds.url, verify=False, lvl="debug"
)

# setup an authentication method that uses an http client to send auth requests
auth_method = tantrum.auth_methods.Credentials(
    http_client=http_client,
    username=tantrum_creds.username,
    password=tantrum_creds.password,
    lvl="debug",
)

# setup an API client that uses an http client to send API requests
api_client = tantrum.api_clients.Soap(
    http_client=http_client, auth_method=auth_method, lvl="debug"
)

# setup an API objects layer
api_objects = tantrum.api_objects.load()

# setup an adapter that uses an API client and API objects to send commands to the API
adapter = tantrum.adapters.Soap(
    api_client=api_client, api_objects=api_objects, lvl="info"
)

# Now you can use an adapter directly, or use a workflow that uses an adapter.
