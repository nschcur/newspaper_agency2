# Newspaper agency (NA) project

Django project for managing newspapers and authors in Agency

## Check it out!

[Newspaper agency project deployed to render](https://newspaper-agency-j00j.onrender.com/) 

# newspaper-agency2

Python3 must be already installed

```shell
git clone https://github.com/nschcur/newspaper_agency2.git
cd newspaper-agency2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```



```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.

![](demo.png)



- After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admintest`
  - Password: `qwerty12345`
- 
