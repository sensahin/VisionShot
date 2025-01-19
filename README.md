# **VisionShot**  
_A Research Project Demonstrating the Ease of Public Screenshot Discovery and AI-based Image Analysis_


[![Demo](https://img.youtube.com/vi/xEsHRepfzks/0.jpg)](https://raw.githubusercontent.com/sensahin/Media/main/assets/0120.mov)


---

## **Overview**
VisionShot is a proof-of-concept (PoC) that illustrates how publicly accessible screenshots can be scraped from popular “share-a-screenshot” services (like [prnt.sc](https://prnt.sc)) and analyzed using modern, compact AI vision models. This project is purely educational—highlighting potential security and privacy risks in uploading sensitive screenshots to publicly indexed services without proper protective measures.

> **Disclaimer**:  
> This project is intended **only** for research and educational purposes. It demonstrates how easily public, non-secure screenshot hosting can be crawled and how those images can be automatically analyzed by AI. The author(s) assume no responsibility for any misuse or damages arising from the use of this tool. Use responsibly and in accordance with applicable laws.

---

## **Key Features**

1. **Random Screenshot Discovery**  
   - Automatically generates random links to [prnt.sc](https://prnt.sc)  
   - Attempts to retrieve and download any publicly available image.

2. **AI-based Image Analysis**  
   - Utilizes the [Moondream2](https://huggingface.co/vikhyatk/moondream2) image analysis model to generate a caption and answer questions about the content of each downloaded image.

3. **Automatic Model Setup**  
   - The program automatically checks for the required Moondream model files. If absent, it downloads and prepares the lightweight **moondream-0_5b-int8** model for immediate use.  

4. **Demonstrates Security Implications**  
   - Highlights the risk of sharing sensitive information on public screenshot services that do not enforce privacy or access control.

---

## **Table of Contents**
1. [Project Purpose](#project-purpose)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Example Output](#example-output)  
5. [Technical Explanation](#technical-explanation)  
6. [Recommended Precautions](#recommended-precautions)  
7. [License](#license)

---

## **Project Purpose**
- **Educational/Research Focus**: Show how trivial it can be to scrape publicly accessible content, and how easily modern AI models can extract detailed information from such images.  
- **Security Awareness**: Emphasize the importance of privacy, the risk of uploading sensitive data to unprotected or easily guessable links, and how these images may be discovered by malicious actors.  
- **AI Demonstration**: Illustrate how advanced vision-language models (like Moondream) have made image captioning and question-answering more accessible than ever, even on modest hardware.

---

## **Installation**

1. **Clone or Download this Repository**
    ```bash
    git clone https://github.com/sensahin/VisionShot.git
    cd VisionShot
    ```

2. **Create a Virtual Environment and Install Dependencies**
    ```bash
    python -m venv env
    source env/bin/activate  # For Windows, use: env\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Run the Program**
    ```bash
    python main.py
    ```

---

## **Usage**

- Upon first run, the program checks for the required **moondream-2b-int8.mf** or **moondream-0_5b-int8.mf** models in the `model/` folder.  
- If neither model exists, it automatically downloads and extracts the lightweight **moondream-0_5b-int8** model from [Hugging Face](https://huggingface.co/vikhyatk/moondream2).  
- Screenshots discovered from `prnt.sc` are downloaded to the `downloads/` folder and analyzed for captions and visual content.

---

## **Example Output**

**Sample Console Output:**
```plaintext
Trying code: AbcDeF12345
  Found image: https://i.prnt.sc/someimage.jpg
  -> Downloaded as downloads/AbcDeF12345.jpg
Caption: A cat sitting on a windowsill.
Answer: A cat is sitting by a window.

Trying code: XyZ987lMnOp
  -> No valid image found.

Completed 100 checks. Downloaded 15 images.
```

---

## **Technical Explanation**

- Model Check and Automatic Setup
  - The program checks for the presence of moondream-2b-int8.mf or moondream-0_5b-int8.mf in the model/ folder.
  - If neither is found, it downloads the lightweight moondream-0_5b-int8.mf model in gzipped format, extracts it, and prepares it for use.
- Random Screenshot Discovery
  - The program generates random 11-character alphanumeric codes and constructs potential screenshot URLs (e.g., https://prnt.sc/AbcDeF12345).
  - It parses each page to find valid screenshot images using BeautifulSoup.
- AI Image Analysis
  - Once downloaded, images are analyzed using the Moondream model for captions and visual content recognition.
 
## **Recommended Precautions**
- Avoid uploading sensitive screenshots to public services without ensuring adequate privacy settings.
- Always assume that public links can be indexed or guessed by unauthorized parties.
