# pythonBluecode

#   build image
docker build -t docker-bluecode .

# container 
docker run -d -p 5000:80  -v D:/pythonWs/bluecode-operator/pythonBluecode:/app/ docker-bluecode



# ref https://stackoverflow.com/questions/51121875/how-to-run-docker-with-python-and-java
# bill
