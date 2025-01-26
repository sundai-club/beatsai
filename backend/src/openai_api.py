from openai import OpenAI

class OpenAIAPI:
    def __init__(self):
        self.api = OpenAI()

    def generate_audio_prompt(self, user_prompt, instrument):
        # System prompt defining the role and purpose of the assistant
        system_prompt = (
            "You are a specialized text-to-audio prompt generator. "
            "Your goal is to produce concise, well-structured instructions "
            "for an audio generator model."
        )

        # Combine user instructions with the instrument choice
        # Provide any formatting or style guidelines as needed
        updated_prompt = (
            f"The user wants an audio piece featuring the instrument: {instrument}. "
            f"Their request: {user_prompt}\n\n"
            "Generate a single, final prompt that includes:\n"
            "• Description of the style or genre\n"
            "• Mood or atmosphere\n"
            "• Notable sound effects (if requested)\n"
            "• Any specific instructions or details\n\n"
            "Keep the prompt under 200 characters and focus on clarity."
        )

        response = self.api.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": updated_prompt}
            ],
            max_tokens=4096,
        )

        return response.choices[0].message.content
