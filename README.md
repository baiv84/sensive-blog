# Yuri Grigorievich success stories blog

Yuri, self-made man, share personal success stories on his personal blog pages.
![Скриншот](screenshots/site.png)

## Prepare virtual environment

First, install package `python3-venv` to work with python virtual environment.

Update packages on your system `!(it depends on your operating system)`
in this document I use Ubuntu as my operating system. 

So I run update command:

```console
$ sudo apt update
```

and run command:

```console
$ sudo apt install -y python3-venv
```

Then jump to project folder:

```console
$ cd sensive-blog
```

and create new python environment to run the code:
```console
$ python3 -m venv venv
```

Activate new virtual environment:

```console
$ source venv/bin/activate
```

As a result, you will see command line prompt like this:

```console
(venv) sensive-blog $
```

Next step, install all necessary dependencies

```console
(venv) sensive-blog $  pip3 install -r requirements.txt
```

## Prepare database file

Download database file `db.sqlite3` and put it to the project folder, next to `manage.py` file.

Download `media` folder and put it to the project folder, next to `manage.py` file as well.

## Run data migrations 

To run data migrations, execute command:

```console
  (venv) sensive-blog $ python3 manage.py migrate
```

## Create superuser account

To create superuser account, run command:

```console
  (venv) sensive-blog $ python3 manage.py createsuperuser
```

This process accompanied with questions, you have just answer to create superuser.


## Run Yuri Grigorievich success blog

To start Yuri success blog site, execute command:

```console
  (venv) sensive-blog $ python3 manage.py runserver
```

Afterwards, in web browser open link: `http://127.0.0.1:8000/`

The main blog page will start shortly.

If you want to run administrative page, in web browser open link: `http://127.0.0.1:8000/admin/`

Enter `username` and `password` of superuser you have created in the previous step.

As a result, you will see the administration web form, where you can manipulate with all program entities, such as `Users`, `Groups`, `Posts`, `Tags` and `Comments`.


# Projects goals

This site was written as a study project for Python web development course [Devman](https://dvmn.org)