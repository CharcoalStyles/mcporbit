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
        image_line = "mcporbit/node-runner:latest"
        f.write(f"""
  {route}:
    image: {image_line}
    command: ["uvx", "mcpo", " --port 8000", "--", "{command}", "{args_str}"]
""")
        # check for mountPoint
        if 'mountPoint' in server:
            mount_point = server['mountPoint']
            f.write(f"""    volumes:
      - ./data/{route}:{mount_point}
""")

    # write the nginx entry
    f.write(f"""
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./index.html:/etc/nginx/html/index.html
""" )
    #write the dependency entry
    f.write(f"""
    depends_on:
        """)
    for server in servers:
        route = server['route']
        f.write(f"""
      - {route}
""")

# write the nginx config file
with open('nginx.conf', 'w') as f:
    f.write(f"""
worker_processes 1;
events {{
  worker_connections 1024;
}}
http {{
  server {{
    listen 80;""")
    for server in servers:
        route = server['route']
        f.write(f"""
    location /{route} {{
      proxy_pass http://{route}:8000;

      rewrite ^/{route}/(.*)$ /$1 break;

      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;

      # Required for sub_filter to work
      proxy_set_header Accept-Encoding "";

      # Rewrite the Swagger UI config
      sub_filter_once off;
      sub_filter 'url: \\'/openapi.json\\'' 'url: \\'/{route}/openapi.json\\'';
      sub_filter 'url: "/openapi.json"' 'url: "/{route}/openapi.json"';
    }}
""")
    f.write(f"""
  }}
}}""")

# Generate index.html for nginx main route
with open('index.html', 'w') as f:
    f.write("""<!DOCTYPE html>
<html>
  <head>
    <title>Installed Servers Directory</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2em; }
      h1 { color: #333; }
      a { color: #007acc; text-decoration: none; padding-bottom: 0.2em; display: block; }
      a:hover { text-decoration: underline; }
      .server-list { margin-top: 1em; display: flex; flex-direction: row; gap: 1em; flex-wrap: wrap; }
      .server-entry { border: 1px solid #ddd; border-radius: 4px; padding: 0.5em; width: 300px; }
      .server-entry h2 { margin-top: -0.25em; color: #848; }
    </style>
  </head>
  <body>
    <h1>Installed Servers Directory</h1>
""")
    f.write(f'    <div class="server-list">\n')
    for server in servers:
        name = server['name']
        route = server['route']
        f.write(f'      <div class="server-entry">\n')
        f.write(f'        <h2>{name}</h2>\n')
        f.write(f'        <a href="/{route}">MCP link</a>\n')
        f.write(f'        <a href="/{route}/docs">OpenAPI Docs</a>\n')
        f.write(f'      </div>\n')
    f.write(f'    </div>\n')
    f.write("""
  </body>
</html>
""")
