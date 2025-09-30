import os, random, time, re
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
app = App(token=os.getenv("SLACK_BOT_TOKEN"), signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

import datetime

@app.command("/cutemsg")
def handle_cutemsg(ack, respond, command):
    ack()  # must ack immediately

    try:
        text = command.get("text", "").strip()
        parts = text.split()
        if len(parts) < 2:
            respond("You dumb ass mf don't you understand Usage: `/cutemsg @user 3 [hi, hello, hey]`")
            return
        
        invoker = f"<@{command['user_id']}>"  # person who used command
        target = parts[0]
        count = int(parts[1]) if parts[1].isdigit() else 1
        rest = " ".join(parts[2:])

        m = re.search(r"\[(.*?)\]", rest)
        if not m:
            respond("You dumb ass mf don't you understand Usage: `/cutemsg @user 3 [hi, hello, hey]`")
            return

        options = [s.strip() for s in m.group(1).split(",") if s.strip()]

        target_text = parts[0]  # what user typed after /cutemsg
        target_mention = target_text
        channel_id = None

        user_match = re.match(r"<@([A-Z0-9]+)>", target_text)
        if user_match:
            user_id = user_match.group(1)
            conv = app.client.conversations_open(users=user_id)
            channel_id = conv["channel"]["id"]
            target_mention = f"<@{user_id}>"
        else:
            users = app.client.users_list()
            found = False
            for u in users["members"]:
                if u.get("profile", {}).get("display_name") == target_text.strip("@") or \
                u.get("name") == target_text.strip("@"):
                    user_id = u["id"]
                    conv = app.client.conversations_open(users=user_id)
                    channel_id = conv["channel"]["id"]
                    target_mention = f"<@{user_id}>"
                    found = True
                    break
            if not found:
                channel_id = target_text

        logC = "C09FMPJGL7N"

        app.client.chat_postMessage(
    channel=command["channel_id"],
    text=f"{invoker} used the command on {target_mention} with count {count} messages!!!  (new)"
)



        # Send messages in a loop
        if count > 10:
            respond("DAMN YOU WANT TO SPAMMMMMM, FUCK YOU SPAMMER? You can't send more than 10 messages at once!")
            count = 10
        respond(" STARTED ( 3 seconds delay between messages )")
        for _ in range(count):
            chosen = random.choice(options)
            app.client.chat_postMessage(channel=channel_id, text=chosen)
            time.sleep(3)

        respond(f"Sent {count} messages to {target}")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        app.client.chat_postMessage(channel=logC, text=(f"Cutemsg snitch\n"
        f"criminal: {invoker}\n"
        f"victim: {target_mention}\n"
        f"count: {count}\n"
        f"time: {now}"))

# stats stuff


    except Exception as e:
        print("Error:", e)
        respond(f"Oops! Something went wrong. {e}")

if __name__ == "__main__":
    app_token = os.getenv("SLACK_APP_TOKEN")
    handler = SocketModeHandler(app, app_token)
    print("Cutemsg bot running in Socket Mode...")
    handler.start()

# nano ~/.config/systemd/user/cutelittle.service
