###SETUP: 
```
python manage.py migrate
python manage.py createsuperuser --email <EMAIL> --username <USERNAME>
python manage.py runserver
```

Authorization is done by using TOKENS. 
I personally prefer using POSTMAN but this curl also work

```
$ curl -H "Authorization: Token <_your_token_>" http://localhost:8000/bonds/
```
to get token for user:
```
$ http post http://127.0.0.1:8000/api-token-auth/ username=admin password=
```
or
```
$ python manage.py drf_create_token <USERNAME>
```
