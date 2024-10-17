import qcm # Pour les questions
import curses # Pour l'interface de la console et les touches
import os # Pour lister les fichiers
import random # Pour mélanger les questions

def play(interface):
    """
    Fonction principale du jeu.
    :pre: A besoin de l'interface de la console.
    :post: Joue une partie de QCM.
    """

    # On cache le curseur
    curses.curs_set(0)

    # On récupère la taille de la console
    height, width = interface.getmaxyx()

    # On vérifie que la console est assez grande
    if height < 20 or width < 80:
        interface.addstr('La console est trop petite pour afficher le jeu correctement. Veuillez l\'agrandir.')
        interface.getch()
        return
    
    # On commence le jeu
    start_game(interface)

    # On récupère les choix de questions et de pondération
    mcq = select_mcq(interface)
    interface.erase()
    weighting = select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Comment voulez-vous pondérer les questions ? [2/2]", ['Sans pénalité', 'Pélanité en cas de mauvais réponses', 'Détection Robot', 'Les 3 pondérations à la fois'], interface)
    interface.erase()

    # On vérifie si l'utilisateur est un robot si la pondération est détection de robot ou les 3 pondérations
    robot = False
    if weighting >= 2:
        robot = detect_robot(interface)
        interface.erase()

    # On mélange les questions
    random.shuffle(mcq)

    # On lance le QCM, on récupère le nombre de bonnes réponses
    correct_anwser = start_mcq(mcq, interface)
    questions_total = len(mcq)

    # On calcule les scores en fonction de la pondération
    # Sans pénalité
    weighting_0 = correct_anwser    
    # Pénalité en cas de mauvaises réponses
    weighting_1 = correct_anwser - (questions_total - correct_anwser)
    # Détection de robot
    weighting_2 = score_robot(correct_anwser, mcq)
    if robot:
        weighting_2 = 0
    
    # On affiche le score final
    show_score(weighting, weighting_0, weighting_1, weighting_2, questions_total, interface)

    # On demande si l'utilisateur veut rejouer
    play_again = select("Voulez-vous rejouer ?", ['Oui', 'Non'], interface)
    if play_again == 0:
        interface.erase()
        play(interface)
    else:
        interface.addstr('  Merci d\'avoir joué !')
    
    # On attend que l'utilisateur appuie sur une touche pour quitter
    interface.getch()

def start_game(interface):
    """
    Affiche l'écran de démarrage du jeu.
    :pre: A besoin de l'interface de la console.
    """

    # On affiche le titre du jeu
    interface.addstr('\n\n')
    interface.addstr('   ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ _________ ____ \n')
    interface.addstr('  ||Q |||U |||I |||Z |||       |||P |||R |||O |||J |||E |||T |||       |||2 ||\n')
    interface.addstr('  ||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||_______|||__||\n')
    interface.addstr('  |/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|\n')
    interface.addstr('\n\n')
    interface.addstr('  Bienvenue dans le jeu de QCM !', curses.A_BOLD)
    interface.addstr('\n\n')
    interface.addstr('  Appuyer sur Entrer pour commencer')

    # On attend que l'utilisateur appuie sur Entrer pour continuer
    while interface.getch() != ord('\n'):
        pass
    
    # On affiche le tutoriel
    select(f"Tutoriel\n\n  Vous allez devoir répondre à une série de questions à choix multiples.\n  Pour répondre, utilisez les flèches directionnelles pour sélectionner la réponse souhaitée\n  et appuyez sur la touche Entrer pour valider.", ['Continuer', 'Toujours continuer'], interface)

def select_mcq(interface):
    """
    Permet de sélectionner un fichier de questions.
    :pre: A besoin de l'interface de la console.
    :post: Retourne la liste des questions.
    """

    # On récupère les fichiers de questions
    question_files = os.listdir('QCM/')

    # On affiche les fichiers de questions et on demande à l'utilisateur d'en choisir un
    answer = select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Quel fichier de questions voulez-vous utiliser ? [1/2]", question_files, interface)
    file = 'QCM/' + question_files[answer]

    # On charge les questions du fichier et on les retourne
    return qcm.build_questionnaire(file)

def detect_robot(interface):
    """
    Permet de détecter si l'utilisateur est un robot.
    :pre: A besoin de l'interface de la console.
    :post: Retourne True si l'utilisateur est un robot, False sinon.
    """

    # On mélange les réponses pour que l'utilisateur ne puisse pas les deviner, mais on garde la première réponse à 'Oui'
    answers = ['Oui', 'Oui', 'Oui', 'Oui']
    answers_rest = ['Oui', 'Oui', 'Oui' ,'Non']
    random.shuffle(answers_rest)
    answers += answers_rest

    # On affiche la question et on demande à l'utilisateur de répondre
    selected = select("Êtes-vous un robot ?", answers, interface)

    # On retourne la réponse
    if answers[selected] == 'Oui':
        return True

    return False

