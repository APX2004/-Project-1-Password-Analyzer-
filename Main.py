import argparse
import time
from checker import evaluate_password, load_common_passwords, hash_password

def main():
    parser = argparse.ArgumentParser(
        description="Advanced Password Analyzer - Real Attacker Simulation"
    )

    parser.add_argument("--password", type=str, help="Password to analyze")
    parser.add_argument("--batch", type=str, help="File with multiple passwords")
    parser.add_argument("--hash", action="store_true", help="Display SHA-256 hash")

    args = parser.parse_args()
    common_passwords = load_common_passwords()

    if args.password:
        analyze(args.password, common_passwords, args.hash)

    elif args.batch:
        try:
            with open(args.batch, "r") as file:
                for line in file:
                    analyze(line.strip(), common_passwords, args.hash)
        except FileNotFoundError:
            print("Batch file not found.")

    else:
        print("Provide --password or --batch")

def analyze(password, common_passwords, show_hash=False):
    start = time.time()

    result = evaluate_password(password, common_passwords)

    end = time.time()

    print("\n===== Analysis Result =====")
    print(f"Password: {password}")
    print(f"Score: {result['score']}/100")
    print(f"Strength: {result['strength']}")
    print(f"Entropy: {result['entropy']} bits")
    print(f"Estimated Crack Time: {result['crack_time']}")

    if show_hash:
        print(f"SHA-256 Hash: {hash_password(password)}")

    print("\nSuggestions:")
    if result["suggestions"]:
        for s in result["suggestions"]:
            print("-", s)
    else:
        print("No improvements needed.")

    print(f"\nAnalysis completed in {round(end-start,4)} seconds\n")

if __name__ == "__main__":
    main()
