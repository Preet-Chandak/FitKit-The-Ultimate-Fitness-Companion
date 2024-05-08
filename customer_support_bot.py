class CustomerSupportBot:
    def __init__(self):
        self.qna = {
            "how do i sign up?": "You can sign up by clicking on the 'Sign Up' button on our homepage.",
            "what are your payment options?": "We accept credit/debit cards and PayPal.",
            "how can i reset my password?": "You can reset your password by visiting the 'Forgot Password' page and following the instructions.",
            "do you offer a free trial?": "Yes, we offer a 7-day free trial for new users.",
            "how do i cancel my subscription?": "To cancel your subscription, log in to your account and navigate to the 'Subscription' section.",
            "can i change my subscription plan?": "Yes, you can upgrade or downgrade your subscription plan at any time in your account settings.",
            "where can i find your privacy policy?": "You can find our privacy policy on the 'Privacy Policy' page at the bottom of our website.",
            "what if i have more questions?": "Feel free to contact our customer support team at support@example.com.",
            "how do I track my steps?": "You can track your steps using the 'Step Tracker' feature on our app. Make sure to have the app open and your device's motion sensors enabled.",
            "can I sync my fitness data with other apps?": "Yes, you can sync your fitness data with popular apps like Apple Health, Google Fit, and Fitbit. Visit the 'Settings' section to set up the integration.",
            "how accurate is the heart rate monitor?": "Our heart rate monitor provides accurate readings, but keep in mind that factors like motion and positioning can affect the measurements.",
            "what exercises are good for weight loss?": "Cardiovascular exercises like running, cycling, and swimming are great for weight loss. Combine them with strength training for better results.",
            "how do I set fitness goals?": "You can set fitness goals in the 'Goals' section of the app. Choose your target, such as steps per day or distance covered, and track your progress.",
            "is there a community or group feature?": "Yes, you can join fitness groups and challenges in the 'Community' section. Connect with others, participate in challenges, and stay motivated together.",
            "how can I improve my sleep quality?": "Establish a consistent sleep schedule, create a relaxing bedtime routine, and avoid electronics before sleep. You can also track your sleep patterns using our app.",
            "what if I have technical issues with the app?": "If you encounter technical issues, you can troubleshoot by restarting the app, updating to the latest version, or contacting our support team for assistance.",
            "how often should I do strength training?": "For beginners, aim for at least 2-3 days of strength training per week. Allow your muscles to rest between sessions for optimal recovery.",
            "what's the best way to stay motivated?": "Setting realistic goals, tracking your progress, and finding an exercise routine you enjoy are key. You can also join challenges and engage with the fitness community.",
            "how do I connect my smartwatch to the app?": "To connect your smartwatch, open the 'Devices' section in the app, select your smartwatch model, and follow the pairing instructions provided.",
        }

    def respond(self, user_input):
        user_input_cleaned = user_input.lower().replace(" ", "").replace("?", "")
        for question in self.qna:
            question_cleaned = question.lower().replace(" ", "").replace("?", "")
            if user_input_cleaned == question_cleaned:
                return self.qna[question]
        
        return "I'm sorry, I don't have an answer to that question. You can contact our support team for assistance."

def main():
    print("Customer Support Bot: How can I assist you today?")
    bot = CustomerSupportBot()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Customer Support Bot: Thank you for using our customer support bot. Have a great day!")
            break

        response = bot.respond(user_input)
        print("Customer Support Bot:", response)

if __name__ == "__main__":
    main()
