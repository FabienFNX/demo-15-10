from langsmith import Client

client = Client()

DATASET_NAME = "QA Example Demo 15 10 2024"
dataset = client.create_dataset(DATASET_NAME)
client.create_examples(
    inputs=[
            {
                "question": "Quels sont les choix de tailles pour la pizza pepperoni ?"
            },
            {
                "question": "Pouvez-vous me dire si vous avez des garnitures disponibles pour les pizzas ?"
            },
            {
                "question": "Combien coûte la petite portion de frites ?"
            },
            {
                "question": "Est-ce que vous avez des boissons gazeuses ?"
            },
            {
                "question": "Quels sont les suppléments que je peux ajouter à ma pizza au fromage ?"
            },
            {
                "question": "Comment fonctionne la livraison ?"
            },
            {
                "question": "Est-ce que la pizza aubergine est disponible en petite taille ?"
            },
            {
                "question": "Combien coûte une bouteille d’eau ?"
            },
            {
                "question": "Puis-je ajouter du bacon sur ma pizza au fromage ?"
            },
            {
                "question": "Est-ce que je peux commander pour un retrait ?"
            }
        ],
    outputs=[
            {
                "answer": "Pour la pizza pepperoni, nous avons trois tailles : grande (12.95), moyenne (10.00) et petite (7.00)."
            },
            {
                "answer": "Bien sûr ! Vous pouvez ajouter du fromage supplémentaire (2.00), des champignons (1.50), de la sauce (3.00), du bacon (3.50), de la sauce IA (1.50) ou des poivrons (1.00)."
            },
            {
                "answer": "La petite portion de frites coûte 3.50."
            },
            {
                "answer": "Oui, nous avons du coca et du sprite en trois tailles : grande (3.00), moyenne (2.00) et petite (1.00)."
            },
            {
                "answer": "Pour la pizza au fromage, vous pouvez ajouter du fromage supplémentaire (2.00), des champignons (1.50), de la sauce (3.00), du bacon (3.50), de la sauce IA (1.50) ou des poivrons (1.00)."
            },
            {
                "answer": "Pour la livraison, nous aurons besoin de votre adresse et il n’y a pas de frais supplémentaires."
            },
            {
                "answer": "Oui, la pizza aux aubergines est disponible en petite taille à 6.75."
            },
            {
                "answer": "Une bouteille d’eau coûte 5.00."
            },
            {
                "answer": "Bien sûr ! Vous pouvez ajouter du bacon pour 3.50."
            },
            {
                "answer": "Oui, vous pouvez choisir le retrait en venant directement chercher votre commande au restaurant."
            }
        ],
    dataset_id=dataset.id,
)