import tiktoken
from app.core.config import settings


class TokenUtils:
    def __init__(self, model=None):
        self.model = model or settings.OPENAI_MODEL
        self.encoding = tiktoken.encoding_for_model(self.model)

    def count_tokens(self, messages):
        """
        Count the number of tokens in a list of messages using tiktoken.

        Args:
            messages (list): The list of messages to be tokenized.

        Returns:
            int: The number of tokens.
        """
        num_tokens = 0
        for message in messages:
            for value in message.values():
                num_tokens += len(self.encoding.encode(value))
        return num_tokens

    def estimate_cost(self, num_tokens):
        """
        Estimate the cost of the API call based on the number of tokens.

        Args:
            num_tokens (int): The number of tokens.

        Returns:
            float: The estimated cost in USD.
        """
        # Define cost per 1M tokens for different models
        cost_per_1M_tokens = {
            "gpt-3.5-turbo": 1.50,  # Cost per 1M tokens for gpt-3.5-turbo
            "gpt-4o": 15.00,  # Cost per 1M tokens for gpt-4o
        }

        if self.model in cost_per_1M_tokens:
            cost_per_token = cost_per_1M_tokens[self.model] / 1_000_000
            return num_tokens * cost_per_token
        else:
            raise ValueError(f"Model {self.model} not supported for cost estimation.")
