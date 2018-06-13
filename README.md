# django_app

Aplicativo Django, com bootstrap, para base de outros apps.

## Começando

Essas instruções farão com que você tenha uma cópia do projeto em execução na sua máquina local para fins de desenvolvimento e teste.

## Pré-requisitos

O que você precisa para instalar o software e instalá-lo

  * [Python v2.7](https://www.python.org)
  * [Django v1.8](https://www.djangoproject.com)
  * [PostgreSQL v9.5](https://www.postgresql.org)

## Utilização

Faça o clone da aplicação (no local desejado):

```
$ git clone https://github.com/diegotainha/django_app.git
```

Entre como usuario postgres e crie o banco de dados (utilizando Linux):

```
$ sudo su - postgres
$ postgres:~$ psql
psql (9.5.13)
Type "help" for help.

postgres=# createdb -U meu_usuario meu_banco;
```
Edite a variavel DATABASES no settings.py do seu projeto, informando as credenciais do seu banco de dados:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'meu_banco',
        'USER': 'meu_usuario',
        'PASSWORD': 'meu_password',
        'HOST': '127.0.0.1', # localhost
        'PORT': '', # 8000 is default
    }
}
```

Faça os migrates do Django e rode a aplicação (na pasta do projeto):

```
$ python manage.py migrate
$ python manage.py runserver 8000
```
No seu navegador acesse: [localhost:8000](http://localhost:8000)

Você também pode criar um usuário para utilizar a página admin do Django:
```
$ python manage.py createsuperuser
```

Seja feliz!

   
## Linguagem de programação

   * [Python v2.7](https://www.python.org)

## Framework

   * [Django v1.8](https://www.djangoproject.com)

## Banco de Dados

   * [PostgreSQL v9.5](https://www.postgresql.org)
   
## Autor

  * **Diego Dias Tainha**

