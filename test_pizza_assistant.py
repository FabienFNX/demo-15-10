import unittest
from unittest.mock import MagicMock
from pizza_assistant import PizzaAssistant

class TestPizzaAssistant(unittest.TestCase):

    def setUp(self):
        self.model = "text-davinci-003"
        self.assistant = PizzaAssistant(model=self.model)
        self.assistant.client.chat.completions.create = MagicMock()

    def test_call_with_valid_conversation(self):
        conversation = [
            {"role": "user", "content": "What pizza do you recommend?"},
            {"role": "assistant", "content": "I recommend a Margherita pizza."}
        ]
        expected_response = "I recommend a Margherita pizza."
        
        # Mock the response from OpenAI API
        self.assistant.client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=expected_response))]
        )

        response = self.assistant.call(conversation)
        self.assertEqual(response, expected_response)
        self.assistant.client.chat.completions.create.assert_called_once_with(
            model=self.model,
            messages=[
                {"role": "system", "content": self.assistant.SYSTEM_PROMPT},
                *conversation
            ]
        )

    def test_call_with_empty_conversation(self):
        conversation = []
        expected_response = "I recommend a Margherita pizza."
        
        # Mock the response from OpenAI API
        self.assistant.client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=expected_response))]
        )

        response = self.assistant.call(conversation)
        self.assertEqual(response, expected_response)
        self.assistant.client.chat.completions.create.assert_called_once_with(
            model=self.model,
            messages=[
                {"role": "system", "content": self.assistant.SYSTEM_PROMPT},
                *conversation
            ]
        )

if __name__ == '__main__':
    unittest.main()