import json
import discord
import numpy as np
from pathlib import Path
from discord.ext import commands

prefix = '?' #You can custom the command prefix

client = discord.Client()
client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

discordToken = "" #Copy your Discord Token here

baseJSON = {"Player": []}

fileHAUT = "HAUT.json"
fileObjHAUT = Path(fileHAUT)

if fileObjHAUT.is_file() == False:
    with open(fileHAUT, "w") as write_file:
        json.dump(baseJSON, write_file, indent = 2)
    write_file.close()

with open(fileHAUT, "r") as read_file:
        HAUT_dict = json.load(read_file)
        read_file.close()

emoteCouronne = 743800687749627936

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("Go faire des HAUT 1 !!!!"))
    print("Bot ready")

@client.command()
async def help(ctx):
    await ctx.send(f"Commandes disponible avec l'Automate calculateur de HAUT 1 :\n```{prefix}addPlayer @[Pseudo]``` Ajoute un joueur a la base de donnée\n```{prefix}leaderboard``` Te montre les plus gros BG de ce serveur\n```{prefix}add @[Pseudo]``` Ajoute un HAUT 1 au compteur du crack qui vient de gagner\n```{prefix}sub @[Pseudo]``` Enleve un HAUT 1\n```{prefix}nbHAUT @[Pseudo]``` Pour voir le nombre de HAUT 1")

@client.command()
async def addPlayer(ctx, membre: discord.Member):
    exisitingPlayer = False

    for idPlayer in HAUT_dict['Player']:
        if idPlayer['idDiscord'] == membre.id:
            exisitingPlayer = True
            break

    if exisitingPlayer == True:
        await ctx.send(f"{membre.name} a déjà etait ajouté à la base de donnée")
    else:
        HAUT_dict['Player'].append({"Name": membre.name,"idDiscord": membre.id,"HAUT": 0})

        await ctx.send(f"{membre.name} a été ajouté a la base de donnée des BG qui joue a TOMBER MEC")

        with open(fileHAUT, "w") as write_file:
            json.dump(HAUT_dict, write_file, indent = 2)
        write_file.close()

@addPlayer.error
async def on_command_error_addPlayer(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Tu dois faire: ```{prefix}addPlayer @[Pseudo]```")

@client.command()
async def nbHAUT(ctx, membre: discord.Member):

    for idPlayer in HAUT_dict['Player']:
        if idPlayer['idDiscord'] == membre.id:
            await ctx.send(f"{membre.name} Tu as fait {idPlayer['HAUT']} HAUT 1 <:couronne:{emoteCouronne}>.")

@addPlayer.error
async def on_command_error_nbHAUT(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Tu dois faire: ```{prefix}nbHAUT @[Pseudo]```")

@client.command()
async def sub(ctx, membre: discord.Member):
    exisitingPlayer = False

    for idPlayer in HAUT_dict['Player']:
        if idPlayer['idDiscord'] == membre.id:
            exisitingPlayer = True
            break

    if exisitingPlayer == True:
        if (idPlayer['HAUT'] == 0):
            await ctx.send(f"{membre.name} est déjà a 0 HAUT 1.")
        else:
            idPlayer['HAUT'] -= 1
            await ctx.send(f"Un HAUT 1 a été élevé à {membre.name}. Il as donc {idPlayer['HAUT']} HAUT 1.")

        with open(fileHAUT, "w") as write_file:
            json.dump(HAUT_dict, write_file, indent = 2)
        write_file.close()
    else:
        await ctx.send(f"{membre.name} n'est pas dans la base de donnée. Tu peux faire : ```{prefix}addPlayer @[Pseudo]``` pour l'ajouter")

@sub.error
async def on_command_error_sub(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Tu dois faire: ```{prefix}sub @[Pseudo]```")

@client.command()
async def add(ctx, membre: discord.Member):
    exisitingPlayer = False

    for idPlayer in HAUT_dict['Player']:
        if idPlayer['idDiscord'] == membre.id:
            exisitingPlayer = True
            break

    if exisitingPlayer == True:
        idPlayer['HAUT'] += 1
        if idPlayer['HAUT'] == 1:
            await ctx.send(f"{membre.name} n'avait aucun HAUT 1. BJ pour ton premier HAUT 1 <:couronne:{emoteCouronne}>.")
        else:
            await ctx.send(f"{membre.name} BJ pour ton {idPlayer['HAUT']} HAUT 1 <:couronne:{emoteCouronne}>.")

        with open(fileHAUT, "w") as write_file:
            json.dump(HAUT_dict, write_file, indent = 2)
        write_file.close()
    else:
        await ctx.send(f"{membre.name} n'est pas dans la base de donnée. Tu peux faire : ```{prefix}addPlayer @[Pseudo]``` pour l'ajouter")

@add.error
async def on_command_error_add(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Tu dois faire : ```{prefix}add @[Pseudo]```d")

@client.command()
async def leaderboard(ctx):

    nbPlayer = len(HAUT_dict['Player'])

    if(nbPlayer == 0):
        await ctx.send(f"Aucun joeur dans la base de donnée, vous pouvez faire : ```{prefix}addPlayer @[Pseudo]``` pour en ajouter")
    else:
        classement = np.zeros((2, nbPlayer), dtype=np.int64)

        x = 0
        for o in HAUT_dict['Player']:
            classement[0][x] = o['idDiscord']
            classement[1][x] = o['HAUT']
            x += 1

        for i in range(len(classement[0])):
            k = classement[1][i]
            h = classement[0][i]
            j = i-1
            while j >= 0 and k < classement[1][j] :
                    classement[1][j + 1] = classement[1][j]
                    classement[0][j + 1] = classement[0][j]
                    j -= 1
            classement[1][j + 1] = k
            classement[0][j + 1] = h

        classementComp = "Voici ceux avec LA MEILLEUR DNA DU SERVEUR :\n"

        HAUTMOINS1 = 0
        x = 1
        for u in range(nbPlayer - 1, -1, -1):
            for idPlayer in HAUT_dict['Player']:
                if classement[0][u] == idPlayer['idDiscord']:
                    classementComp = classementComp + f"{x} : {idPlayer['Name']} avec {idPlayer['HAUT']} HAUT 1\n"
                    if HAUTMOINS1 == classement[1][u]:
                        HAUTMOINS1 = classement[1][u]
                    else:
                        x += 1

        await ctx.send(f"{classementComp}")

client.run(discordToken)
