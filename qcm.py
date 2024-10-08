#!/usr/bin/env python3


"""
    Exemple d'utilisation de la librairie:
    -------------------------------------

    >>> questions = build_questionnaire("QCM.txt")
    >>> questions[2]
    ["Quel est l'équivalent américain de l'ESA (European Space Agency) ?", [['NASA', True, ''], ['NSA', False, 'La NSA est la National Security Agency'], ['FBI', False, '']]]


    Format détaillé:
    ----------------

    Une question est une liste à deux éléments.
    E.g.: ["La diagonale d'un rectangle est:", [
        ['La somme des cotés', False, 'Relisez le théorème de Pythagore'],
        ['La racine carré de la somme des carrés des cotés', True, '']
    ]
        * Le premier est le texte de la question.
        * Le deuxième est une liste de choix.

    Un choix est une liste à trois éléments. E.g.: ['La somme des cotés', False, 'Relisez le théorème de Pythagore']
        * Le premier est le texte du choix.
        * Le deuxième est un booléen indiquant si ce choix est correct.
        * Le troisième est une explication éventuelle adjointe au choix lors de la correction.

"""


def build_questionnaire(filename):
    """
        Construit le QCM avec les questions contenue dans le fichier donné.
        :type filename: Un string représentant le nom du fichier a charger.

        :return: Une liste de questions
    """
    questions = []
    wording = None
    choices = []
    with open(filename, encoding='utf-8') as file:
        for line in file.readlines():
            if '|' not in line:
                if wording or choices:
                    questions.append([wording, choices])
                wording = None
                choices = []
            else:
                parts = line.strip().split('|')
                if 1 < len(parts) < 5:
                    if parts[0] == 'Q':
                        if not wording and not choices:
                            wording = parts[1]
                            choices = []
                        else:
                            questions.append([wording, choices])
                            wording = None
                            choices = []
                    elif parts[0] == 'A':
                        if parts[2] not in ('V', 'X'):
                            print("Error when loading line:\n\t{}".format(line))
                        else:
                            choices.append([parts[1], parts[2] == 'V', parts[3] if len(parts) > 3 else ''])
                    else:
                        print("Error when loading line:\n\t{}".format(line))
                else:
                    print("Error when loading line:\n\t{}".format(line))

                if line.startswith('Q'):
                    wording = parts[1]

    if wording or choices:
        questions.append([wording, choices])
    return questions
