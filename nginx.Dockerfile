# Use official nginx image
FROM nginx:latest

# Copy generated index.html to nginx web root
COPY index.html /usr/share/nginx/html/index.html