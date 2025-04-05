import json
import subprocess

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Access the name property and list of servers
app_name = config['name']
servers = config['servers']

# open a file to write the docker-compose file
with open('docker-compose.yml', 'w') as f:
    f.write(f"""
      services:""")
    # Loop over all servers
    for server in servers:
        name = server['name']
        route = server['route']
        command = server['command']
        args = server['args']

        print(f"Generating compose entry for server: {server['name']}")
        args_str= "\", \"".join(args)
        print(f"args_str: {args_str}")
        image_line = "mcporbit/node_runner" if command == "npx" else "ghcr.io/astral-sh/uv:python3.12-bookworm-slim"
        f.write(f"""
        {route}:
          image: {image_line}
          command: ["uvx", "mcpo", " --port 8000", "--", "{command}", "{args_str}"]
        """)
        # Generate Dockerfile
        # Use a Python image with uv pre-installed
        # ghcr.io/astral-sh/uv:python3.12-bookworm-slim