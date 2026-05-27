"""
Friday AI — Command-Line Interface
Run the AI assistant directly from your terminal!

Usage:
    python cli.py                    # Start interactive CLI mode
    python cli.py "your command"     # Execute single command and exit
    python cli.py --voice            # Start voice interaction mode
"""

import sys
import argparse
from backend.core.nlp_engine import classify_intent
from backend.core.task_executor import execute_task
from backend.core.inference import InferencePipeline


class FridayCLI:
    def __init__(self):
        self.inference = InferencePipeline()
        self.history = []
        self.running = True

    def process_command(self, user_input: str) -> str:
        """
        Process a user command:
        1. Classify intent
        2. Execute action or route to local LLM
        3. Return response
        """
        if not user_input.strip():
            return ""

        # Classify the intent
        intent, entity = classify_intent(user_input)
        
        # Try to execute as an action first
        action_response = execute_task(intent, entity, raw_command=user_input)
        
        if action_response:
            response = action_response
        else:
            # Route to local LLM inference (no HTTP needed)
            response = self.ask_friday_local(user_input)
        
        # Add to history for context
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": response})
        
        # Keep history to last 10 exchanges (avoid memory bloat)
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        return response

    def ask_friday_local(self, message: str) -> str:
        """Use local inference pipeline directly (no HTTP API needed)."""
        try:
            response_stream = self.inference.generate_stream(
                prompt=message,
                history=self.history
            )
            full_response = ""
            for chunk in response_stream:
                full_response += chunk
            return full_response.strip() or "I'm thinking... could you repeat that?"
        except Exception as e:
            return f"Error generating response: {e}"

    def interactive_mode(self):
        """Run interactive CLI chat loop."""
        print("\n" + "="*60)
        print("🤖 Friday AI Assistant - CLI Mode")
        print("="*60)
        print("Type 'help' for commands, 'exit' to quit\n")
        
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye", "goodbye", "stop"]:
                    print("\nFriday: Goodbye! Have a great day! 👋\n")
                    self.running = False
                    break
                
                if user_input.lower() == "help":
                    self.show_help()
                    continue
                
                if user_input.lower() == "clear":
                    self.history = []
                    print("Conversation history cleared.\n")
                    continue
                
                # Process the command
                print("\nFriday: ", end="", flush=True)
                response = self.process_command(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\nFriday: Interrupted. Goodbye! 👋\n")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    def single_command_mode(self, command: str):
        """Execute a single command and exit."""
        print("\n" + "="*60)
        print("🤖 Friday AI Assistant")
        print("="*60 + "\n")
        
        try:
            response = self.process_command(command)
            print(f"Friday: {response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
            sys.exit(1)

    def voice_mode(self):
        """Run voice-based interaction (uses speech_listener and tts_engine)."""
        from backend.core.task_executor import run_voice_loop
        try:
            run_voice_loop()
        except Exception as e:
            print(f"❌ Voice mode error: {e}")
            sys.exit(1)

    def show_help(self):
        """Show available commands and examples."""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                   FRIDAY COMMANDS                          ║
╚════════════════════════════════════════════════════════════╝

🔍 SEARCH:
  - "search for Python tutorials"
  - "google machine learning"
  - "what is quantum computing?"

🚀 APP CONTROL:
  - "open notepad"
  - "launch chrome"
  - "start visual studio code"

⚙️  SYSTEM:
  - "shutdown"
  - "restart"
  - "volume up"

💬 CHAT:
  - "tell me a joke"
  - "how are you today?"
  - "what's the weather like?"

📋 CLI COMMANDS:
  - help        → Show this help message
  - clear       → Clear conversation history
  - exit/quit   → Exit the application
  - bye/goodbye → Exit the application

"""
        print(help_text)


def main():
    parser = argparse.ArgumentParser(
        description="Friday AI Assistant - CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py                    # Start interactive mode
  python cli.py "search python"    # Single command
  python cli.py --voice            # Voice mode
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default=None,
        help="Single command to execute (optional)"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Start voice interaction mode (requires microphone)"
    )
    
    args = parser.parse_args()
    
    cli = FridayCLI()
    
    try:
        if args.voice:
            print("Starting voice mode...")
            cli.voice_mode()
        elif args.command:
            cli.single_command_mode(args.command)
        else:
            cli.interactive_mode()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
