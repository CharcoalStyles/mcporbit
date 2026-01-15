#mcp(o)rbit

Expose a collection of MCP servers as OpenAPI-compatible HTTP routes form one endpoint.

Built using

- [mcpo](https://github.com/open-webui/mcpo)
- docker
- nginx

## Requirements
- Docker
- Docker Compose
- Python 3.8+

## Setup
Build the node runner image
```bash
./build.sh
```
or
```cmd
build.bat
```

## Configuration

Copy the `config.sample.json` file, then edit it to your needs.

The root of the config file has two keys:
- `name`: The name of the server. This is currently used in the nginx index page.
- `port`: The port to expose the nginx server on, default is `80`
- `servers`: A list of servers to expose.

Each server has the following keys:
- `name`: The name of the server. This is currently only used in logging
- `route`: The route of the server. This is currently only used to generate the container name.
- `command`: The base command to run the server. Currently supporting `uvx` and `npx` to run publicly accessible self hosted MCP servers. Currently testing the ability to use SSE and streaming HTTP responses, with the `sse` and `streamable-http` options.
- `args`: The arguments to pass to the command.
- `mountPoint` (optional): The mount point inside the container to mount a volume. If specified, a volume will be created at `./data/{route}` on the host and mounted to the specified mount point inside the container.
- `env` (optional): A dictionary of environment variables to set inside the container.

## Build

Build the dockercompose file using the `generateDocker.py` script.
```
python3 generateDocker.py
```
or
```
python generateDocker.py
```
This will generate a `docker-compose.yml` file in the current directory.

## Run

Run the docker-compose file using the `docker-compose` command.
```
docker-compose up -d
```

# Usage

## Accessing the servers

With this commit, the nginx server is not added to the docker-compose file, so the servers are not accessible from the outside. This is just because this commit is a WIP to transfer to a different computer 🤣