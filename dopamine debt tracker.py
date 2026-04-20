import datetime  # Basic module for dates (built-in, no install needed)
import os        # Basic module for file checking (built-in)

def get_user_inputs():
    """Get daily inputs from user using input()."""
    print("=== Daily Dopamine Debt Tracker ===")
    distraction = float(input("Enter today's distraction time (minutes): "))
    productive = float(input("Enter today's productive/study time (minutes): "))
    sleep = float(input("Enter today's sleep hours: "))
    return distraction, productive, sleep

def calculate_score(distraction, productive, sleep):
    """Calculate Dopamine Debt Score using simple math."""
    score = (distraction * 1.5) - (productive * 1.2)
    if sleep < 6:
        score += 15  # Penalty for low sleep
    return score

def get_status(score):
    """Return status message based on score using if-else."""
    if score < 0:
        return "Balanced Day"
    elif 0 <= score <= 30:
        return "Overstimulated Day"
    else:
        return "High Dopamine Debt"

def log_data(score, distraction, productive, sleep):
    """Save data to a simple CSV file using basic file handling."""
    filename = "dopamine_log.csv"
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Check if file exists, if not create header
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write("Date,Distraction,Productive,Sleep,Score\n")
    
    # Append today's data
    with open(filename, 'a') as f:
        f.write(f"{today},{distraction},{productive},{sleep},{score:.2f}\n")
    print(f"Data logged to {filename}")

def show_last_entries():
    """Display last 3 entries from the log file using basic file reading."""
    filename = "dopamine_log.csv"
    if not os.path.exists(filename):
        print("No previous data yet. First entry will be logged now!")
        return
    
    entries = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Skip header, take last 3 data lines
        for line in lines[-4:][1:]:  # Last 3, skip header if present
            entries.append(line.strip())
    
    print("\n=== Last Entries ===")
    for entry in entries[-3:]:  # Ensure max 3
        print(entry)

def main():
    """Main function to run the tracker."""
    distraction, productive, sleep = get_user_inputs()
    score = calculate_score(distraction, productive, sleep)
    status = get_status(score)
    
    print(f"\nYour Dopamine Debt Score: {score:.2f}")
    print(f"Status: {status}")
    
    if score > 30:
        print("Bonus Tip: Take a break! Go for a walk or meditate.")
    
    log_data(score, distraction, productive, sleep)
    show_last_entries()
    print("\nThanks for tracking! Run again tomorrow.")

# Run the program
if __name__ == "__main__":
    main()
