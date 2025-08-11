# Project: AI Photo Editing with Inpainting

This project’s web app swaps image backgrounds using the **Segment Anything Model (SAM-ViT-Base)** for precise, efficient zero-shot segmentation. SAM uses an image encoder, prompt encoder, and mask decoder to separate subjects from backgrounds. Downloaded from HuggingFace, it’s configured for **mask generation** with the **Transformers** library.


## Getting Started

Instructions for how to get a copy of the project running on your local machine.

### Dependencies

```
Examples here
```

### Installation

Step by step explanation of how to get a dev environment running.

List out the steps

```
Give an example here
```

## Testing

Explain the steps needed to run any automated tests


## 👨‍💻 Break Down Tests
### Test 1: Car Image – Background Replacement
- **Prompt:** `a car driving on Mars under studio lights. Shot with a vintage camera, 1970s aesthetic, photorealistic`
- **Negative Prompt:** `artifacts, low quality, distortion`
- **CFG Settings Tested:** 3.0 and 8.55
- **Infill:** Background only

### Results
![Car Image – Background Replacement](./images/prompt1.jpg)
![Car Image – Background Replacement](./images/prompt2.jpg)
- The lower CFG (3.0) produced a more natural background blend but with less stylization.
- Higher CFG (8.55) emphasized the Mars texture but introduced minor lighting artifacts.

---

### Test 2: Car Image – Subject Swap
- **Prompt:** *same as above*
- **CFG Settings Tested:** 3.0 and 8.55
- **Mask Mode:** Subject only

### Results
![Car Image – Subject Swap](./images/prompt3.jpg)
![Car Image – Subject Swap](./images/prompt4.jpg)

- Subject replacement worked fairly well. The new car has different structure and lighting but preserved orientation.
- The higher CFGS provided a sharper more detailed image.

---

### Test 3: Background Generation for a Dragon Character
- **Prompt:** *a cute blue dragon standing in a lush enchanted forest, surrounded by magical floating lights, cinematic depth of field*
- **Negative Prompt:** *indoors, plain background, studio lighting*
- **CFG:** 7.65
- **Infill Mode:** Background only

### 💡 Results
![Dragon image](./images/prompt5.jpg)
The generated background successfully followed the "lush enchanted forest" theme, with magical lights enhancing the atmosphere. However, due to the relatively high CFG scale (7.65), the result shows a **slightly blurry background**, especially around the edges of the subject. This might be attributed to the aggressive guidance pulling the model toward an overly cinematic look, as hinted by the "depth of field" phrase in the prompt.

Reducing the CFG to around **5.5–6.5** might preserve more background sharpness while keeping the magical aesthetic.

---


### Test 4: Monalisa as Marylin Monroe
- **Prompt:** *Monalisa reimagined as Marylin Monroe in pop art style, bold colors, exaggerated makeup, silk screen texture*
- **Negative Prompt:** *photorealism, oil painting, CG face*
- **CFG:** 7.5
- **Infill Mode:** Subject only

### Results
![Monalisa as Marylin](./images/prompt8.jpg)
Acceptable face blend with more makeup, hairstyle kinds of resembles Monroe’s, still recognizable as Mona Lisa.

---

### Test 5: Monalisa as Marylin Monroe with pop art background
- **Prompt:** *same as above*
- **CFG Settings Tested:** 6.5
- **Mask Mode:** Background only

### Results
![Monalisa as Marylin](./images/prompt9.jpg)
- The output transforms it into a vibrant pop art style with geometric patterns and bright colors
- The system was able to maintain subject integrity while completely reimagining the artistic context

```
Examples here
```

## Project Instructions

This section should contain all the student deliverables for this project.

## Built With

* [Item1](www.item1.com) - Description of item
* [Item2](www.item2.com) - Description of item
* [Item3](www.item3.com) - Description of item

Include all items used to build project.

## License

[License](LICENSE.txt)
