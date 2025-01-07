import argparse

def main(name):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example Python Script")
    parser.add_argument("--name", required=True, help="Your name")
    args = parser.parse_args()
    main(args.name)
