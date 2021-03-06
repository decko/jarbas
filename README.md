# Jarbas — a tool for [Serenata de Amor](http://github.com/datasciencebr/serenata-de-amor)

[![Build Status](https://travis-ci.org/datasciencebr/jarbas.svg?branch=master)](https://travis-ci.org/datasciencebr/jarbas)
[![Code Climate](https://codeclimate.com/github/datasciencebr/jarbas/badges/gpa.svg)](https://codeclimate.com/github/datasciencebr/jarbas)
[![Coverage Status](https://coveralls.io/repos/github/datasciencebr/jarbas/badge.svg?branch=master)](https://coveralls.io/github/datasciencebr/jarbas?branch=master)
[![Updates](https://pyup.io/repos/github/datasciencebr/jarbas/shield.svg)](https://pyup.io/repos/github/datasciencebr/jarbas/)
[![donate](https://img.shields.io/badge/donate-apoia.se-EB4A3B.svg)](https://apoia.se/serenata)

[Jarbas](http://jarbas.serenatadeamor.org/) is part of [Serenata de Amor](http://github.com/datasciencebr/serenata-de-amor) — we fight corruption with data science.

Jarbas is in charge of making data from [CEAP](https://github.com/datasciencebr/serenata-de-amor/blob/master/CONTRIBUTING.md#more-about-the-quota-for-exercising-parliamentary-activity-ceap) more accessible. In the near future Jarbas will show what [Rosie](https://github.com/datasciencebr/rosie) thinks of each reimbursement made for our congresspeople.

## Table of Contents

1. [JSON API endpoints](#json-api-endpoints)
    1. [Reimbursement](#reimbursement)
    1. [Subquota](#subquota)
    1. [Applicant](#applicant)
    1. [Company](#company)
    1. [Tapioca Jarbas](#tapioca-jarbas)
1. [Installing](#installing)
    1. [Using Docker](#using-docker)
    1. [Local install](#local-install)
    1. [Settings](#settings)

## JSON API endpoints

### Reimbursement

Each `Reimbursement` object is a reimbursement claimed by a congressperson and identified publicly by its `document_id`.

#### Retrieving a specific reimbursement

##### `GET /api/reimbursement/<document_id>/`

Details from a specific reimbursement. If `receipt_url` wasn't fetched yet, the server **won't** try to fetch it automatically.

##### `GET /api/reimbursement/<document_id>/receipt/`

URL of the digitalized version of the receipt of this specific reimbursement.

If `receipt_url` wasn't fetched yet, the server **will** try to fetch it automatically.

If you append the parameter `force` (i.e. `GET /api/reimbursement/<document_id>/receipt/?force=1`) the server will re-fetch the receipt URL.

Not all receipts are available, so this URL can be `null`.

#### Listing reimbursements

##### `GET /api/reimbursement/`

Lists all reimbursements.

##### Filtering

All these endpoints accepts any combination of the following parameters:

* `applicant_id`
* `cnpj_cpf`
* `document_id`
* `issue_date_start` (inclusive)
* `issue_date_end` (exclusive)
* `month`
* `subquota_id`
* `suspicions` (_boolean_, `1` parses to `True`, `0` to `False`)
* `has_receipt` (_boolean_, `1` parses to `True`, `0` to `False`)
* `year`
* `order_by`: `issue_date` (default) or `probability` (both descending)
* `in_latest_dataset` (_boolean_, `1` parses to `True`, `0` to `False`)


For example:

```
GET /api/reimbursement/?year=2016&cnpj_cpf=11111111111111&subquota_id=42&order_by=probability
```

This request will list:

* all 2016 reimbursements
* made in the supplier with the CNPJ 11.111.111/1111-11
* made according to the subquota with the ID 42
* sorted by the highest probability

Also you can pass more than one value per field (e.g. `document_id=111111,222222`).

##### `GET /api/reimbursement/<document_id>/same_day/`

Lists all reimbursements of expenses from the same day as `document_id`.

### Subquota

Subqoutas are categories of expenses that can be reimbursed by congresspeople.

#### Listing subquotas

##### `GET /api/subquota/`

Lists all subquotas names and IDs.

##### Filtering

Accepts a case-insensitve `LIKE` filter in as the `q` URL parameter (e.g. `GET /api/subquota/?q=meal` list all applicant that have `meal` in their names.

### Applicant

An applicant is the person (congressperson or theleadership of aparty or government) who claimed the reimbursemement.

#### List applicants

##### `GET /api/applicant/`

Lists all names of applicants together with their IDs.

##### Filtering

Accepts a case-insensitve `LIKE` filter in as the `q` URL parameter (e.g. `GET /api/applicant/?q=lideranca` list all applicant that have `lideranca` in their names.

### Company

A company is a Brazilian company in which congressperson have made expenses and claimed for reimbursement.

#### Retrieving a specific company

##### `GET /api/company/<cnpj>/`

This endpoit gets the info we have for a specific company. The endpoint expects a `cnpj` (i.e. the CNPJ of a `Company` object, digits only). It returns `404` if the company is not found.

### Tapioca Jarbas

There is also a [tapioca-wrapper](https://github.com/vintasoftware/tapioca-wrapper) for the API. The [tapioca-jarbas](https://github.com/daneoshiga/tapioca-jarbas/) can be installed with `pip install tapioca-jarbas` and can be used to access the API in any Python script.

## Installing


### Using Docker

With [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/)) installed just run:

```console
$ make run.devel
```

or

```console
$ docker-compose up -d
$ docker-compose run --rm jarbas python manage.py migrate
$ docker-compose run --rm jarbas python manage.py ceapdatasets
$ docker-compose run --rm jarbas python manage.py tweets
$ docker-compose run --rm jarbas python manage.py collectstatic --no-input
```

You can access it at [`localhost:8000`](http://localhost:8000/). However your database starts empty, but you can use sample data to development using this command:

```console
$ make seed.sample
```

or

```console
$ docker-compose run --rm jarbas python manage.py reimbursements contrib/sample-data/reimbursements_sample.xz
$ docker-compose run --rm jarbas python manage.py companies contrib/sample-data/companies_sample.xz
$ docker-compose run --rm jarbas python manage.py suspicions contrib/sample-data/suspicions_sample.xz
```

You can get the datasets running [Rosie](https://github.com/datasciencebr/rosie) or directly with the [toolbox](https://github.com/datasciencebr/rosie).

To add a fresh new `reimbursements.xz` brewed by [Rosie](https://github.com/datasciencebr/rosie) or made with our [toolbox](https://github.com/datasciencebr/rosie), you just need to have this file **inside project folder** and give the path at the end of the command, as bellow:

```console
$ docker-compose run --rm jarbas python manage.py reimbursements path/to/my/fresh_new_reimbursements.xz
```

To change any of the default environment variables defined in the `docker-compose.yml` just export it in a local environment variable, so when you run Jarbas it will get them.

Finally if you would like to access the Django Admin for an alternative view of the reimbursements, you can access it at [`localhost:8000/admin/`](http://localhost:8000/admin/) creating an user with:

```console
$ docker-compose run --rm jarbas python manage.py createsuperuser
```

### Local install

#### Requirements

Jarbas requires [Python 3.5](http://python.org), [Node.js 6+](https://nodejs.org/en/), [Yarn](https://yarnpkg.com), and [PostgreSQL 9.4+](https://www.postgresql.org). Once you have `pip` and `yarn` available install the dependencies:

```console
$ yarn install
$ python -m pip install -r requirements-dev.txt
```

##### Python's `lzma` module

In some Linux distros `lzma` is not installed by default. You can check whether you have it or not with `$ python -m lzma`. In Debian based systems you can fix that with `$ apt-get install liblzma-dev` or in macOS with `$ brew install xz` — but you might have to re-compile your Python.

#### Setup your environment variables

Basically this means copying `contrib/.env.sample` as `.env` in the project's root folder — but there is [an entire section on that](#settings).

#### Migrations

Once you're done with requirements, dependencies and settings, create the basic database structure:

```console
$ python manage.py migrate
```

#### Load data

Now you can load the data from our datasets and get some other data as static files:

```
$ python manage.py reimbursements <path to reimbursements.xz>
$ python manage.py suspicions <path to suspicions.xz file>
$ python manage.py companies <path to companies.xz>
$ python manage.py tweets
$ python manage.py ceapdatasets
```

You can get the datasets running [Rosie](https://github.com/datasciencebr/rosie) or directly with the [toolbox](https://github.com/datasciencebr/serenata-toolbox).

#### Generate static files

We generate assets through NodeJS, so run it before Django collecting static files:

```console
$ yarn assets
$ python manage.py collectstatic

```

#### Ready?

Not sure? Test it!

```
$ python manage.py check
$ python manage.py test
$ yarn test
```

#### Ready!

Run the server with `$ python manage.py runserver` and load [localhost:8000](http://localhost:8000) in your favorite browser.

#### Using Django Admin


If you would like to access the Django Admin for an alternative view of the reimbursements, you can access it at [`localhost:8000/admin/`](http://localhost:8000/admin/) creating an user with:

```console
$ python manage.py createsuperuser
```


### Settings

If **you are not** using Docker copy `contrib/.env.sample` as `.env` in the project's root folder and adjust your settings. These are the main variables:

##### Django settings

* `DEBUG` (_bool_) enable or disable [Django debug mode](https://docs.djangoproject.com/en/1.10/ref/settings/#debug)
* `SECRET_KEY` (_str_) [Django's secret key](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SECRET_KEY)
* `ALLOWED_HOSTS` (_str_) [Django's allowed hosts](https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts)
* `USE_X_FORWARDED_HOST` (_bool_) [Whether to use the `X-Forwarded-Host` header](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-USE_X_FORWARDED_HOST)
* `CACHE_BACKEND` (_str_) [Cache backend](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-CACHES-BACKEND) (e.g. `django.core.cache.backends.memcached.MemcachedCache`)
* `CACHE_LOCATION` (_str_) [Cache location](https://docs.djangoproject.com/en/1.10/ref/settings/#location) (e.g. `localhost:11211`)
* `SECURE_PROXY_SSL_HEADER` _(str)_ [Django secure proxy SSL header](https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header) (e.g. `HTTP_X_FORWARDED_PROTO,https` transforms in tuple `('HTTP_X_FORWARDED_PROTO', 'https')`)

##### Database

* `DATABASE_URL` (_string_) [Database URL](https://github.com/kennethreitz/dj-database-url#url-schema), must be [PostgreSQL](https://www.postgresql.org) since Jarbas uses [JSONField](https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#jsonfield).

##### Amazon S3 settings

* `AMAZON_S3_BUCKET` (_str_) Name of the Amazon S3 bucket to look for datasets (e.g. `serenata-de-amor-data`)
* `AMAZON_S3_REGION` (_str_) Region of the Amazon S3 (e.g. `s3-sa-east-1`)
* `AMAZON_S3_CEAPTRANSLATION_DATE` (_str_) File name prefix for dataset guide (e.g. `2016-08-08` for `2016-08-08-ceap-datasets.md`)

##### Google settings

* `GOOGLE_ANALYTICS` (_str_) Google Analytics tracking code (e.g. `UA-123456-7`)
* `GOOGLE_STREET_VIEW_API_KEY` (_str_) Google Street View Image API key

##### Twitter settings

* `TWITTER_CONSUMER_KEY` (_str_) Twitter API key
* `TWITTER_CONSUMER_SECRET` (_str_) Twitter API secret
* `TWITTER_ACCESS_TOKEN` (_str_) Twitter access token
* `TWITTER_ACCESS_SECRET` (_str_) Twitter access token secret

To get this credentials follow [`python-twitter`
instructions](https://python-twitter.readthedocs.io/en/latest/getting_started.html#getting-your-application-tokens).
