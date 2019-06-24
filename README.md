# VeritasWrestling-Website
## Contents
- [Purpose](#Purpose)
- [Usage](#Usage)
- [Features](#Features)
  * [In Development](#In Development)
  * [Released](#Released)
- [Abandoned Features](#Abandoned Features)
- [Learning](#What I learned)

## Purpose
This website was developed to display advanced analytics for the sport of wrestling. 
The website serves the first open source database for statistics in the sport and the only location for analytics.  
Fantasy sport components will be implemented to increase marketability.

## Usage
Clone the repository: `git clone https://github.com/nanthony007/VeritasAnalytics-Website.git`  
It is recommended to activate a virtual environment using 
[virtualenv](https://virtualenv.pypa.io/en/latest/) `virtualenv venv`  
  
Utilize the [Abbreviations file](collection/VWSabbreviations.xlsx) 
to familiarize yourself with Veritas data abbreviations.
United World Wrestling (UWW) rules and language 
can be found [here(rules)](collection/uww_wrestling_rules.pdf) and [here(language)](collection/uww_basic_vocabulary.pdf).
  
Run `$python3 FScollector.py`  
This will write to the site database and the local files in the [stats](collection/stats) directory.  
  
Analysis can be found in the series of Jupyter Notebooks located in the [analysis](collection/analysis) directory.

## Features
#### In Development
- [ ] Fantasy user app (building on coaches portal)
- [ ] Live fantasy draft
- [ ] Coaches portal to analyze wrestlers strengths/weaknesses
- [ ] Interactive page to compare wrestlers AND predict winner
#### Released
- [x] Sortable tables
- [x] Events Result field
- [x] Wrestlers Reports

## Abandoned Features
1. Blog/articles app that utilizes .ipynb files as field

## What I learned
1.  Django web framework including ORM
2.  SQL and PostgreSQL connections with django models
3.  HTML forms
    -adding records to a live database from an outside script
    -html tabling and styling
4. Google Charts API
5. Bokeh interactive visualizations
6. User account management
