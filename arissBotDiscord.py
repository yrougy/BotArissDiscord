# Pip install  discord.py
import sys
import os
import re
import requests
import html2text
import discord
from discord.ext import commands, tasks
import asyncio
from icalendar import Calendar
from datetime import datetime, timedelta, date
from pytz import UTC

#######################################################
# CONFIGURATION IS HERE
# id of the discord channel to send logs to
DiscordChannel = 1234 #  <Discord Channel id to post to>
# The API Key of the bot
BotKEY = 'API Key for the bot'
#
Mode = 'net' # local to not send to discord
Location = 'Europe' # FM over Europe only
# END OF CONFIGURATION
#######################################################


# Discord Bot initialization
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!',intents=intents)

Location = ' - FM over ' + Location

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await send_msg()

@client.event
async def send_msg():
    ics_url = 'https://calendar.google.com/calendar/ical/39fpkdtnqhma60vk5nd0ndur4o%40group.calendar.google.com/public/basic.ics'
    events = get_events_from_ics(ics_url)
    formatted_events = ret_upcoming_events(events)
    if not events:
        print("No event found.")
        channel = client.get_channel(DiscordChannel)
        await client.close()
        return

    print("Future events:")
    for event in events:
        start = event['start'].strftime('%d/%m/%Y')
        end = event['end'].strftime('%Y-%m-%d %H:%M:%S')
        summary = convert_html_to_markdown(event['summary'])
        content = convert_html_to_markdown(event['description'])
        msg=f"**Summary**:{summary}\n**Date**:{start}\n{content}"
        chunks = shorten_msg(msg)
        channel = client.get_channel(DiscordChannel)
        if channel:
          if Mode == 'local':
              print("🛰️  -- **Planned ARISS contact** -- 🛰️n\n\n")
          else:
                await channel.send("🛰️ -- **Planned ARISS contact** -- 🛰️\n\n")
          for i, chunk in enumerate(chunks):
            if Mode == 'local':
                print(chunk)
            else:
                await channel.send(chunk)
          if Mode == 'local':
              print("🛰️   -- EOT ------------\n\n")
          else:
            await channel.send("🛰️  -- EOT ------------\n\n")
        await client.close()


def shorten_msg(input_string, byte_limit=1900, encoding='utf-8'):
    # We have to cut the message in shorter messages to go to discord
    byte_chunks = []
    current_chunk = b''

    for char in input_string:
        char_bytes = char.encode(encoding)
        if len(current_chunk) + len(char_bytes) > byte_limit:
            byte_chunks.append(current_chunk.decode(encoding))
            current_chunk = b''
        current_chunk += char_bytes

    if current_chunk:
        byte_chunks.append(current_chunk.decode(encoding))

    return byte_chunks

def convert_html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0

    markdown_content = h.handle(html_content)
    return markdown_content


def get_events_from_ics(url):
    response = requests.get(url)
    response.raise_for_status()

    # ICS file analysis
    cal = Calendar.from_ical(response.content)

    # We keep track of the next 2 weeks (can be adapted)
    now = datetime.utcnow().replace(tzinfo=UTC)
    two_week_later = now + timedelta(days=14)

    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            event_start = component.get('dtstart').dt
            event_end = component.get('dtend')
            event_summary = component.get('summary')
            event_desc = component.get('description')
            # If dtend is None, we use dstart as dtend (on day event)
            if event_end is None:
                event_end = event_start
            else:
                event_end = event_end.dt

            # We check objects are datetime so we can compare them
            if isinstance(event_start, datetime):
                event_start = event_start
            elif isinstance(event_start, date):
                event_start = datetime.combine(event_start, datetime.min.time(), tzinfo=UTC)

            if isinstance(event_end, datetime):
                event_end = event_end
            elif isinstance(event_end, date):
                event_end = datetime.combine(event_end, datetime.min.time(), tzinfo=UTC)

            if now <= event_start <= two_week_later:
                #print(event_desc)
                if Location in event_desc:
                  events.append({
                      "start": event_start,
                      "end": event_end,
                      "summary": event_summary,
                      "description": event_desc
                  })
    return events

def ret_upcoming_events(events):
    if not events:
        print("Aucun événement à venir trouvé.")
        return

    print("Événements à venir:")
    for event in events:
        start = event['start'].strftime('%d/%m/%Y')
        end = event['end'].strftime('%Y-%m-%d %H:%M:%S')
        summary = event['summary']
        content = convert_html_to_markdown(event['description'])
        return(f"{start} - {end}: {summary}\n--\n {content}")

if __name__ == '__main__':
    client.run(BotKEY)



