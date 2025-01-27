from openai import OpenAI
import re
from ast import literal_eval
def parse_response(response):
    matches = re.findall(r'```json(.*?)```', response, re.DOTALL)
    if matches:
        return literal_eval(matches[0])
    else:
        return None


class OpenAIAPI:
    def __init__(self):
        self.api = OpenAI()

    
    def generate_text(self, prompt):
        system_prompt = (
            "You are a specialized text-to-audio prompt generator. "
            "Your goal is to produce concise, well-structured instructions "
            "for an audio generator model."
        )


        response = self.api.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def generate_audio_prompt(self, user_prompt, instrument):
        # System prompt defining the role and purpose of the assistant


        # Combine user instructions with the instrument choice
        # Provide any formatting or style guidelines as needed
        updated_prompt = """The user wants an audio piece featuring only the mentioned instrument, the instrument: {instrument}. 
            Their request: {user_prompt}

            Generate a single, final prompt that includes:
            • Description of the style or genre
            • Mood or atmosphere\n
            • Notable sound effects (if requested)
            • Any specific instructions or details
            Keep the prompt under 200 characters and focus on clarity.
            Provide the output in the following format:

            Output Format:
            ```json{{"prompt": "prompt_text"}} ```

            Output:
            """

        updated_prompt = updated_prompt.format(instrument=instrument, user_prompt=user_prompt)

        response = self.generate_text(updated_prompt)
        prompt = parse_response(response)
        return prompt
