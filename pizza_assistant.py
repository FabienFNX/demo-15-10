from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import MessagesPlaceholder

class PizzaAssistant:
    """A pizza recommendation assistant powered by OpenAI's API."""
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

    def __init__(self, model: str):
        self.client = ChatOpenAI(model_name=model)

    def call(self, conversation: list):
        """Call the assistant with a conversation."""
        messages = [SystemMessage(self.SYSTEM_PROMPT), MessagesPlaceholder("conversation")]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.client
        result = chain.invoke({"conversation": conversation})
        return result.content
