"""
Main entry point for prototype experiments.
Use this file to quickly test new concepts and ideas.
"""

def main():
    """
    Entry point for experimental code.
    Replace this with your experiment code.
    """
    print("Project Janus - Prototype Experiment")
    print("Replace this with your experimental code")
    
    # Example: Test a simple choice scenario
    test_simple_choice()

def test_simple_choice():
    """
    Simple test of choice-based psychological assessment.
    """
    print("\n--- Simple Choice Test ---")
    print("You find a wallet on the ground with money visible.")
    print("What do you do?")
    print("1. Take it to the police")
    print("2. Look for ID and try to return it directly")
    print("3. Take the money and leave the wallet")
    print("4. Leave it where it is")
    
    choice = input("Enter your choice (1-4): ")
    
    # Simple psychological scoring example
    psychological_scores = {
        "1": {"conscientiousness": 0.8, "agreeableness": 0.7},
        "2": {"conscientiousness": 0.9, "agreeableness": 0.9, "openness": 0.6},
        "3": {"conscientiousness": -0.8, "agreeableness": -0.9},
        "4": {"conscientiousness": 0.1, "agreeableness": 0.1}
    }
    
    if choice in psychological_scores:
        scores = psychological_scores[choice]
        print(f"\nPsychological indicators: {scores}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
