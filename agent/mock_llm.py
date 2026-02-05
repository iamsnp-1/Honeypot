class MockLLM:
    def generate(self, system, prompt, max_tokens=60):
        """
        Deterministic mock response.
        This simulates a confused but cooperative human reply.
        """
        return "I’m not sure… can you explain once?"
