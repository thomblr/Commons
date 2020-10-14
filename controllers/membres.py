# -*- coding: utf-8 -*-
def liste():
    # On récupère les tous les membres dont l'id n'est pas null
    members = db(db.members.id!=None).select()
    return dict(aff_memb=members)

def detail():
    # Récupération de l'id du membre passé en paramètre dans l'url
    id_mem = request.args(0, cast=int, otherwise=URL('liste'))
    # On sélectionne le membre dans la bdd donc l'id correspond à celui passé en paramètre
    member = db(db.members.id == id_mem).select()
    # On récupère les votes respectifs de ce membre ainsi que les infos de la division correspondante avec une requête jointe
    votes = db(db.votes.id_member == id_mem).select(db.divisions.id,
                                                    db.divisions.numero,
                                                    db.divisions.question,
                                                    db.divisions.date_div,
                                                    db.votes.vote,
                                                    db.votes.affiliation,
                                                    left=db.votes.on(db.divisions.id == db.votes.id_division))
    return dict(mem=member, votes=votes)
