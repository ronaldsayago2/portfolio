import os
import requests

# Create directories if they don't exist
pieces_dir = os.path.join('static', 'img', 'chesspieces', 'wikipedia')
os.makedirs(pieces_dir, exist_ok=True)

# List of all chess pieces
pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 
          'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

# base_url = "https://raw.githubusercontent.com/oakmac/chessboardjs/master/img/chesspieces/wikipedia/"
base_url = "https://github.com/oakmac/chessboardjs/tree/master/website/img/chesspieces/wikipedia/"


# Download each piece
for piece in pieces:
    filename = f"{piece}.png"
    url = base_url + filename
    filepath = os.path.join(pieces_dir, filename)
    
    print(f"Downloading {filename}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

print("\nDownload complete!")