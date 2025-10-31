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

    # write the nginx entry
    f.write(f"""
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
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
