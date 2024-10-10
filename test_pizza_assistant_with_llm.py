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
