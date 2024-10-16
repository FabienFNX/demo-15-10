from langchain_openai import ChatOpenAI
from langchain import hub
from langsmith import evaluate
from langsmith.evaluation import LangChainStringEvaluator
from pizza_assistant import PizzaAssistant

assistant = PizzaAssistant(model="gpt-4o-mini")
prompt = hub.pull("demo-15-10-evaluator")
eval_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
qa_evaluator = LangChainStringEvaluator("qa", config={"llm": eval_llm, "prompt": prompt})

def langsmith_app(inputs):
    output = assistant.call([{"role": "user", "content": inputs["question"]}])
    return {"output": output}

experiments_results = evaluate(
    langsmith_app,
    data="QA Example Demo 15 10 2024",
    evaluators=[qa_evaluator],
    experiment_prefix="demo-15-10-2024",
    )