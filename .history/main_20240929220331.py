
import argparse
from dotenv import load_dotenv
from alfred_chain import create_alfred_chain
import sys

def main():
    load_dotenv()
    
    alfred_chain = create_alfred_chain()
    
    print("Good day, I'm Alfred. How may I be of assistance with your wardrobe today?")
    print("(You may ask for outfit recommendations for any location, or type 'exit' to end our conversation.)")

    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nAlfred: Very well. Do have a splendid day, and don't hesitate to call on me if you need further assistance.")
            sys.exit(0)
        
        if not user_input:
            print("\nAlfred: I beg your pardon, but I didn't quite catch that. Could you please repeat your request?")
            continue
        
        try:
            response = alfred_chain(user_input)
            print(f"\nAlfred: {response}")
        except Exception as e:
            print(f"\nAlfred: I do apologize, but I seem to be having some difficulty processing that request. Perhaps we could try again?")
            print(f"(Error details: {str(e)})")

        print("\nAlfred: Is there anything else I can help you with today?")

if __name__ == "__main__":
    main()