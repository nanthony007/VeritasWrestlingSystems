# VeritasWrestling-Website
## Contents
- [Purpose](#Purpose)
- [Usage](#Usage)
- [Features](#Features)
  * [In Development](#In-Development)
  * [Released](#Released)
- [Abandoned Features](#Abandoned-Features)
- [Skills Learned](#Skills)

## Purpose
This website was developed to display advanced analytics for the sport of wrestling. 
The website serves the first open source database for statistics in the sport and the only location for analytics.  
Fantasy sport components will be implemented to increase marketability.

## Usage
Clone the repository: `$git clone https://github.com/nanthony007/VeritasAnalytics-Website.git`  
It is recommended to activate a virtual environment using 
[virtualenv](https://virtualenv.pypa.io/en/latest/) `$virtualenv venv`  
  
Activate venv `$source venv/bin/activate`.

Install requirements with `$pip3 install -r requirements.txt`  

Utilize the [Abbreviations file](collection/VWSabbreviations.xlsx)
to familiarize yourself with Veritas data abbreviations.
United World Wrestling (UWW) rules and language 
can be found [here(rules)](collection/uww_wrestling_rules.pdf) and [here(language)](collection/uww_basic_vocabulary.pdf).
  
Run `$python3 FScollector.py` to start collecting data. 

This will write to the site database as you collect data.  

Use `save_script.py` to save the current database instance to local files in [stats](collection/stats).

## Features
#### In-Development
- [ ] Fantasy user app (building on coaches portal)
- [ ] Fantasy draft
- [ ] Network graph for predicted match sequence
- [ ] Predict type of result and score

#### Released
- [x] Interactive page to compare wrestlers AND predict winner
- [x] Coaches portal to analyze wrestlers strengths/weaknesses
- [x] Coaches profile page with embedded tableau
- [x] User registration and login
- [x] Sortable tables
- [x] Events Result field
- [x] Wrestlers Reports

## Abandoned-Features
1. Blog/articles app that utilizes .ipynb files

## Skills
1.  Django web framework including ORM
2.  SQL and PostgreSQL connections with django models
3.  HTML forms
    -adding records to a live database from an outside script
    -html tabling and styling
4. Google Charts API
5. Bokeh interactive visualizations
6. Chart.js visualizations
7. mdboostrap styling
8. User account management
9. Tableau embedding
10. Logistic Regression modeling
11. Feature Engineering