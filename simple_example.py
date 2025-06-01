#!/usr/bin/env python3
"""
Simple ElevenLabs API Example

This is a minimal example showing the basic usage pattern you requested.
"""

import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

# Initialize ElevenLabs client
elevenlabs = ElevenLabs(
    api_key=os.getenv('ELEVENLABS_API_KEY', 'YOUR_API_KEY'),
)

def simple_text_to_speech():
    """
    Simple text-to-speech example
    """
    # Text to convert to speech
    text = "Hello! This is a simple example of using ElevenLabs API in Python."
    
    # Generate audio
    audio = elevenlabs.generate(
        text=text,
        voice="Rachel",  # You can use voice name or voice_id
        model="eleven_monolingual_v1"
    )
    
    # Save the audio to file
    save(audio, "simple_output.mp3")
    print("Audio saved to simple_output.mp3")
    
    # Play the audio
    play(audio)
    print("Playing audio...")

def list_available_voices():
    """
    List all available voices
    """
    voices = elevenlabs.voices.get_all()
    
    print("Available voices:")
    for voice in voices.voices:
        print(f"- {voice.name} (ID: {voice.voice_id})")

if __name__ == "__main__":
    print("🎤 Simple ElevenLabs Demo")
    print("-" * 30)
    
    # List voices
    list_available_voices()
    
    print()
    
    # Generate speech
    simple_text_to_speech()
    
    print("\n✅ Demo completed!")
