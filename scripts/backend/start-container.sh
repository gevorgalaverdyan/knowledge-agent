docker build -t knowledge-app-be .
docker run -d -p 8000:80 --name backend-container knowledge-app-be
# docker logs backend-container