import os, random, time, re
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()
app = App(token=os.getenv("SLACK_BOT_TOKEN"), signing_secret=os.getenv("SLACK_SIGNING_SECRET"))

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

        # extract message options
        m = re.search(r"\[(.*?)\]", rest)
        if not m:
            respond("You dumb ass mf don't you understand Usage: `/cutemsg @user 3 [hi, hello, hey]`")
            return

        options = [s.strip() for s in m.group(1).split(",") if s.strip()]

        # Determine channel_id
        channel_id = None

        # Check if user mention <@U12345>
        user_match = re.match(r"<@([A-Z0-9]+)>", target)
        if user_match:
            user_id = user_match.group(1)
            conv = app.client.conversations_open(users=user_id)
            channel_id = conv["channel"]["id"]

        # Check if channel mention <#C12345|name>
        elif re.match(r"<#(C[0-9A-Z]+)(?:\|[^>]+)?>", target):
            channel_id = re.match(r"<#(C[0-9A-Z]+)(?:\|[^>]+)?>", target).group(1)

        # Fallback: assume direct channel ID or name
        else:
            channel_id = target

        app.client.chat_postMessage(
            channel=command["channel_id"],
            text=f"{invoker} used the command on {target} with count {count} messages!!!  ( 3 seconds delay between messages )"
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

    except Exception as e:
        print("Error:", e)
        respond("Oops! Something went wrong.")

if __name__ == "__main__":
    print(f" Cutemsg bot running on port {os.environ.get('PORT', 3000)}")
    app.start(port=int(os.environ.get("PORT", 3000)))
nano ~/.config/systemd/user/cutelittle.service
