#!/usr/bin/env python3
"""
ElevenLabs API Python Demo

This demo showcases various features of the ElevenLabs Text-to-Speech API:
- Basic text-to-speech conversion
- Voice listing and selection
- Audio streaming
- Voice settings customization
- Model selection

Requirements:
- elevenlabs Python package
- API key from ElevenLabs

Author: Demo
Date: 2025
"""

import os
import io
from pathlib import Path
from typing import List, Optional

from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play, stream, save


class ElevenLabsDemo:
    """ElevenLabs API demonstration class"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ElevenLabs client
        
        Args:
            api_key: ElevenLabs API key. If None, will try to get from environment variable
        """
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set ELEVENLABS_API_KEY environment variable or pass api_key parameter")
        
        self.client = ElevenLabs(api_key=self.api_key)
        
    def list_voices(self) -> List[Voice]:
        """
        Get all available voices
        
        Returns:
            List of Voice objects
        """
        print("📋 获取可用语音列表...")
        voices = self.client.voices.get_all()
        
        print(f"\n找到 {len(voices.voices)} 个可用语音:")
        print("-" * 50)
        
        for voice in voices.voices:
            print(f"🗣️  {voice.name}")
            print(f"   ID: {voice.voice_id}")
            print(f"   类别: {voice.category}")
            print(f"   描述: {voice.description or 'N/A'}")
            print()
        
        return voices.voices
    
    def basic_tts(self, text: str, voice_name: str = "Rachel", output_file: str = "output.mp3"):
        """
        Basic text-to-speech conversion
        
        Args:
            text: Text to convert to speech
            voice_name: Name of the voice to use
            output_file: Output audio file path
        """
        print(f"🔊 基础文本转语音: '{text[:50]}...'")
        print(f"📢 使用语音: {voice_name}")
        
        try:
            # Generate speech
            audio = self.client.generate(
                text=text,
                voice=Voice(name=voice_name),
                model="eleven_monolingual_v1"
            )
            
            # Save to file
            save(audio, output_file)
            print(f"✅ 音频已保存到: {output_file}")
            
            # Play the audio (optional)
            print("🎵 播放音频...")
            play(audio)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def advanced_tts_with_settings(self, 
                                 text: str, 
                                 voice_id: str,
                                 stability: float = 0.5,
                                 similarity_boost: float = 0.5,
                                 style: float = 0.0,
                                 use_speaker_boost: bool = True,
                                 output_file: str = "advanced_output.mp3"):
        """
        Advanced text-to-speech with custom voice settings
        
        Args:
            text: Text to convert
            voice_id: Voice ID to use
            stability: Voice stability (0.0-1.0)
            similarity_boost: Similarity boost (0.0-1.0)
            style: Style exaggeration (0.0-1.0)
            use_speaker_boost: Whether to use speaker boost
            output_file: Output file path
        """
        print(f"🎛️  高级文本转语音设置:")
        print(f"   稳定性: {stability}")
        print(f"   相似度增强: {similarity_boost}")
        print(f"   风格: {style}")
        print(f"   扬声器增强: {use_speaker_boost}")
        
        try:
            # Create voice with custom settings
            voice = Voice(
                voice_id=voice_id,
                settings=VoiceSettings(
                    stability=stability,
                    similarity_boost=similarity_boost,
                    style=style,
                    use_speaker_boost=use_speaker_boost
                )
            )
            
            # Generate speech with advanced settings
            audio = self.client.generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2"  # Using multilingual model
            )
            
            # Save and play
            save(audio, output_file)
            print(f"✅ 高级音频已保存到: {output_file}")
            play(audio)
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def streaming_tts(self, text: str, voice_name: str = "Rachel"):
        """
        Streaming text-to-speech for real-time playback
        
        Args:
            text: Text to convert
            voice_name: Voice name to use
        """
        print(f"🌊 流式文本转语音: '{text[:50]}...'")
        print("🎵 实时播放中...")
        
        try:
            # Generate and stream audio
            audio_stream = self.client.generate(
                text=text,
                voice=Voice(name=voice_name),
                model="eleven_turbo_v2",  # Faster model for streaming
                stream=True
            )
            
            # Stream and play in real-time
            stream(audio_stream)
            print("✅ 流式播放完成")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    def get_voice_by_name(self, voice_name: str) -> Optional[Voice]:
        """
        Get voice object by name
        
        Args:
            voice_name: Name of the voice
            
        Returns:
            Voice object if found, None otherwise
        """
        voices = self.client.voices.get_all()
        for voice in voices.voices:
            if voice.name.lower() == voice_name.lower():
                return voice
        return None
    
    def demo_multiple_voices(self, text: str = "Hello, this is a voice demonstration."):
        """
        Demonstrate multiple voices with the same text
        
        Args:
            text: Text to speak with different voices
        """
        print(f"🎭 多语音演示: '{text}'")
        
        # Common voice names (these might vary based on your subscription)
        demo_voices = ["Rachel", "Drew", "Clyde", "Paul"]
        
        for i, voice_name in enumerate(demo_voices, 1):
            print(f"\n🗣️  语音 {i}: {voice_name}")
            try:
                audio = self.client.generate(
                    text=text,
                    voice=Voice(name=voice_name),
                    model="eleven_monolingual_v1"
                )
                
                output_file = f"demo_voice_{i}_{voice_name.lower()}.mp3"
                save(audio, output_file)
                print(f"   💾 保存到: {output_file}")
                
                # Optional: play each voice (uncomment to hear)
                # play(audio)
                # time.sleep(1)  # Small delay between voices
                
            except Exception as e:
                print(f"   ❌ 语音 {voice_name} 失败: {e}")


