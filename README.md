# EveryElection
[![Build Status](https://travis-ci.org/DemocracyClub/EveryElection.svg?branch=master)](https://travis-ci.org/DemocracyClub/EveryElection) [![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/EveryElection/badge.svg?branch=master)](https://coveralls.io/github/DemocracyClub/EveryElection?branch=master)

For recording every election in the UK

## Domain Model

### Elections

The elections table stores a list of election objects, each with a semantic ID.

Election IDs sometimes have a parent, and are sometimes a "group ID".

There are two types of group ID:

1. `[type].[date]`, for example `local.2017-05-04` will be the group for all local elections happening on 2017-05-04.
2. `[type].[organiation].[date]`, for example `local.norfolk.2017-05-04` is the Norfolk County Council elections.

Finally an ID is made _per ballot paper_ using `[type].[organiation].[organisation division].[date]` for example `local.norfolk.diss.2017-05-04`.

[See the reference for more information](https://democracyclub.org.uk/projects/election-ids/reference/).

![Graph](docs/graph.png)

## Setting up a dev copy

* Clone the repo
* `pip install -r requirements/testing.txt`
* `sudo -u postgres createdb every_election`
* `sudo -u postgres createuser dc -P -s`
* `sudo -u postgres psql every_election`
* `CREATE EXTENSION postgis;`
* `cp every_election/settings/local.example.py every_election/settings/local.py`
* Populate `local.py` with your DB password
* `python manage.py migrate`
* `python manage.py import_organisations`
* TODO: importing organisation_divisions and geometries!
