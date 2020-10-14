# -*- coding: utf-8 -*-
# Au cas où la personne arrive sur la page index, on redirige vers la liste des divisions
def index(): redirect(URL('liste'))

def liste():
    # On récupère toutes les divisions dont l'id n'est pas null
    divisions = db(db.divisions.id!=None).select()
    return dict(aff_div=divisions)

def detail():
    # On récupère l'id de la division passé en paramètre
    id_div = request.args(0, cast=int, otherwise=URL('liste'))
    # On sélectionne la divisions correspondante
    division = db(db.divisions.id == id_div).select()
    # On récupère les votes correspondants à cette division ainsi que les informations relatives en membres qui ont voté grâce à une requête jointe
    votes = db(db.votes.id_division == id_div).select(db.votes.ALL, db.members.ALL, left=db.members.on(db.members.id == db.votes.id_member))

    # On récupère le nombre de votes de chaque type afin d'afficher un résumé
    pour = db((db.votes.vote == "Aye") & (db.votes.id_division == id_div)).count()
    contre = db((db.votes.vote == "No") & (db.votes.id_division == id_div)).count()

    return dict(div=division, votes=votes, pour=pour, contre=contre)

@auth.requires_membership('teller') # Permet de n'autoriser l'accès qu'aux membres du groupe teller
def new():
    # On crée le formulaire qu'on va utiliser pour ajouter une nouvelle division
    form = FORM(
        'Question', INPUT(_name='question', requires=IS_NOT_EMPTY(), _class='input-custom-form'), BR(),
        'Numéro', INPUT(_name='number', _type='integer', requires=IS_NOT_EMPTY(), _class='input-custom-form'), BR(),
        'Date', INPUT(_name='date', _type='date', requires=IS_DATE(), _class='input-custom-form'), BR(),
        'Votes', INPUT(_name='votes', _type='file', requires=IS_NOT_EMPTY(), _class='input-custom-form'), BR(),
        INPUT(_value='Soumettre', _type='submit'))

    # Si le formulaire est accepté
    if form.process().accepted:
        # Ajout de la division et sauvegarde de son id
        new_div_id = db.divisions.insert(numero = form.vars.number, question = form.vars.question, date_div=form.vars.date)

        # Ajout des votes à la bdd sur base du csv
        db.votes.import_from_csv_file(form.vars.votes.file)

        # Lien entre les votes et la division
        for vote in db(db.votes.id_division == None).select():
            vote.update_record(id_division = new_div_id)

        response.flash = "form accepted and sent"

    return dict(form=form)
