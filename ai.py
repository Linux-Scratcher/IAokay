import sqlite3
import re

# Fonction pour créer la base de données et la table des faits
def create_db():
    conn = sqlite3.connect('learned_facts.db')
    cursor = conn.cursor()
    
    # Créer la table des faits si elle n'existe pas déjà
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Fonction pour ajouter un fait à la base de données
def add_fact(fact):
    conn = sqlite3.connect('learned_facts.db')
    cursor = conn.cursor()
    
    # Ajouter un fait à la base de données
    cursor.execute("INSERT INTO facts (fact) VALUES (?)", (fact,))
    
    conn.commit()
    conn.close()

# Fonction pour récupérer tous les faits appris
def get_all_facts():
    conn = sqlite3.connect('learned_facts.db')
    cursor = conn.cursor()
    
    # Récupérer tous les faits
    cursor.execute("SELECT * FROM facts")
    facts = cursor.fetchall()
    
    conn.close()
    
    return facts

# Fonction pour analyser une question et rechercher une réponse
def answer_question(question):
    facts = get_all_facts()
    question = question.lower()
    
    # Rechercher des faits pertinents en fonction des mots-clés de la question
    relevant_facts = []
    for fact in facts:
        fact_text = fact[1].lower()
        
        # Vérifier si la question contient un mot-clé présent dans un fait
        if any(word in fact_text for word in question.split()):
            relevant_facts.append(fact[1])
    
    if relevant_facts:
        return "Voici ce que je sais :\n" + "\n".join(relevant_facts)
    else:
        return None  # Si aucun fait pertinent n'est trouvé

# Fonction d'interaction avec l'utilisateur
def interact_with_ai():
    print("Bienvenue dans l'IA ! Vous pouvez poser des questions.")

    while True:
        question = input("\nPosez une question à l'IA (ou tapez 'exit' pour quitter) : ")
        
        if question.lower() == 'exit':
            print("Merci d'avoir utilisé l'IA !")
            break
        
        # L'IA essaie de répondre à la question
        answer = answer_question(question)
        
        if answer:
            print(answer)  # Si l'IA a une réponse, elle la donne
        else:
            # Si l'IA n'a pas de réponse, elle demande à l'utilisateur
            print("Je ne sais pas répondre à cette question.")
            new_fact = input("Peux-tu m'apprendre la réponse ? (par exemple : 'L'eau gèle à 0°C.') : ")
            add_fact(new_fact)
            print("Merci de m'avoir appris cela !")

# Création de la base de données si nécessaire
create_db()

# Lancer l'interaction avec l'IA
interact_with_ai()
