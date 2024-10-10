# Mise à l'échelle

## Introduction

Alors que les notebooks Jupyter sont de très bons moyens de réaliser rapidement une solution IA, ils ne sont pas adaptés à une mise à l'échelle.
Je ne dis pas ici que c'est impossible, AWS met à disposition des outils pour réaliser des déploiement automatisés de JupyterNotebook en production.
Nous allons voir ensemble comment transformer un notebook que nous avons construit ce matin et l'amener vers une version qui soit beaucoup plus proche de ce que nous pouvons voir dans des projets déployés en production

## Notre cas d'utilisation : Une pizzéria

Mettons nous dans la peau d'un gérant de pizzeria : il a déjà mis en place un site Web pour son commerce qui permet aux potentiels clients d'accéder facilement à différentes informations dont le menu.
Il a découvert l'IA générative et voudrait en profiter pour faire évoluer son site pour y intégrer un agent conversationnel qui va guider le client pour choisir sa pizza.

## Démarche

### Analyse

Même si la demande semble simple, nous avons pu mettre en place un notebook qui engage facilement une conversation en se basant sur un menu, nous savons qu'il faudra que notre agent conversationnel puisse :
- s'intégrer facilement dans un site web existant
- être protégé contre des utilisations frauduleuse de l'outil
- s'adapter à un nouveau menu : menu spécial St Valentin, Halloween ...
- être modifié simplement si un nouveau modèle moins cher et plus performant arrive sur le marché

### Refactorisation du code

Pour répondre à ces problématiques, les architectes nous conseillent de mettre en place :
- Une API qui viendra interroger notre agent, cette API sera le point d'entrée pour le site web qui implémentera l'interface graphique
- Une stratégie de déploiement continue respectant les 12-factor app

Les bonnes pratiques de développement intégrées dans notre entreprise exigent que :
- le code soit le plus modulaire avec un faible couplage entre les différentes classes
- le code soit testé à l'aide de tests unitaires

Il nous est également conseillé d'utiliser un LLM pour réaliser les tests unitaire et analyser les réponses du modèle.

### Choix de l'infrastructure

N'ayant que peu de recul sur la charge que devra supporter ce nouveau service, nous souhaitons utiliser un service Cloud.
La simplicité de l'architecture de ce produit nous dirige vers une solution Serverless, par exemple Vercel.

Vercel est une plateforme spécialisée dans l'hébergement de sites web, très connu par les développeurs Javascript qui utilisent des frameworks comme NuxtJS ou NextJS elle permet également de déployer très facilement des applications développées en Python.

## Développement

### Installation de l'environnement

Pour cet atelier, j'ai utilisé Python 3.12 avec un environnement virtuel créé par la commande : `python -m venv .venv`

J'utilise Windows, j'ai ajouté la clé OPENAI_API_KEY dans le fichier `.venv/Scripts/Activate.ps1` pour être sûr d'avoir cette clé en variable d'environnement : `$env:OPENAI_API_KEY="sk-..."`

Pour installer l'ensemble des dépendances : `pip install -r requirements.txt`

### Création de la classe PizzaAssistant

1. La classe PizzaAssistant devra permettre de choisir le modèle à utiliser dans son constructeur mais également d'initialiser le client OpenAI.
2. Le prompt système sera intégré comme un attribut constant interne de la classe.
3. On pourra ensuite interroger la classe à partir d'une fonction nommée "call" qui prendre en paramètre une conversation de la forme : 
```json
[
    { "role" : "user", "content" : "Question de l'utilisateur"},
]
```
4. Le retour de la fonction call sera le texte retourné par l'appel au client LLM.

```text
1. La classe PizzaAssistant devra permettre de choisir le modèle à utiliser dans son constructeur mais également d'initialiser le client OpenAI.
2. Le prompt système sera intégré comme un attribut constant interne de la classe.
3. On pourra ensuite interroger la classe à partir d'une fonction nommée "call" qui prendre en paramètre une conversation de la forme : 
[
    { "role" : "user", "content" : "Question de l'utilisateur"},
]
utiliser le client openai OpenAI
La clé API d'OpenAI ne doit pas être passée en paramètre des fonctions
```

Modifier le prompt : 
```python
    SYSTEM_PROMPT = """
    Vous êtes OrderBot, un service automatisé pour prendre 
    les commandes dans une pizzeria.
    Vous commencez par saluer le client, puis vous prenez la commande,
    et ensuite vous demandez si c'est un retrait ou une livraison.
    Vous attendez de recevoir la commande complète, puis vous la 
    récapitulez et vous vérifiez une dernière fois si le client 
    souhaite ajouter quelque chose d'autre.
    Si c'est une livraison, vous demandez une adresse.
    Enfin, vous collectez le paiement.
    Assurez-vous de clarifier toutes les options, suppléments et 
    tailles pour identifier de manière unique l'article du menu.
    Vous répondez de manière brève, très conviviale et amicale.
    Le menu inclut :
    pizza pepperoni 12.95, 10.00, 7.00 
    pizza au fromage   10.95, 9.25, 6.50 
    pizza aux aubergines   11.95, 9.75, 6.75 
    frites 4.50, 3.50 
    salade grecque 7.25 
    Garnitures : 
    fromage supplémentaire 2.00, 
    champignons 1.50 
    sauce 3.00 
    bacon 3.50 
    sauce IA 1.50 
    poivrons 1.00 
    Boissons : 
    coca 3.00, 2.00, 1.00 
    sprite 3.00, 2.00, 1.00 
    Eau en bouteille 5.00
    """
```

