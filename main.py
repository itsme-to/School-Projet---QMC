import qcm
import curses
import os
import random

def play(stdscr):
    """
    Fonction principale du jeu.
    :pre: A besoin de l'interface de la console.
    :post: Joue une partie de QCM.
    """

    start_game(stdscr)
    mcq = select_mcq(stdscr)
    stdscr.erase()
    weighting = select_weighting(stdscr)
    stdscr.erase()

    robot = False
    if weighting >= 2:
        robot = detect_robot(stdscr)
        stdscr.erase()

    random.shuffle(mcq)
    correct_anwser = start_mcq(mcq, stdscr)
    questions_total = len(mcq)

    weighting_0 = correct_anwser
    weighting_1 = correct_anwser - (questions_total - correct_anwser)
    weighting_2 = score_robot(correct_anwser, mcq)
    if robot:
        weighting_2 = 0
    
    show_score(weighting, weighting_0, weighting_1, weighting_2, questions_total, stdscr)
    
    stdscr.getch()

def start_game(stdscr):
    """
    Affiche l'écran de démarrage du jeu.
    :pre: A besoin de l'interface de la console.
    """

    stdscr.addstr('\n\n')
    stdscr.addstr('   ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ _________ ____ \n')
    stdscr.addstr('  ||Q |||U |||I |||Z |||       |||P |||R |||O |||J |||E |||T |||       |||2 ||\n')
    stdscr.addstr('  ||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__|||_______|||__||\n')
    stdscr.addstr('  |/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|\n')
    stdscr.addstr('\n\n')
    stdscr.addstr('  Bienvenue dans le jeu de QCM !', curses.A_BOLD)
    stdscr.addstr('\n\n')
    stdscr.addstr('  Appuyer sur Entrer pour commencer')

    while stdscr.getch() != ord('\n'):
        pass

def select_mcq(stdscr):
    """
    Permet de sélectionner un fichier de questions.
    :pre: A besoin de l'interface de la console.
    :post: Retourne la liste des questions.
    """

    question_files = os.listdir('QCM/')
    answer = select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Quel fichier de questions voulez-vous utiliser ? [1/2]", question_files, stdscr)
    file = 'QCM/' + question_files[answer]

    return qcm.build_questionnaire(file)

def select_weighting(stdscr):
    """
    Permet de sélectionner un mode de pondération.
    :pre: A besoin de l'interface de la console.
    :post: Retourne le mode de pondération sélectionné.
    """

    return select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Comment voulez-vous pondérer les questions ? [2/2]", ['Sans pénalité', 'Pélanité en cas de mauvais réponses', 'Détection Robot', 'Les 3 pondérations à la fois'], stdscr)

def detect_robot(stdscr):
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

    selected = select("Êtes-vous un robot ?", answers, stdscr)

    if answers[selected] == 'Oui':
        return True

    return False

def start_mcq(questions, stdscr):
    """
    Permet de lancer une série de questions.
    :pre: A besoin de la liste des questions et de l'interface
    :post: Retourne le nombre de bonnes réponses.
    """
    correct_answer = 0

    for question in questions:
        random.shuffle(question[1])
        index = questions.index(question)

        answers = []
        for answer in question[1]:
            answers.append(answer[0])

        answer = select(f"{create_progress_bar(index + 1, len(questions), 60)} [{str(index + 1)}/{str(len(questions))}]\n\n  {question[0]}", answers, stdscr)

        selected = question[1][answer]
        correct = selected[1]
        if correct:
            stdscr.addstr('  Bonne réponse !', curses.A_BOLD)
            correct_answer += 1
        else:
            stdscr.addstr('  Mauvaise réponse... ' + selected[2], curses.A_BOLD)
        
        stdscr.getch()
        stdscr.erase()

    return correct_answer

def show_score(weighting, weighting_0, weighting_1, weighting_2, lenght, stdscr):
    """
    Affiche le score final.
    :pre: A besoin du mode de pondération,du nombre de bonnes réponses pour chaque pondération et de l'interface.
    :post: Affiche le score final. 
    """

    stdscr.addstr('\n\n')
    stdscr.addstr('  Score final\n\n', curses.A_BOLD)

    if weighting == 0:
        stdscr.addstr('  Sans pénalité [' + str(weighting_0) + '/' + str(lenght) + ']\n')
    elif weighting == 1:
        stdscr.addstr('  - Pénalité en cas de mauvaises réponses [' + str(weighting_1) + '/' + str(lenght) + ']\n')
    elif weighting == 2:
        stdscr.addstr('  - Détection de robot [' + str(weighting_2) + '/' + str(lenght) + ']\n')
    else:
        stdscr.addstr('  Les 3 pondérations à la fois\n')
        stdscr.addstr('  - Sans pénalité : [' + str(weighting_0) + '/' + str(lenght) + ']\n')
        stdscr.addstr('  - Pénalité en cas de mauvaises réponses : [' + str(weighting_1) + '/' + str(lenght) + ']\n')
        stdscr.addstr('  - Détection de robot : [' + str(weighting_2) + '/' + str(lenght) + ']\n')
    
    stdscr.addstr('\n\n')

def select(question, answers, stdscr):
    """
    Permet de sélectionner une réponse parmi plusieurs.
    :pre: A besoin du titre de la question, des réponses possibles et de l'interface
    :post: Retourne la réponse sélectionnée.
    """

    style = []
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    style.append(curses.color_pair(1))

    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    style.append(curses.color_pair(2))

    selected = 0
    key = None

    while key != ord('\n'):
        stdscr.erase()

        stdscr.addstr('\n\n')
        stdscr.addstr("  " + question, curses.A_BOLD)
        stdscr.addstr('\n\n')
        
        for i in range(len(answers)):
            if i == selected:
                select_style = style[1]
            else:
                select_style = style[0]
            
            stdscr.addstr("   - ")
            stdscr.addstr(answers[i] + '\n', select_style)
        
        stdscr.addstr('\n\n')

        key = stdscr.getch()
        if key == curses.KEY_DOWN and selected < len(answers) - 1:
            selected += 1
        elif key == curses.KEY_UP and selected > 0:
            selected -= 1
    return selected

def score_robot(correct_answers, mcq):
    """
    Calcule le score d'un robot.
    :pre: A besoin de la liste des questions.
    :post: Retourne le score du robot.
    """
    true_answers = 0
    false_answers = 0

    for question in mcq:
        for answer in question[1]:
            if answer[1]:
                true_answers += 1
            else:
                false_answers += 1

    not_correct_point = (false_answers - (true_answers + false_answers) / 2) / false_answers
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
        if i < progress * length // total:
            bar += '#'
        else:
            bar += '-'
    bar += ']'

    return bar

curses.wrapper(play)