# mirror_bounty.py
import subprocess
import sys

def mirror_bounty(bounty_url):
    try:
        # Install the thirtyoneday package if not already installed
        subprocess.run(["pip", "install", "thirtyoneday"], check=True)

        # Mirror the bounty
        result = subprocess.run(["thirtyoneday", "mirror", bounty_url], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Bounty successfully mirrored: {bounty_url}")
            print(result.stdout)
        else:
            print(f"Failed to mirror bounty: {bounty_url}")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("Usage: python mirror_bounty.py <external_bounty_url>")
        sys.exit(1)

    bounty_url = sys.argv[1]
    mirror_bounty(bounty_url)
