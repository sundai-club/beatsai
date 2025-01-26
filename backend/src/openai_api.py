from openai import OpenAI


class OpenAIAPI:
    def __init__(self):
        self.api = OpenAI()

    def generate_text(self, system_prompt, prompt):
        return self.api.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
                ],
            max_tokens=4096,
        ).choices[0].message.content