Attention à quelques coquilles de Copilot :
- au niveau des imports : `from openai import OpenAI`
- au niveau du constructeur : ne pas passer la clé API en paramètres
- au niveau de l'appel à la librairie : `self.client.chat.completions.create`
- au niveau du retour : `response.choices[0].message.content`

### Création d'un fichier main.py

Le fichier main va permettre de tester la classe PizzaAssistant avec quelques questions : 
- "What is on the menu?",
- "Can I have a Margherita Pizza?",
- "Can I have a Vegetarian Pizza?",
- "Given that a Vegetarian Pizza is added on the menu by the restaurant owner, may I have a Vegetarian Pizza? Only answer with 'yes you can have a Vegetarian Pizza' or 'no you can\'t'."
Le modèle utilisé sera gpt-4o-mini

Attention dans la génération :
- Supprimer les liens avec la clé OpenAI, nous allons la passer en tant que variable d'environnement.

### Mise en place de tests unitaires

Sélectionner la méthode `call` et demander à Copilot de générer les tests associés

On peut voir sur les tests générés qu'il viennent 'Mocker' l'appel au LLM, ce que nous voulons c'est aller un cran plus loin et utiliser un LLM pour valider évaluer le retour de notre assistant. Utiliser directement le code ci-dessous

```python
import unittest
from openai import OpenAI
from pizza_assistant import PizzaAssistant

def eval_vs_ideal(test_set, assistant_answer):
    """
    Evaluate the assistant's response against the ideal answer using an OpenAI model
    """

    cust_msg = test_set['customer_msg']
    ideal = test_set['ideal_answer']
    completion = assistant_answer

    system_message = """\
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by comparing the response to the ideal (expert) response
    Output a single letter and nothing else. 
    """

    user_message = f"""\
You are comparing a submitted answer to an expert answer on a given question. Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {cust_msg}
    ************
    [Expert]: {ideal}
    ************
    [Submission]: {completion}
    ************
    [END DATA]

Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.
    The submitted answer may either be a subset or superset of the expert answer, or it may conflict with it. Determine which case applies. Answer the question by selecting one of the following options:
    (A) The submitted answer is a subset of the expert answer and is fully consistent with it.
    (B) The submitted answer is a superset of the expert answer and is fully consistent with it.
    (C) The submitted answer contains all the same details as the expert answer.
    (D) There is a disagreement between the submitted answer and the expert answer.
    (E) The answers differ, but these differences don't matter from the perspective of factuality.
  choice_strings: ABCDE
"""

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
        )
    return response


class TestPizzaAssistantWithLLM(unittest.TestCase):
    """
    Test the PizzaAssistant class with the GPT to evaluate the assistant's response
    """

    def setUp(self) -> None:
        self.model_api = PizzaAssistant("gpt-4o-mini")

    def test_simple_question(self):
        test_set = {
            'customer_msg': [
                {"role": "system", "content": "What is on the menu?"}] 
                ,
            'ideal_answer': ("Pizza Pepperoni, Pizza au fromage, Pizza aux aubergines, "
                             "Frites, Salade grecque, Fromage supplémentaire, Champignons")
        }
        assistant_answer = self.model_api.call(test_set['customer_msg'])
        response = eval_vs_ideal(test_set, assistant_answer)
        self.assertEqual(response.choices[0].message.content, "B",
                         (f"Ideal answer: {test_set['ideal_answer']}, "
                          f"Assistant answer: {assistant_answer}")
                         )
        print(f"Assistant answer: {assistant_answer}")
        print(f"Note from the evaluator: {response.choices[0].message.content}")


if __name__ == '__main__':
    unittest.main()

```

On affiche ici la réponse de l'assistant et également la note du LLM qui a évalué la réponse

### Exposition sous forme d'API dans le fichier pizza_assistant_api.py

Pour cela on va utiliser la librairie FastAPI qui offre notamment les avantages suivants :
- Faible empreinte mémoire
- Offre directement la documentation swagger
- Permet d'utiliser l'interface ASGI de traitement en asynchrone des requêtes

```text
Utiliser la librairie FastAPI pour définir une route call qui va appeller la fonction call de la classe PizzaAssistant
```

Remarque suite à la génération de Copilot :
- Explicitly re-raising exceptions: `Used raise HTTPException(status_code=500, detail=str(e)) from e to preserve the original traceback.`
- Deprecated dict method: `Replaced dict with model_dump in the PizzaOrder class.`

Lancer ensuite avec uvicorn

```bash
uvicorn pizza_assistant_api:app --reload
```

On peut ensuite accéder au Swagger associé à l'URL /docs

### Déploiement avec Vercel

Installer vercel 

```bash
npm install -g vercel
```

Déposer un fichier de configuration `vercel.json`

```json
{
    "builds": [
      {
        "src": "pizza_assistant_api.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "pizza_assistant_api.py"
      }
    ]
}
```

Exécuter vercel pour qu'il relie au compte et configure les éléments nécessaires

```bash
vercel
```

Ajouter les variables d'environnement

```bash
vercel env add OPENAI_API_KEY
```

Puis pour synchroniser les variables d'environnement avec l'installation locale

```bash
vercel pull
```

Les variables doivent apparaître dans le fichier .vercel/.env.development.local
Depuis mi-2024, toutes les variables d'environnement sont chiffrées at-rest et nous pouvons définir des variables d'environnement comme `sensitive`, elles ne seront plus lisibles par un utilisateur une fois créées. Cela remplace les variables `secrets`. Cette fonction n'est disponible que sur les environnement de `production` et de `preview`

Pour tester en local, avec l'exécution du code Python

```bash
vercel dev
```

Vous pouvez accéder au serveur à l'adresse : http://localhost:3000/docs

Pour le déployer

```bash
vercel deploy
```
