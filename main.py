import os
import requests
import random
import string
from bs4 import BeautifulSoup
import gzip
import shutil
from PIL import Image

import moondream as md

# --------------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------------
MODEL_DIR = "model"
MODEL_FILENAME_2B = "moondream-2b-int8.mf"
MODEL_FILENAME_05B = "moondream-0_5b-int8.mf"
MODEL_DOWNLOAD_URL_05B = (
    "https://huggingface.co/vikhyatk/moondream2/resolve/"
    "9dddae84d54db4ac56fe37817aeaeb502ed083e2/moondream-0_5b-int8.mf.gz?download=true"
)

# --------------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------------
def generate_random_code(length=11):
    """Generate a random code of given length, consisting of letters and digits."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def get_image_url_from_prntsc(code):
    """
    Given a prnt.sc code, retrieve the page and parse out the image URL 
    from the 'og:image' meta property if it exists.
    """
    url = f"https://prnt.sc/{code}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        )
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag = soup.find("meta", property="og:image")
        if not meta_tag:
            return None
        
        image_url = meta_tag.get("content")
        # Skip default/placeholder images
        if "st.prntscr.com" in image_url:
            return None
        
        return image_url
    
    except requests.RequestException:
        return None

def download_image(image_url, filename):
    """
    Download and save an image from `image_url` to `filename`.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(image_url, headers=headers, stream=True)
    if resp.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

def analyze_image_with_moondream(image_path, model):
    """
    Use the moondream model to generate a caption and answer a question 
    about the image at `image_path`.
    """
    try:
        image = Image.open(image_path)
        encoded_image = model.encode_image(image)
        
        # Generate caption
        caption = model.caption(encoded_image)["caption"]
        
        # Ask question
        answer = model.query(encoded_image, "What's in this image?")["answer"]
        
        print(f"Caption: {caption}")
        print(f"Answer:  {answer}")
        
    except Exception as e:
        print(f"Failed to analyze image with moondream. Error: {e}")

def download_and_unzip_model(url, output_path):
    """
    Download a GZ file from `url` and decompress it to `output_path`.
    Returns True if successful, False otherwise.
    """
    tmp_gz_path = output_path + ".gz"

    try:
        print(f"Downloading model from: {url}")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(tmp_gz_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("Download complete. Unzipping...")
        with gzip.open(tmp_gz_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove the gz file after extraction
        os.remove(tmp_gz_path)

        print(f"Model unzipped to: {output_path}")
        return True
    except Exception as e:
        print(f"Failed to download or unzip model. Error: {e}")
        return False

def get_or_download_model():
    """
    Check for moondream-2b-int8.mf or moondream-0_5b-int8.mf in MODEL_DIR.
    If both are missing, attempt to download moondream-0_5b-int8.mf.
    """
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_2b_path = os.path.join(MODEL_DIR, MODEL_FILENAME_2B)
    model_05b_path = os.path.join(MODEL_DIR, MODEL_FILENAME_05B)

    # Priority: moondream-2b-int8.mf
    if os.path.exists(model_2b_path):
        print(f"Found {MODEL_FILENAME_2B}. Using that model.")
        return model_2b_path
    # Next check for moondream-0_5b-int8.mf
    elif os.path.exists(model_05b_path):
        print(f"{MODEL_FILENAME_2B} not found, but {MODEL_FILENAME_05B} is present. Using that model.")
        return model_05b_path
    else:
        # Neither model is found. Attempt to download moondream-0_5b-int8.mf
        print(f"Neither {MODEL_FILENAME_2B} nor {MODEL_FILENAME_05B} found in '{MODEL_DIR}'.")
        print("Attempting to download moondream-0_5b-int8.mf from Hugging Face...")
        success = download_and_unzip_model(MODEL_DOWNLOAD_URL_05B, model_05b_path)
        if success and os.path.exists(model_05b_path):
            return model_05b_path
        else:
            print(
                "Automatic download failed. Please download moondream-2b-int8.mf or "
                "moondream-0_5b-int8.mf manually and place it in the 'model' folder."
            )
            return None

# --------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------
def main(num_checks=10000):
    """
    Attempt `num_checks` random prnt.sc URLs. For each valid image found:
      - Download it to a 'downloads' folder
      - Analyze it with moondream
    """

    # 1. Get the path to the model or attempt to download
    model_path = get_or_download_model()
    if not model_path or not os.path.exists(model_path):
        print("No valid model found. Exiting.")
        return

    # 2. Load the moondream model
    print(f"Initializing moondream model: {model_path}")
    model = md.vl(model=model_path)

    # 3. Ensure there's a downloads folder
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    successful_downloads = 0
    
    for _ in range(num_checks):
        code = generate_random_code(11)
        print(f"Trying code: {code}")
        
        image_url = get_image_url_from_prntsc(code)
        if image_url:
            print(f"  Found image: {image_url}")
            filename = os.path.join("downloads", f"{code}.jpg")
            
            try:
                download_image(image_url, filename)
                successful_downloads += 1
                print(f"  -> Downloaded as {filename}")
                
                # Analyze the downloaded image
                analyze_image_with_moondream(filename, model)
                print("")
            except Exception as e:
                print(f"  -> Failed to download or analyze. Error: {e}\n")
        else:
            print("  -> No valid image found.\n")
    
    print(f"Completed {num_checks} checks. Downloaded {successful_downloads} images.")

if __name__ == "__main__":
    main(num_checks=10000)