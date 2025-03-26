import pyautogui
import time

def send_love_messages(message="I love you! ❤️", count=50):
    """
    Sends a repeated message on WhatsApp Web
    Assumes WhatsApp Web is already open and the chat is selected
    
    Args:
        message: The message to send
        count: Number of messages to send (default: 50)
    """
    # Give the user time to click on the WhatsApp Web chat
    print("You have 5 seconds to click on the WhatsApp chat input box...")
    time.sleep(5)
    
    # Send messages
    for i in range(count):
        # Type the message
        pyautogui.typewrite(message)
        
        # Press Enter to send
        pyautogui.press('enter')
        
        # Print status
        print(f"Message {i+1}/{count} sent: {message}")
        
        # Small delay between messages
        time.sleep(0.5)
    
    print("All done! All your love messages have been sent!")

if __name__ == "__main__":
    # Change these variables to your preferences
    love_message = "I love you! ❤️"
    message_count = 50
    
    # Run the function
    send_love_messages(love_message, message_count)