import os
import telebot
import random
from time import sleep
from truth_dare_data import TRUTH_QUESTIONS, DARE_LIST

# Replace 'YOUR_BOT_TOKEN' with the token you got from BotFather
TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

# Enhanced 8ball responses
MAGIC_8BALL_RESPONSES = [
    "Absolutely! 🌟",
    "Without a doubt. ✨",
    "Yes, definitely! 💯",
    "You can count on it. 🔮",
    "Most likely. 👍",
    "The stars align for yes. 🌠",
    "Signs point to yes. 🎯",
    "Outlook is good. 🌈",
    "Reply hazy, try again. 🌫️",
    "Ask again later. ⏳",
    "Better not tell you now. 🤐",
    "Cannot predict now. 🤔",
    "My sources say no. 📚",
    "Very doubtful. ❌",
    "Chances are slim. 📉",
    "Negative. 🚫",
    "Absolutely not. 🛑",
    "Not in your wildest dreams. 😅",
    "Maybe in another universe. 🌌",
    "Keep dreaming. 💭",
    "The universe says no. 🌍",
    "Not happening. 🙅‍♀️"
]

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "Welcome to the FlipMaster Bot! by @AbuSalehT 🎲🎱\n\n"
        "Commands:\n"
        "/flip - Flip a coin\n"
        "/multiflip [number] - Flip multiple coins\n"
        "/8ball [question] - Ask the magic 8ball\n"
        "/truth - Get a truth question\n"
        "/dare - Get a dare challenge\n"
        "/help - Show this help message"
    )
    bot.reply_to(message, welcome_message)

# Command handler for /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = (
        "Available commands:\n"
        "/flip - Flip a coin\n"
        "/multiflip [number] - Flip multiple coins\n"
        "/8ball [question] - Ask the magic 8ball\n"
        "/truth - Get a truth question\n"
        "/dare - Get a dare challenge\n"
        "\nIn groups, you can also mention me with:\n"
        "@YourBotUsername flip\n"
        "@YourBotUsername 8ball [question]\n"
        "@YourBotUsername truth\n"
        "@YourBotUsername dare"
    )
    bot.reply_to(message, help_message)

# Enhanced Coin Flip Command
@bot.message_handler(commands=['flip'])
def flip_coin(message):
    # Coin flip animation messages
    animation_messages = [
        "🎲 Flipping the magical coin.."
    ]
    
    # Send initial animation message
    msg = bot.reply_to(message, random.choice(animation_messages))
    
    # Final coin result
    result = random.choice([
        "👑 Heads wins!",
        "🦁 Tails wins!"
    ])
    
    # Edit message with final result after a short delay
    sleep(1)
    bot.edit_message_text(result, 
                         chat_id=message.chat.id, 
                         message_id=msg.message_id)

# Enhanced Multi Flip Command
@bot.message_handler(commands=['multiflip'])
def multi_flip(message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 2:
            bot.reply_to(message, "🎲 Please specify the number of flips! Example: /multiflip 5")
            return
            
        num_flips = int(command_parts[1])
        
        if num_flips <= 0:
            bot.reply_to(message, "🚫 Please enter a positive number!")
            return
        elif num_flips > 100:
            bot.reply_to(message, "⚠️ Maximum 100 flips allowed at once!")
            return
            
        # Flip animation
        msg = bot.reply_to(message, f"🎲 Flipping {num_flips} magical coins...")
        sleep(1)
        
        # Perform the flips
        results = [random.choice(['Heads', 'Tails']) for _ in range(num_flips)]
        heads_count = results.count('Heads')
        tails_count = results.count('Tails')
        
        # Prepare a fun, colorful result message
        response = (
            f"🎯 Coin Flip Challenge Results 🌟\n\n"
            f"🔢 Total Flips: {num_flips}\n"
            f"👑 Heads: {heads_count} ({(heads_count/num_flips)*100:.1f}%)\n"
            f"🦁 Tails: {tails_count} ({(tails_count/num_flips)*100:.1f}%)\n\n"
            f"🏆 {'Heads' if heads_count > tails_count else 'Tails'} takes the lead!"
        )
        
        bot.edit_message_text(response, 
                            chat_id=message.chat.id, 
                            message_id=msg.message_id)
        
    except ValueError:
        bot.reply_to(message, "🚫 Please enter a valid number!")

# Enhanced 8Ball Command
@bot.message_handler(commands=['8ball'])
def magic_8ball(message):
    question = ' '.join(message.text.split()[1:])
    if not question:
        bot.reply_to(message, "🎱 Please ask a question! Example: /8ball Will I have a great day?")
        return
        
    # Send initial animation message
    msg = bot.reply_to(message, "🎱8ball is thinking...")
    
    # Simulate thinking with a delay
    sleep(1)
    
    # Select and display response
    response = random.choice(MAGIC_8BALL_RESPONSES)
    
    bot.edit_message_text(f"{response}", 
                         chat_id=message.chat.id, 
                         message_id=msg.message_id)

# Truth Command
@bot.message_handler(commands=['truth'])
def truth_command(message):
    # Get a random truth question
    truth_question = random.choice(TRUTH_QUESTIONS)
    
    # Send the truth question
    bot.reply_to(message, f"🤔 Truth Challenge:\n\n{truth_question}")

# Dare Command
@bot.message_handler(commands=['dare'])
def dare_command(message):
    # Get a random dare
    dare_challenge = random.choice(DARE_LIST)
    
    # Send the dare challenge
    bot.reply_to(message, f"🔥 Dare Challenge:\n\n{dare_challenge}")

# Handle mentions in groups
@bot.message_handler(func=lambda message: message.text and '@' in message.text)
def handle_mention(message):
    # Get bot's username
    bot_info = bot.get_me()
    bot_username = f"@{bot_info.username}"
    
    # Only process messages that mention the bot
    if bot_username.lower() not in message.text.lower():
        return
        
    # Extract command and text after mention
    text = message.text.lower().replace(bot_username.lower(), '').strip()
    
    if text.startswith('flip'):
        flip_coin(message)
    elif text.startswith('8ball'):
        message.text = f"/8ball {text[6:].strip()}"
        magic_8ball(message)
    elif text.startswith('truth'):
        truth_command(message)
    elif text.startswith('dare'):
        dare_command(message)
    else:
        bot.reply_to(message, "Try mentioning me with 'flip', '8ball [question]', 'truth', or 'dare'!")

# Start the bot
def main():
    print("Bot started...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
