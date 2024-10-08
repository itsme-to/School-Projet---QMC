import qcm
import curses
import os
import random

def play(stdscr):
    """
    Fonction principale du jeu.
    """

    start_game(stdscr)
    qmc = select_qmc(stdscr)
    weighting = select_weighting(stdscr)

    random.shuffle(qmc)

    stdscr.addstr('Vous avez choisi la réponse : ' + str(weighting))
    stdscr.getch()

def start_game(stdscr):
    """
    Affiche l'écran de démarrage du jeu.
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

def select_qmc(stdscr):
    """
    Permet de sélectionner un fichier de questions.
    """

    question_files = os.listdir('QCMS/')
    answer = select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Quel fichier de questions voulez-vous utiliser ? [1/2]", question_files, stdscr)
    file = 'QCMS/' + question_files[answer]

    return qcm.build_questionnaire(file)

def select_weighting(stdscr):
    """
    Permet de sélectionner un mode de pondération.
    """

    return select("Avant de commencer, voici quelques questions pour configurer la partie. \n\n  Comment voulez-vous pondérer les questions ? [2/2]", ['Sans pénalité', 'Pélanité en cas de mauvais réponses', '50%', 'Les 3 pondérations à la fois'], stdscr)


def select(question, answers, stdscr):
    """
    Permet de sélectionner une réponse parmi plusieurs.
    :pre: A besoin du titre de la question et des réponses possibles.
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
    
    stdscr.erase()
    return selected

curses.wrapper(play)
    
  
