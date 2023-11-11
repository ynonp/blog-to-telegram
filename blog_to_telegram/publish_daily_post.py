import requests
import telepot
import sys, os, re

def fix_code_blocks(list_of_messages):
    result = []
    next_prefix = ""

    for msg in list_of_messages:
        msg = next_prefix + msg
        next_prefix = ""

        if (nm := len(re.findall(r"```", msg, re.S))) % 2 == 0:
            result.append(msg + "\n")
        else:
            result.append(msg + "\n```\n")
            next_prefix = "```\n"

    return result

def fix_spaces(list_of_messages):
    return [s.strip() for s in list_of_messages]

def daily_post_url():
    response = requests.get(
        'https://www.tocode.co.il/blog',
        headers={'Accept': 'application/json'},
    )
    json_response = response.json()

    return json_response['blog']['posts'][0]['href']

def post_content(url):
    response = requests.get("https://www.tocode.co.il" + url + '.md')
    return response.text

def split_body_to_messages(body, max_length=4090):
    expression = r"^(.{1," + str(max_length - 20) + r"}(?:\n|$))"
    output = re.findall(expression, body, re.S|re.M)

    return fix_code_blocks(fix_spaces(output))

def to_markdown_v2(text):
    return re.sub(r'(?m)^#+\s*(.*)$', lambda m: f'* {m.group(1)} *', text)


if __name__ == "__main__":
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = daily_post_url()

    body = post_content(url)
    
    chat_id = "@tocodeil"
    bot = telepot.Bot(TELEGRAM_TOKEN)
    bot.sendMessage(chat_id, "https://www.tocode.co.il" + url, disable_web_page_preview=None)

    for msg in split_body_to_messages(to_markdown_v2(body), 4000):
        bot.sendMessage(chat_id, msg, parse_mode="MarkdownV2")

