# AI Photo Editing with Inpainting

This project is a web application that intelligently swaps image backgrounds and subjects using advanced AI models. It leverages the **Segment Anything Model (SAM-ViT-Base)** for high-precision, zero-shot image segmentation and a **Stable Diffusion Inpainting model** to generate new image content based on text prompts.

Here’s your updated version with the Gradio app feature included:

---

## How It Works

The image editing process follows a multi-step pipeline:

1. **Segmentation:** An input image is processed by the **Segment Anything Model (SAM)**. SAM identifies and isolates the main subject from the background, generating a precise mask.
2. **Mask Generation:** The segmentation output is used to create a black-and-white mask, which dictates the area of the image to be modified.
3. **Inpainting with Stable Diffusion:** The original image, the mask, and a user-defined text prompt are fed into a **Stable Diffusion Inpainting model**. This model generates new pixels within the masked area that match the text description, seamlessly blending it with the unmasked portion of the image.
4. **Interactive Gradio App:** A **Gradio-powered web interface**, integrated with the project’s notebook, allows users to upload images, provide prompts, preview segmentations, and experiment with different background swaps in real time.

---

## Getting Started

Follow these instructions to get the project running on your local machine.

### Dependencies

The project requires Python 3.8+ and the following libraries. You can install them using pip:

```bash
pip install torch transformers diffusers accelerate Pillow
```

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: You may want to create a `requirements.txt` file containing the dependencies listed above.)*

4.  **Model Caching:** The necessary models from Hugging Face (SAM, Stable Diffusion) will be automatically downloaded and cached the first time you run the script.

Here’s an enhanced version of your **Testing** section for the README:

---

## Testing

The model was evaluated using a variety of prompts, mask modes, and CFG settings to test segmentation quality, inpainting performance, and visual consistency. Interactive experiments were run through the Gradio app to simulate real-world use cases, allowing instant previews and parameter adjustments.

The combined automated and interactive testing approach ensured that the pipeline delivers **high-quality, user-ready results** while maintaining performance and stability.

-----

### Test 1: Car Image – Background Replacement

  - **Prompt:** `a car driving on Mars under studio lights. Shot with a vintage camera, 1970s aesthetic, photorealistic`
  - **Negative Prompt:** `artifacts, low quality, distortion`
  - **CFG Settings Tested:** 3.0 and 8.55
  - **Infill:** Background only

**Results**

![Car Image – Background Replacement](./images/prompt1.jpg)
![Car Image – Background Replacement](./images/prompt2.jpg)

  - The lower CFG (3.0) produced a more natural background blend but with less stylization.
  - Higher CFG (8.55) emphasized the Mars texture but introduced minor lighting artifacts.

-----

### Test 2: Car Image – Subject Swap

  - **Prompt:** *same as above*
  - **CFG Settings Tested:** 3.0 and 8.55
  - **Mask Mode:** Subject only

**Results**

![Car Image – Subject Swap](./images/prompt3.jpg)
![Car Image – Subject Swap](./images/prompt4.jpg)

  - Subject replacement worked fairly well. The new car has a different structure and lighting but preserved orientation.
  - The higher CFG provided a sharper, more detailed image.

-----

### Test 3: Background Generation for a Dragon Character

  - **Prompt:** `a cute blue dragon standing in a lush enchanted forest, surrounded by magical floating lights, cinematic depth of field`
  - **Negative Prompt:** *indoors, plain background, studio lighting*
  - **CFG:** 7.65
  - **Infill Mode:** Background only

**Results**
![Dragon image](./images/prompt5.jpg)

  - The generated background successfully followed the "lush enchanted forest" theme, with magical lights enhancing the atmosphere.
  - The relatively high CFG scale (7.65) caused a slightly blurry background, likely due to the "depth of field" instruction in the prompt. Reducing the CFG to around 5.5–6.5 might improve sharpness.

-----

### Test 4: Monalisa as Marylin Monroe

  - **Prompt:** `Monalisa reimagined as Marylin Monroe in pop art style, bold colors, exaggerated makeup, silk screen texture`
  - **Negative Prompt:** *photorealism, oil painting, CG face*
  - **CFG:** 7.5
  - **Infill Mode:** Subject only

**Results**
![Monalisa as Marylin](./images/prompt8.jpg)

  - Acceptable face blend with more makeup. The hairstyle resembles Monroe’s while the face is still recognizable as Mona Lisa.

-----

### Test 5: Monalisa as Marylin Monroe with pop art background

  - **Prompt:** *same as above*
  - **CFG Settings Tested:** 6.5
  - **Mask Mode:** Background only

**Results**
![Monalisa as Marylin](./images/prompt9.jpg)

  - The output transforms the background into a vibrant pop art style with geometric patterns and bright colors, while successfully maintaining the integrity of the subject.

## Built With

  * [Python](https://www.python.org/) - The core programming language.
  * [PyTorch](https://pytorch.org/) - The deep learning framework used by the models.
  * [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) - Used for accessing the Segment Anything Model (SAM).
  * [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index) - Used for running the Stable Diffusion Inpainting model.
  * [Pillow (PIL)](https://www.google.com/search?q=https://python-pillow.org/) - For image manipulation and processing.

## License

Distributed under the MIT License. See [License](LICENSE.txt) for more information.



