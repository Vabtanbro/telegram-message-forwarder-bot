import os
import random
from time import sleep
from pyrogram import filters
from bot import LOG, app, advance_config, chats_data, from_chats, to_chats, \
                remove_strings, replace_string, sudo_users
from bot.helper.utils import get_formatted_chat

LOG.info("Welcome, this is the telegram-message-forwarder-bot. main routine...")

LOG.error('vab tan')
@app.on_message(filters.chat(from_chats) & filters.incoming)
def work(client, message):
    print("New Message")
    print(f"```From:{str(from_chats)} \nTo:{str(to_chats)} \nAdmin:{str(sudo_users)}```")
    caption = None
    msg = None
    if remove_strings:
      for string in remove_strings:
        if message.media and not message.poll:
          caption = message.caption.html.replace(string, replace_string)
        elif message.text:
          msg = message.text.html.replace(string, replace_string)
    if advance_config:
      try:
        for chat in chats_data[message.chat.id]:
          if caption:
            message.copy(chat, caption=caption)
          elif msg:
            app.send_message(chat, msg, parse_mode="html")
          else:
            message.copy(chat)
      except Exception as e:
        LOG.error(e)
    else:
      try:
        for chat in to_chats:
          if caption:
            message.copy(chat, caption=caption)
          elif msg:
            app.send_message(chat, msg)
          else:
            message.copy(chat)
      except Exception as e:
        LOG.error(e)



@app.on_message(filters.user(sudo_users) & filters.command(["fwdold", "forwardold"]), group=1)
def forward(app, message):
    if len(message.command) > 1:
      chat_id = get_formatted_chat(message.command[1], app)
      if chat_id:
        try:
          offset_id = 0
          limit = 0
          if len(message.command) > 2:
            limit = int(message.command[2])
          if len(message.command) > 3:
            offset_id = int(message.command[3])
          for msg in app.iter_history(chat_id, limit=limit, offset_id=offset_id):
            msg.copy(message.chat.id)
            sleep(random.randint(1, 10))
        except Exception as e:
          message.reply_text(f"```{e}```")
      else:
        reply = message.reply_text("```Invalid Chat Identifier. Give me a chat id, username or message link.```")
        sleep(5)
        reply.delete()
    else:
      reply = message.reply_text("```Invalid Command ! Use /fwd {ChatID} {limit} {FirstMessageID}```")
      sleep(20)
      reply.delete()




@app.on_message(filters.user(sudo_users) & filters.command(["add_toc", "newtochal"]), group=1)
def to_chat_add(app, message):
    if len(message.command) > 1:
      chat_id = get_formatted_chat(message.command[1], app)
      
      if chat_id:
        print("Chat Id:",chat_id)
        to_chats.append(chat_id)
        reply = message.reply_text(f"```Added User {message.command[1]}```")

        '''
        try:
          offset_id = 0
          limit = 0
          if len(message.command) > 2:
            limit = int(message.command[2])
          if len(message.command) > 3:
            offset_id = int(message.command[3])
          for msg in app.iter_history(chat_id, limit=limit, offset_id=offset_id):
            msg.copy(message.chat.id)
            sleep(random.randint(1, 10))
        except Exception as e:
          message.reply_text(f"```{e}```")'''
      else:
        reply = message.reply_text("```Invalid Chat Identifier. Give me a chat id, username or message link.```")
        sleep(5)
        reply.delete()
    else:
      reply = message.reply_text("```Invalid Command ! Use /fwd {ChatID} {limit} {FirstMessageID}```")
      sleep(20)
      reply.delete()


@app.on_message(filters.user(sudo_users) & filters.command(["add_fromc", "newfromchal"]), group=1)
def fromchat_add_fun(app, message):
    if len(message.command) > 1:
      chat_id = get_formatted_chat(message.command[1], app)
      
      if chat_id:
        print("Chat Id:",chat_id)
        from_chats.append(chat_id)
        reply = message.reply_text(f"```Added User {message.command[1]}```")

        '''
        try:
          offset_id = 0
          limit = 0
          if len(message.command) > 2:
            limit = int(message.command[2])
          if len(message.command) > 3:
            offset_id = int(message.command[3])
          for msg in app.iter_history(chat_id, limit=limit, offset_id=offset_id):
            msg.copy(message.chat.id)
            sleep(random.randint(1, 10))
        except Exception as e:
          message.reply_text(f"```{e}```")'''
      else:
        reply = message.reply_text("```Invalid Chat Identifier. Give me a chat id, username or message link.```")
        sleep(5)
        reply.delete()
    else:
      reply = message.reply_text("```Invalid Command ! Use /fwd {ChatID} {limit} {FirstMessageID}```")
      sleep(20)
      reply.delete()

@app.on_message(filters.user(sudo_users) & filters.command(["addu", "new_admin"]), group=1)
def admin_add_fun(app, message):
    if len(message.command) > 1:
      chat_id = get_formatted_chat(message.command[1], app)
      
      if chat_id:
        print("Chat Id:",chat_id)
        sudo_users.append(chat_id)
        print(sudo_users)
        reply = message.reply_text(f"```Added User {message.command[1]}```")

      else:
        reply = message.reply_text("```Invalid Chat Identifier. Give me a chat id, username or message link.```")
        sleep(5)
        reply.delete()
    else:
      reply = message.reply_text("```Invalid Command ! Use /fwd {ChatID} {limit} {FirstMessageID}```")
      sleep(20)
      reply.delete()
    
      
@app.on_message(filters.command(["myadmin", "addmin"]))
def adminfun(app, message):
    reply = message.reply_text(f"```From:{str(from_chats)} To:{str(to_chats)} Admin:{str(sudo_users)}```")


app.run()
