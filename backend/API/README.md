# Drive API Client

`drive_client` is a Python client generated from Drive’s OpenAPI specification (`swagger.json`) using OpenAPI Generator.

It provides Python methods and data models to call the real Drive API, plus documentation for the operations included in the specification.

Our agents can use this client from the orchestration backend. It does not require FastAPI or start another server: Drive must already be running.

## Generate the client

Run these commands from the `backend` directory.

Download the specification:

```bash
curl -fS \
  'http://localhost:8071/api/v1.0/swagger.json' \
  -o swagger.json
```

Once the download succeeds, generate the Python client:

```bash
sudo docker run --rm \
  --user "$(id -u):$(id -g)" \
  -v "$PWD:/local" \
  openapitools/openapi-generator-cli generate \
  -i /local/swagger.json \
  -g python \
  -o /local/API/drive_client
```

## Install

Create and activate a virtual environment, then install the local package:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ./API/drive_client
```

Add `.venv/` to `.gitignore`. Reactivate the environment in each new terminal with `source .venv/bin/activate`.

## Usage and authentication

Import the client into your Python code, configure the Drive server address, and call the generated methods. Examples and method names are available in `API/drive_client/README.md`.

Authentication depends on the endpoint:

* Public configuration: no authentication required.
* Files and folders: an authenticated user session or an OIDC access token accepted by Drive.
* Storage metrics: a separate API key, which does not grant access to files.

Keep credentials outside the generated code and Git repository.

## Current limitations

Metrics were excluded from our Swagger specification to work around a schema-generation error, so their endpoint is absent from this client.

The generated `NullEnum` contained invalid syntax (`class NullEnum(, Enum):`), temporarily corrected to `class NullEnum(Enum):`. Regeneration may overwrite this fix; nullable model behavior still needs validation.
