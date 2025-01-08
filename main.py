import discord
import asyncio
import os
import json
import random


d6msg_id = None
d12msg_id = None
d10msg_id = None
resultado_id = None
msg_user = None

# Carregar o token do arquivo config.json
with open('config.json', 'r') as f:
    config = json.load(f)
COR =0x690FC3
TOKEN = config.get("DISCORD_TOKEN")

# Definindo intents corretamente
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
# Criando o cliente com intents ativados
client = discord.Client(intents=intents)

def interpretar_resultado(valor):
    """Função para interpretar o resultado do dado para assimilação."""
    if valor in [1, 2]:
        return f"{valor} = Nada ❌"
    elif valor == 3:
        return f"{valor} = 1 Pressão 🦉"
    elif valor in [4, 5]:
        return f"{valor} = 1 Pressão 🦉 e 1 Adaptação 🫎"
    elif valor == 6:
        return f"{valor} = 1 Sucesso 🐞"
    elif valor == 7:
        return f"{valor} = 2 Sucessos 🐞🐞"
    elif valor == 8:
        return f"{valor} = 1 Sucesso 🐞 e 1 Adaptação 🫎"
    elif valor == 9:
        return f"{valor} = 1 Sucesso 🐞, 1 Adaptação 🫎 e 1 Pressão 🦉"
    elif valor == 10:
        return f"{valor} = 2 Sucessos 🐞🐞 e 1 Pressão 🦉"
    elif valor == 11:
        return f"{valor} = 1 Sucesso 🐞, 2 Adaptações 🫎🫎 e 1 Pressão 🦉"
    elif valor == 12:
        return f"{valor} = 2 Pressões 🦉🦉"
    else:
        return f"{valor} = Resultado inválido 🚫"


@client.event
async def on_ready():
    print('Bot Online - Olá Mundo! :3')
    print(client.user.name)
    print(client.user.id)
    print('--------------------------')

@client.event
async def on_message(message):
    global d6msg_id
    global d10msg_id
    global d12msg_id
    #global resultado_id
    if message.content == '?test':
        await message.channel.send('Ola mundo! estou vivo!')
    if message.content == '?dados':
        embed1 = discord.Embed(
            title="Dados D6",
            color=COR,
            description="- 1d6 = :one: \n"
                        "- 2d6  = :two: \n"
                        "- 3d6  = :three:\n"
                        "- 4d6  = :four: \n"
                        "- 5d6  = :five: \n", )

        embed2 = discord.Embed(
            title="Dados d10",
            color=COR,
            description="- 1d10 = :one: \n"
                        "- 2d10  = :two: \n"
                        "- 3d10  = :three:\n"
                        "- 4d10  = :four: \n"
                        "- 5d10  = :five: ", )

        embed3 = discord.Embed(
            title="Dados d12",
            color=COR,
            description="- 1d10 = :one: \n"
                        "- 2d10  = :two: \n"
                        "- 3d10  = :three:\n"
                        "- 4d10  = :four: \n"
                        "- 5d10  = :five: ", )

 #       embed4 = discord.Embed(
  #          title="Resultado",
   #         color=COR,
    #        description="Usuario rolou \n"
     #                   "D6: \n"
      #                  "D10: \n"
       #                 "D12: \n", )

    d12msg = await message.channel.send(embed=embed3)
    d6msg = await message.channel.send(embed=embed1)
    d10msg = await message.channel.send(embed=embed2)
   # resultado = await message.channel.send(embed=embed4)
    for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
        await d6msg.add_reaction(emoji)
    d6msg_id = d6msg.id

    await d10msg.add_reaction('1️⃣')
    await d10msg.add_reaction('2️⃣')
    await d10msg.add_reaction('3️⃣')
    await d10msg.add_reaction('4️⃣')
    await d10msg.add_reaction('5️⃣')
    d10msg_id = d10msg.id

    await d12msg.add_reaction('1️⃣')
    await d12msg.add_reaction('2️⃣')
    await d12msg.add_reaction('3️⃣')
    await d12msg.add_reaction('4️⃣')
    await d12msg.add_reaction('5️⃣')
    d12msg_id = d12msg.id

