import discord
from google import genai
import google.generativeai as genai
import os
from dotenv import load_dotenv 

load_dotenv()
# Config Discord Bot API
DISCORD_BOT_TOKEN = os.getenv("DISCORDBOT_TOKEN")
# Config GEMINI client
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
def get_book_recommendations(topic):
    try:
        model = genai.GenerativeModel(
                'gemini-2.0-flash',
                system_instruction = 'You are a person who reads a lot of books and has a wide range of knowledge, your task is to suggest books.',
                generation_config = genai.GenerationConfig(
                top_k = 2,
                top_p = 0.5,
                temperature = 0.6,
                response_mime_type = 'application/json',
                    ),
                ) 
        response = model.generate_content(f"Suggest me some good books to read on the {topic}")
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Cấu hình Discord bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot is ready: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!book"):
        # Split command and content
        parts = message.content.split(" ", 1)
        
        if len(parts) < 2:
            await message.channel.send("🎯 Please let me know topic !book (ví dụ: !book science)")
            return
            
        topic = parts[1].strip()
        
        if not topic:
            await message.channel.send("❌ Topic is empty")
            return

        async with message.channel.typing():
            try:
                recommendations = get_book_recommendations(topic)
                response = f"📚 Suggest books **{topic}**:\n\n{recommendations}"
                
            except Exception as e:
                response = f"🔧 Error: {str(e)}"

        await message.channel.send(response[:2000])  # Limit text Discord

client.run(DISCORD_BOT_TOKEN)