def start_mcq(questions, interface):
    """
    Permet de lancer une série de questions.
    :pre: A besoin de la liste des questions et de l'interface
    :post: Retourne le nombre de bonnes réponses.
    """
    
    # Calcul du nombre de bonnes réponses
    correct_answer = 0

    for index, question in enumerate(questions):
        # On mélange les réponses
        random.shuffle(question[1])

        # On crée une liste des réponses possibles
        answers = []
        for answer in question[1]:
            answers.append(answer[0])

        # On demande à l'utilisateur de sélectionner une réponse
        answer = select(f"{create_progress_bar(index + 1, len(questions), 60)} [{str(index + 1)}/{str(len(questions))}]\n\n  {question[0]}", answers, interface)

        # On récupère la réponse sélectionnée et on vérifie si elle est correcte
        selected = question[1][answer]
        correct = selected[1]
        if correct:
            interface.addstr('  Bonne réponse !', curses.A_BOLD)
            correct_answer += 1
        else:
            interface.addstr('  Mauvaise réponse... ' + selected[2], curses.A_BOLD)
        
        # On attend que l'utilisateur appuie sur une touche pour continuer
        interface.getch()

        # On efface l'écran
        interface.erase()

    return correct_answer

def show_score(weighting, weighting_0, weighting_1, weighting_2, lenght, interface):
    """
    Affiche le score final.
    :pre: A besoin du mode de pondération,du nombre de bonnes réponses pour chaque pondération et de l'interface.
    :post: Affiche le score final. 
    """
    # On affiche le score final
    interface.addstr('\n\n')
    interface.addstr('  Score final\n\n', curses.A_BOLD)

    if weighting == 0 or weighting == 3:
        interface.addstr('  - Sans pénalité [' + str(weighting_0) + '/' + str(lenght) + ']\n')
    if weighting == 1 or weighting == 3:
        interface.addstr('  - Pénalité en cas de mauvaises réponses [' + str(weighting_1) + '/' + str(lenght) + ']\n')
    if weighting == 2 or weighting == 3:
        interface.addstr('  - Détection de robot [' + str(weighting_2) + '/' + str(lenght) + ']\n')

    interface.addstr('\n\n  Appuyer sur Entrer pour continuer')
    interface.getch()


def select(question, answers, interface):
    """
    Permet de sélectionner une réponse parmi plusieurs.
    :pre: A besoin du titre de la question, des réponses possibles et de l'interface
    :post: Retourne la réponse sélectionnée.
    """

    # On crée les styles pour les réponses, sélectionnée ou non
    style = []
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    style.append(curses.color_pair(1))

    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    style.append(curses.color_pair(2))

    # Donne la question sélectionnée
    selected = 0

    # Donne la touche appuyée
    key = None

    # Tant que l'utilisateur n'a pas appuyé sur Entrer
    while key != ord('\n'):

        # On efface l'écran
        interface.erase()

        # On affiche la question
        interface.addstr('\n\n')
        interface.addstr("  " + question, curses.A_BOLD)
        interface.addstr('\n\n')
        
        # On affiche les réponses, en mettant en surbrillance celle sélectionnée
        for i in range(len(answers)):
            if i == selected:
                select_style = style[1]
            else:
                select_style = style[0]
            
            interface.addstr("   - ")
            interface.addstr(answers[i] + '\n', select_style)
        
        interface.addstr('\n\n')

        # On récupère la touche appuyée
        key = interface.getch()

        # On change la réponse sélectionnée en fonction de la touche appuyée, en vérifiant qu'elle est dans les limites
        if key == curses.KEY_DOWN and selected < len(answers) - 1:
            selected += 1
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1

    # On retourne la réponse sélectionnée
    return selected

def score_robot(correct_answers, mcq):
    """
    Calcule le score d'un robot.
    :pre: A besoin de la liste des questions.
    :post: Retourne le score du robot.
    """

    # On compte le nombre de bonnes et de mauvaises réponses
    true_answers = 0
    false_answers = 0

    # On parcourt les questions et les réponses
    for question in mcq:
        for answer in question[1]:
            # On vérifie si la réponse est correcte ou non
            if answer[1]:
                true_answers += 1
            else:
                false_answers += 1

    # On calcule le score du robot, en prenant en compte le nombre de bonnes et de mauvaises réponses
    # On ajoute un point pour chaque bonne réponse
    # La pénalité est calculée en fonction de la différence entre les bonnes et les mauvaises réponses
    not_correct_point = (false_answers - (true_answers + false_answers) / 2) / false_answers

    # On retourne le score, essayant de se rapprocher le plus possible de 0
    score = correct_answers + not_correct_point*(len(mcq)-correct_answers) - len(mcq) / 2
    return score

def create_progress_bar(progress, total, length):
    """
    Crée une barre de progression.
    :pre: A besoin de la progression actuelle, du total et de la longueur de la barre.
    :post: Retourne la barre de progression.
    """

    bar = '['
    for i in range(length):
        # On ajoute un # si on est avant la progression actuelle, sinon un -
        if i < progress * length // total:
            bar += '#'
        else:
            bar += '-'
    bar += ']'

    return bar

# Initialisation de la console, lancement du jeu
curses.wrapper(play)