@client.event
async def on_reaction_add(reaction, user):
    global d6msg_id
    global d10msg_id
    global d12msg_id

    if user == client.user:
        return

    #### d6
    if reaction.message.id == d6msg_id:
        emoji_map = {
            '1️⃣': 1,
            '2️⃣': 2,
            '3️⃣': 3,
            '4️⃣': 4,
            '5️⃣': 5
        }
        if reaction.emoji in emoji_map:
            qtd_dados = emoji_map[reaction.emoji]
            resultados = [random.randint(1, 6) for _ in range(qtd_dados)]
            resultados_interpretados = [interpretar_resultado(valor) for valor in resultados]
            resultado_final = "\n".join(resultados_interpretados)

            # Atualizar a embed d6 adicionando o resultado
            embed_editada = discord.Embed(
                title="Dados D6",
                color=discord.Color.green(),
                description=(
                    "- 1d6 = :one: \n"
                    "- 2d6  = :two: \n"
                    "- 3d6  = :three:\n"
                    "- 4d6  = :four: \n"
                    "- 5d6  = :five: \n\n"
                    f"**{user.mention} rodou {qtd_dados}d6 e tirou:**\n{resultado_final}"
                )
            )
            await reaction.message.edit(embed=embed_editada)
            await reaction.message.remove_reaction(reaction.emoji, user)

      #### d10

    if reaction.message.id == d10msg_id:
        emoji_map = {
            '1️⃣': 1,
            '2️⃣': 2,
            '3️⃣': 3,
            '4️⃣': 4,
            '5️⃣': 5
        }
        if reaction.emoji in emoji_map:
            qtd_dados = emoji_map[reaction.emoji]
            resultados = [random.randint(1, 10) for _ in range(qtd_dados)]
            resultados_interpretados = [interpretar_resultado(valor) for valor in resultados]
            resultado_final = "\n".join(resultados_interpretados)

            # Atualizar a embed d10 adicionando o resultado
            embed_editada = discord.Embed(
                title="Dados D10",
                color=discord.Color.green(),
                description=(
                    "- 1d10 = :one: \n"
                    "- 2d10 = :two: \n"
                    "- 3d10 = :three:\n"
                    "- 4d10 = :four: \n"
                    "- 5d10 = :five: \n\n"
                    f"**{user.mention} rodou {qtd_dados}d10 e tirou:**\n{resultado_final}"
                )
            )
            await reaction.message.edit(embed=embed_editada)
            await reaction.message.remove_reaction(reaction.emoji, user)

    #### d12

    if reaction.message.id == d12msg_id:
        emoji_map = {
            '1️⃣': 1,
            '2️⃣': 2,
            '3️⃣': 3,
            '4️⃣': 4,
            '5️⃣': 5
        }
        if reaction.emoji in emoji_map:
            qtd_dados = emoji_map[reaction.emoji]
            resultados = [random.randint(1, 12) for _ in range(qtd_dados)]
            resultados_interpretados = [interpretar_resultado(valor) for valor in resultados]
            resultado_final = "\n".join(resultados_interpretados)

            # Atualizar a embed d12 adicionando o resultado
            embed_editada = discord.Embed(
                title="Dados D12",
                color=discord.Color.green(),
                description=(
                    "- 1d12 = :one: \n"
                    "- 2d12 = :two: \n"
                    "- 3d12 = :three:\n"
                    "- 4d12 = :four: \n"
                    "- 5d12 = :five: \n\n"
                    f"**{user.mention} rodou {qtd_dados}d12 e tirou:**\n{resultado_final}"
                )
            )
            await reaction.message.edit(embed=embed_editada)
            await reaction.message.remove_reaction(reaction.emoji, user)


client.run(TOKEN)
