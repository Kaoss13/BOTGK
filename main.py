import os
import discord
import numpy as np
from discord.ext import commands
from sentence_transformers import SentenceTransformer, util


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


responses = [
    "Vous comprenez rien au jeu ", "TA GUEULE", "Je suis meilleur que vous",
    "Irl tu tiens pas les mêmes propos", "Tats pue la merde",
    "T'y connais rien", "T'es nul à chier", "Je me suis pas fait gap",
    "J'ai laissé Fley pour mort", "J'ai peak 550 lp", "Je monte quand je veux",
    "Vous comprenez pas le jeu", "Je suis meilleur que vous sur vos champions",
    "Je suis Félix Lebrun", "Crown merite le G tier", "Bon ftg",
    "Go reserver un dojo non?",
    "reste digne et ferme ta gueule si tu connais pas l'histoire",
    "Si tu utilises ton cerveau correctement ta mère explose?",
    "Dis que t'y connais rien sans dire que t'y connais rien belle perf. Puis nique ta mere la pute à me mentionner sale random. T'es un acad reste digne et parle pas du jeu",
    "après t'as vu je vais pas t'insulter ta grand mere pcq je suis gk gentil, mais essaye de lire le debut de la conv avant d'intervenir chef",
    "Me dis plus jamais que tu connais les limites de Viktor si tu veux pas je te retrouve irl",
    "Les gens détestable + nuls au jeu sont forcément détestables irl"
]


model = SentenceTransformer('all-MiniLM-L6-v2')


response_embeddings = model.encode(responses, convert_to_tensor=True)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        
        query_embedding = model.encode(message.content, convert_to_tensor=True)

        
        cos_scores = util.cos_sim(query_embedding, response_embeddings)[0]

       
        best_idx = int(np.argmax(cos_scores))
        chosen = responses[best_idx]

        await message.reply(chosen)

    
    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))
