from typing import Dict, TypedDict, Optional
# pip install langgraph, httpx
# pip install requests --upgrade
from langgraph.graph import StateGraph, END
from enum import Enum


class OrderState(Enum, str):
    # NODE
    WELCOME = "WELCOME"
    LISTEN = "LISTEN"
    ORDER = "ORDER"
    PAYMENT = "PAYMENT"
    CONFIRM = "CONFIRM"
    # EDGE
    READY = "READY"
    PUT_ORDER = "PUT_ORDER"
    PAY = "PAY"
    SUCCESS = "SUCCESS"
    CANCEL = "CANCEL"
    FAIL = "FAIL"
    OK = "OK"


class GraphState(TypedDict):
    question: Optional[str] = None
    classification: Optional[str] = None
    response: Optional[str] = None


class OrderAgent:
    def __init__(self):
        self.workflow = StateGraph(GraphState)
        self.buildWorkflow()

    def welcome(self, state):
        pass

    def ready(self, state):
        pass

    def order(self, state):
        pass

    def payment(self, state):
        pass

    def cancel(self, state):
        pass

    def confirm(self, state):
        pass

    def classify(self, q: str):
        if q.startswith("Hello"):
            return "greeting"
        else:
            return "handle_search"

    def classify_input_node(self, state):
        question = state.get('question', '').strip()
        classification = self.classify(question)  # Assume a function that classifies the input
        return {"classification": classification}

    def handle_greeting_node(self, state):
        return {"response": "Hello! How can I help you today?"}

    def handle_search_node(self, state):
        question = state.get('question', '').strip()
        search_result = f"Search result for '{question}'"
        return {"response": search_result}

    def decide_next_node(self, state):
        return "handle_greeting" if state.get('classification') == "greeting" else "handle_search"

    def buildWorkflow(self):
        """
        그래프를 생성한다.
        """

        # 노드 정의
        self.workflow.add_node(OrderState.WELCOME, self.welcome)
        # 간선 정의
        self.workflow.add_conditional_edges(
            OrderState.WELCOME,
            self.decide_next_node,
            {
                OrderState.READY: OrderState.LISTEN,
            }
        )

        self.workflow.add_node(OrderState.LISTEN, self.ready)
        self.workflow.add_conditional_edges(
            OrderState.LISTEN,
            self.decide_next_node,
            {
                OrderState.PAY: OrderState.PAYMENT,
                OrderState.PUT_ORDER: OrderState.ORDER,
            }
        )

        self.workflow.add_node(OrderState.ORDER, self.order)
        self.workflow.add_conditional_edges(
            OrderState.ORDER,
            self.decide_next_node,
            {
                OrderState.READY: OrderState.LISTEN,
            }
        )

        self.workflow.add_node(OrderState.PAYMENT, self.payment)
        self.workflow.add_conditional_edges(
            OrderState.PAYMENT,
            self.decide_next_node,
            {
                OrderState.SUCCESS: OrderState.CONFIRM,
                OrderState.CANCEL: OrderState.LISTEN,
                OrderState.FAIL: END,
            }
        )

        self.workflow.add_node(OrderState.CONFIRM, self.confirm)
        self.workflow.add_conditional_edges(
            OrderState.CONFIRM,
            self.decide_next_node,
            {
                OrderState.OK: END,
            }
        )

        self.workflow.set_entry_point(OrderState.WELCOME)

        # self.workflow.add_node("classify_input", self.classify_input_node)
        # self.workflow.add_node("handle_greeting", self.handle_greeting_node)
        # self.workflow.add_node("handle_search", self.handle_search_node)
        # self.workflow.add_conditional_edges(
        #     "classify_input",
        #     self.decide_next_node,
        #     {
        #         "handle_greeting": "handle_greeting",
        #         "handle_search": "handle_search"
        #     }
        # )
        #
        # self.workflow.set_entry_point("classify_input")
        # self.workflow.add_edge('handle_greeting', END)
        # self.workflow.add_edge('handle_search', END)

    def execute(self):
        app = self.workflow.compile()
        inputs = {"question": "Hello, how are you?"}
        result = app.invoke(inputs)
        print(result)


if __name__ == '__main__':
    oa = OrderAgent()
    oa.execute()

