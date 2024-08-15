import anthropic

class ClaudeManager:
    def __init__(self):
        self.client = anthropic.Client(api_key="your_anthropic_api_key_here")

    def analyze_labels(self, labels_data):
        prompt = f"""Analyze the following image labels and metadata:

{labels_data}

Based on this data, suggest optimal parameters for fine-tuning a Stable Diffusion model, including:
1. Number of training epochs
2. Batch size
3. Learning rate

Provide your recommendations in a JSON format."""

        response = self.client.completions.create(
            model="claude-3.5-sonnet",
            prompt=prompt,
            max_tokens_to_sample=1000,
        )

        return response.completion