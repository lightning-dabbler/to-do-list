To-Do List Wep App
============
> A to-do list web app

> Built with a Containerized Flask and MySQL stack

Installation
--------
* Docker 18.06.0+ Must Be Installed on Host before running this Web App 

- Run ```docker-compose up``` to run the app 

**If the images associated with the docker-compose and Dockerfile files are not available on your host computer, 
docker will pull these images and it will take some time to have them fully pulled to your host computer.**
**After that any** ```docker-compose up``` **commands will run the containers right away.**

- Run ```docker-compose down``` to stop and remove the containers and the network.

**The images, however, will still stay on your computer unless you want to remove them.** 

The app is ```app.py```

The app will be running on http://localhost:5001/

Sample Images
---------
<img src="./screenshots/mobile_compatible_historical_data.png" alt="Historical Page displaying Mobile Compatibility" height="905" width="404"> <img src="./screenshots/mobile_compatible_current_data.png" alt="Landing Page displaying Mobile Compatibility" height="665" width="404">


Tech 
------
* [flask]
* [pytz] 
* [Jinja2]
* [mysql-connector-python]
* [MySQL]
* [Docker]
* [Docker-Compose]
* [Bootstrap]

Version
--------
* 1.1.8

Author
--------
* Osarodion Irabor


[flask]: http://flask.pocoo.org/
[Docker]: https://docs.docker.com/engine/reference/builder/#usage
[Docker-Compose]: https://docs.docker.com/compose/compose-file/
[Jinja2]: http://jinja.pocoo.org/docs/2.10/
[pytz]: https://pypi.org/project/pytz/
[MySQL]: https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-12.html
[mysql-connector-python]: https://dev.mysql.com/doc/connector-python/en/
[Bootstrap]: https://getbootstrap.com/docs/4.0/getting-started/introduction/
