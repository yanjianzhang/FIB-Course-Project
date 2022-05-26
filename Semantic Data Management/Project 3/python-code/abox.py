import random

import pandas as pd
from tbox_new import *
from tqdm import tqdm
import random
random.seed(2022)

name2area = {}
name2author = {}
name2reviewer = {}
name2conf = {}
name2jour = {}
name2edition = {}
name2volume = {}
name2chair = {}
name2editor = {}
conference_type = ['workshop', 'symposium', 'expert group', 'regular conference']



def get_areas(area_names):
    areas = []
    for name in area_names:
        if name in name2area:
            area = name2area[name]
        else:
            area = Area(uri=name)
            area.fullname = name
            name2area[name] = area
        areas.append(area)
    return areas

def get_chairs(chair_names):
    chairs = []
    for name in chair_names:
        if name in name2chair:
            chair = name2chair[name]
        else:
            chair = Chair(uri=name)
            chair.fullname = name
            name2chair[name] = chair
        chairs.append(chair)
    return chairs


def get_editors(editor_names):
    editors = []
    for name in editor_names:
        if name in name2editor:
            editor = name2editor[name]
        else:
            editor = Editor(uri=name)
            editor.fullname = name
            name2editor[name] = editor
        editors.append(editor)
    return editors

def get_authors(author_names):
    authors = []
    for name in author_names:
        if name in name2author:
            author = name2author[name]
        else:
            author = Author(uri=name)
            author.fullname = name
            name2author[name] = author
        authors.append(author)
    return authors

def get_reviewer(review_names):
    reviewers = []
    for name in review_names:
        if name in name2reviewer:
            reviewer = name2reviewer[name]
        else:
            reviewer = Reviewer(uri=name)
            reviewer.fullname = name
            name2reviewer[name] = reviewer
        reviewers.append(reviewer)
    return reviewers

def get_conference(name):
    if name in name2conf:
        conf = name2conf[name]
    else:
        conf = Conference(uri=name)
        conf.fullname = name
        name2conf[name] = conf
    return conf

def get_journal(name):
    if name in name2jour:
        jour = name2jour[name]
    else:
        jour = Journal(uri=name)
        jour.fullname = name
        name2jour[name] = jour
    return jour

def get_edition(name):
    if name in name2edition:
        edition = name2edition[name]
    else:
        edition = EditionProceedings(uri=name)
        edition.fullname = name
        edition.periodicaltype = 'edition'
        name2edition[name] = edition
    return edition

def get_volume(name):
    if name in name2volume:
        volume = name2volume[name]
    else:
        volume = Volume(uri=name)
        volume.fullname = name
        volume.periodicaltype = 'volume'
        name2volume[name] = volume
    return volume

# read conf
conf_df = pd.read_csv("../data/Updated_CSVs/updates_conferences_general.csv")
print(conf_df.info)
for index, row in tqdm(conf_df.iterrows()):
    edition = get_edition(row['edition_code'])
    conf = get_conference(row['booktitle'])
    conf.has_edition.append(edition)
    area_names = list(row['areas'].split('|'))
    areas = get_areas(area_names)
    conf.has_area = areas
    chair_names = list(row['Chair'].split('|'))
    chairs = get_chairs(chair_names)
    for chair in chairs:
        chair.chairOf.append(conf)
    conf.conf_type = random.choice(conference_type)

# read paper-conf
paper_conf_df = pd.read_csv("../data/Updated_CSVs/updated_conf_papers.csv")
print(paper_conf_df.info())
accept_paper_num = 0
unaccept_paper_num = 0
for index, row in tqdm(paper_conf_df.iterrows()):
    # 1% unaccepted
    accepted_seed = random.random()
    if accepted_seed > 0.01:
        paper = Accepted_Paper(uri = row['key'])
        paper.accepted = True
        accept_paper_num += 1
    else:

        paper = Unaccepted_Paper(uri = row['key'])
        paper.accepted = False
        unaccept_paper_num += 1
    paper.title = row['title']
    paper.paper_type = row['paper_types']
    author_names = list(row['authors'].split('|'))
    reviewer_names = list(row['reviwers'].split('|'))

    authors = get_authors(author_names)
    for author in authors:
        author.writes.append(paper)

    reviewers = get_reviewer(reviewer_names)
    for reviewer in reviewers:
        print(row['key'], reviewer.fullname)
        review = Review(uri=row['key']+reviewer.fullname)
        reviewer.reviews.append(review)
        paper.has_review.append(review)

    area_names = list(row['areas'].split('|'))
    areas = get_areas(area_names)
    paper.has_area = areas
    periodical = get_edition(row['edition_code'])
    periodical.published.append(paper)

# read journal
jour_df = pd.read_csv('../data/Updated_CSVs/updates_journals_general.csv')
print(jour_df.info())
for index, row in tqdm(jour_df.iterrows()):
    volume = get_volume(row['journal_code'])
    jour = get_journal(row['journal'])
    jour.has_volume.append(volume)
    area_names = list(row['areas'].split('|'))
    areas = get_areas(area_names)
    jour.has_area = areas
    editor_names = list(row['editors'].split('|'))
    editors = get_editors(editor_names)
    for editor in editors:
        editor.editorOf.append(jour)

# read paper-journal
paper_jour_df = pd.read_csv('../data/Updated_CSVs/updated_journal_papers.csv')
print(paper_jour_df.info())
for index, row in tqdm(paper_jour_df.iterrows()):
    # journal's paper type could not be poster
    if row['paper_types'] == 'poster':
        continue

    # 1% unaccepted
    accepted_seed = random.random()
    if accepted_seed > 0.01:
        paper = Accepted_Paper(uri=row['key'])
        paper.accepted = True
        accept_paper_num += 1
    else:

        paper = Unaccepted_Paper(uri=row['key'])
        paper.accepted = False
        unaccept_paper_num += 1
    paper.title = row['title']
    paper.paper_type = row['paper_types']
    author_names = list(row['authors'].split('|'))
    reviewer_names = list(row['reviwers'].split('|'))

    authors = get_authors(author_names)
    for author in authors:
        author.writes.append(paper)

    reviewers = get_reviewer(reviewer_names)
    for reviewer in reviewers:
        print(row['key'], reviewer.fullname)
        review = Review(uri=row['key'] + reviewer.fullname)
        reviewer.makes.append(review)
        paper.has_review.append(review)

    area_names = list(row['areas'].split('|'))
    areas = get_areas(area_names)
    paper.has_area = areas
    periodical = get_volume(row['journal_code'])
    periodical.published.append(paper)



if __name__ == "__main__":
    onto.save("../data/tbox_abox.rdf")
    print("accepted paper", accept_paper_num, "unaccepted paper", unaccept_paper_num)