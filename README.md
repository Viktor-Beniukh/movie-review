# Movie Review Project 

Django project describing detail movie information data with information about directors and actors.


### Installing using GitHub

- Python3 must be already installed
- Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/movie-review.git
cd movie-review
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   
```
You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;



## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`



## Features
- Powerful admin panel for advanced managing;
- Managing movies, directors, actors and users directly from website;
- Creating movies, directors, actors, categories and genres of movies (only admin);
- Updating actors & directors data (only admin);
- Searching of movies by title and categories;
- Filtering of movies by genres and years of release;
- There is an opportunity to add a clip from YouTube (only admin);
- There is an opportunity to leave reviews for movies (for authenticated users);
- There is an opportunity to leave comments for reviews (for authenticated users);
- There is an opportunity to subscribe and unsubscribe from newsletters (for authenticated users);
- It is possible to evaluate films by rating (for authenticated users);
- Registration and authorisation of users, creating and updating user profiles;
- Changing and reset user password.
    
  
### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that 2 services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;



## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`;
- If needed, also check the flake8: `docker-compose run app sh -c "flake8"`.



## Check project functionality

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.
