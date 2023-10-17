import discord

intents = discord.Intents.default()
intents.members = True  # Enable member events (join, leave server, role changes, etc.)
intents.presences = True  # Enable presence events (user activity, like joining/leaving voice channels)

client = discord.Client(intents=intents)
token = "your token here"

@client.event
async def on_ready():
    print(f'Bot connected as {client.user.name}')

@client.event
async def on_member_join(member):
    registration_channel = discord.utils.get(member.guild.channels, name="registration")  # Change the channel name as per your needs

    if registration_channel:
        message = f"**{member.display_name}** has joined the server."
        await registration_channel.send(message)

@client.event
async def on_member_remove(member):
    registration_channel = discord.utils.get(member.guild.channels, name="registration")  # Change the channel name as per your needs

    if registration_channel:
        message = f"**{member.display_name}** has left the server."
        await registration_channel.send(message)

@client.event
async def on_member_update(before, after):
    # Check if member's roles (privileges) are changed
    if before.roles != after.roles:
        role_registration_channel = discord.utils.get(after.guild.channels, name="role_registration")  # Change the channel name as per your needs

        if role_registration_channel:
            previous_roles = [role.name for role in before.roles]
            current_roles = [role.name for role in after.roles]

            added_roles = set(current_roles) - set(previous_roles)
            removed_roles = set(previous_roles) - set(current_roles)

            message = f"**{after.display_name}** has had role changes:\n"
            if added_roles:
                message += f"Added Roles: {', '.join(added_roles)}\n"
            if removed_roles:
                message += f"Removed Roles: {', '.join(removed_roles)}"

            await role_registration_channel.send(message)

@client.event
async def on_voice_state_update(member, before, after):
    # Check if someone enters or leaves a voice channel
    if before.channel != after.channel:
        voice_channel_registration = discord.utils.get(member.guild.channels, name="voice_channel_registration")  # Change the channel name as per your needs

        if voice_channel_registration:
            if after.channel:
                message = f"**{member.display_name}** entered the voice channel **{after.channel.name}**."
            else:
                message = f"**{member.display_name}** left the voice channel."

            await voice_channel_registration.send(message)

client.run(token)
