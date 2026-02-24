def classify_intent(user_input):
    text = user_input.lower()

    if "how long" in text or "when" in text or "time" in text:
        return "resolution_time"
    elif "reopen" in text or "open again" in text or "closed ticket" in text:
        return "reopen_ticket"
    elif "vpn" in text or "internet" in text:
        return "network_issue"
    elif "laptop" in text or "computer" in text:
        return "hardware_issue"
    elif "password" in text or "access" in text:
        return "access_issue"
    else:
        return "unknown"


def bot_reply(intent):
    if intent == "resolution_time":
        return (
            "⏱️ Resolution time depends on the issue:\n"
            "- Password reset: 5–15 minutes\n"
            "- VPN / Network: 30 minutes – 2 hours\n"
            "- Software issue: Up to 24 hours\n"
            "- Hardware issue: 1–3 business days"
        )
    elif intent == "reopen_ticket":
        return (
            "To reopen your ticket:\n"
            "1. Go to the Service Desk portal\n"
            "2. Click 'My Tickets'\n"
            "3. Select the resolved ticket\n"
            "4. Click 'Reopen' or add a comment"
        )
    elif intent == "network_issue":
        return (
            "It looks like a network/VPN issue.\n"
            "Try this first:\n"
            "1. Restart your laptop\n"
            "2. Reconnect VPN\n"
            "3. Check your internet connection"
        )
    elif intent == "hardware_issue":
        return (
            "This sounds like a hardware issue.\n"
            "Please confirm:\n"
            "- Is your laptop not powering on?\n"
            "- Any error lights or beeps?"
        )
    elif intent == "access_issue":
        return (
            "For access/password issues:\n"
            "1. Try password reset portal\n"
            "2. If locked out, I can create a ticket for IT"
        )
    else:
        return "Can you describe your issue in a bit more detail?"


def main():
    print("🤖 Service Desk AI Bot (Type 'exit' to quit)")
    print("----------------------------------------")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye! 👋")
            break

        intent = classify_intent(user_input)
        reply = bot_reply(intent)

        print("\nBot:", reply)


if __name__ == "__main__":
    main()