def main():
    """
    Main demonstration function
    """
    print("🎬 ElevenLabs API Python Demo")
    print("=" * 40)
    
    try:
        # Initialize the demo class
        demo = ElevenLabsDemo()
        
        # Demo 1: List available voices
        print("\n1️⃣  演示：列出可用语音")
        voices = demo.list_voices()
        
        # Demo 2: Basic TTS
        print("\n2️⃣  演示：基础文本转语音")
        demo.basic_tts(
            text="Hello! This is a demonstration of ElevenLabs text-to-speech API. The quality is quite impressive!",
            voice_name="Rachel",
            output_file="demo_basic.mp3"
        )
        
        # Demo 3: Advanced TTS with custom settings
        if voices:
            print("\n3️⃣  演示：高级设置文本转语音")
            first_voice = voices[0]
            demo.advanced_tts_with_settings(
                text="This is an advanced example with custom voice settings. Notice the difference in tone and style.",
                voice_id=first_voice.voice_id,
                stability=0.7,
                similarity_boost=0.8,
                style=0.2,
                output_file="demo_advanced.mp3"
            )
        
        # Demo 4: Streaming TTS
        print("\n4️⃣  演示：流式文本转语音")
        demo.streaming_tts(
            text="This is a streaming example. The audio should play in real-time as it's being generated.",
            voice_name="Rachel"
        )
        
        # Demo 5: Multiple voices comparison
        print("\n5️⃣  演示：多语音对比")
        demo.demo_multiple_voices(
            text="This is the same text spoken by different voices for comparison."
        )
        
        print("\n🎉 所有演示完成！")
        print("📁 检查当前目录中生成的音频文件")
        
    except ValueError as e:
        print(f"❌ 配置错误: {e}")
        print("\n🔧 设置说明:")
        print("1. 获取 ElevenLabs API 密钥: https://elevenlabs.io/")
        print("2. 设置环境变量: export ELEVENLABS_API_KEY='your_api_key'")
        print("3. 或者在代码中直接传入 api_key 参数")
        
    except Exception as e:
        print(f"❌ 意外错误: {e}")


if __name__ == "__main__":
    main()
