import qcm

"""
    Exemple d'utilisation de la librairie de lecture de fichiers QCM
"""


if __name__ == '__main__':
    filename = "Projet2/QCM.txt"

    # Chargement du questionnaire
    questions = qcm.build_questionnaire(filename)

    print(questions)
    
  

