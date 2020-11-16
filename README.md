# Welcome to Microblog!

This is an example application featured in my [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). See the tutorial for instructions on how to work with it.

#docker command
#Create MySQL Container
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=smallapp -e MYSQL_USER=smallapp \
    -e MYSQL_PASSWORD=ly119811 \
    mysql/mysql-server:8.0
#confilct at this line

