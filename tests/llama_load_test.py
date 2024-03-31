"""Load testing script for the Llama API using Locust."""

from locust import HttpUser, task, between

class LlamaUser(HttpUser):
    """
    Locust user class for load testing the Llama API.

    Attributes:
        wait_time (tuple): Tuple representing the range of time between consecutive requests.
    """

    wait_time = between(1, 5)  # Time between consecutive requests

    @task
    def get_llama_answer(self) -> None:
        """
        Task to simulate a user requesting an answer from the Llama API.

        Returns:
            None
        """
        try:
            input_text = "What is the meaning of life?"
            response = self.client.post("/llama", json={"text": input_text})
            if response.status_code != 200:
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"An error occurred: {e}")
