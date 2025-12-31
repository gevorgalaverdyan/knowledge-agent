docker build -t knowledge-app-fe .
docker run -d -p 8080:8080 --name angular-container knowledge-app-fe
# docker logs angular-container