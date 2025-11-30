import os
import random
from elevenlabs.client import ElevenLabs

class VoiceManager:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = None
        if self.api_key:
            self.client = ElevenLabs(api_key=self.api_key)
            
        # Archetype-based Voice Mapping
        # We map the suspect's 'archetype' (from image metadata or role logic) or gender to these.
        
        self.voices = {
            "male": {
                "executive": "ErXwobaYiN019PkySvjV", # Antoni (Polished)
                "worker": "wI49R6YUU5NNP1h0CECc",    # Josh (Casual)
                "criminal": "VR6AewLTigWg4xSOukaG",  # Arnold (Gravelly)
                "artist": "D38z5RcWu1voky8WS1ja",    # Fin (Expressive)
                "default": "TxGEqnHWrfWFTfGW9XjX"    # Josh
            },
            "female": {
                "executive": "21m00Tcm4TlvDq8ikWAM", # Rachel (Professional)
                "worker": "AZnzlk1XvdvUeBnXmlld",    # Domi (Strong)
                "socialite": "EXAVITQu4vr4xnSDxMaL", # Bella (Intense)
                "artist": "nDJIICjR9zfJExIFeSCN",    # Bella
                "default": "6u6JbqKdaQy89ENzLSju"    # Rachel
            }
        }

    def assign_voice(self, gender, role=""):
        """Pick a voice based on gender and role archetype."""
        g = "male" if gender.lower() == "male" else "female"
        role = role.lower()
        
        # Simple archetype matching logic (matches game_logic.js)
        archetype = "default"
        if "ceo" in role or "cfo" in role or "manager" in role or "dealer" in role:
            archetype = "executive"
        elif "janitor" in role or "chef" in role or "caterer" in role:
            archetype = "worker"
        elif "artist" in role or "curator" in role:
            archetype = "artist"
        elif "heir" in role or "collector" in role or "sister" in role:
            archetype = "socialite"
        elif "ex-" in role or "customer" in role:
            archetype = "criminal"
            
        # Return specific voice or random if not found? 
        # Better to return specific to ensure personality match.
        voice_map = self.voices[g]
        return voice_map.get(archetype, voice_map["default"])

    def generate_audio(self, text, voice_id):
        """Generates audio bytes from text."""
        if not self.client:
            print("Warning: No ElevenLabs API Key. Skipping TTS.")
            return None
            
        try:
            # Modern SDK usage
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1"
            )
            # Consolidate generator into bytes
            audio_bytes = b"".join(audio_generator)
            return audio_bytes
        except Exception as e:
            print(f"ElevenLabs Error: {e}")
            return None