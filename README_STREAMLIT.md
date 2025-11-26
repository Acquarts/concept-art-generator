# 🎨 Concept Art Generator v3.0 - Streamlit App

Generates concept art for video games using **Claude (prompts) + FLUX (images via fal.ai)** in a simple and elegant web interface.

## ✨ Features

- **Modern web interface**: Streamlit for easy interaction
- **Dual AI**:
  - **Claude 3.5 Sonnet** (AWS Bedrock) for creative prompts
  - **FLUX** (fal.ai) for high-quality images
- **No restrictive filters**: No more content validation errors
- **3 FLUX models**: Dev, Pro, Schnell
- **Customizable**: Select categories and number of images
- **Real-time visualization**: See images as they're generated

## 🚀 Quick Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

You need **2 services**:

**A) AWS Bedrock (for Claude - prompts)**
- AWS Access Key ID
- AWS Secret Access Key
- Bedrock access enabled in us-east-1
- Enabled model: Claude 3.5 Sonnet (`us.anthropic.claude-3-5-sonnet-20241022-v2:0`)

**B) fal.ai (for FLUX - images)**
- Sign up at https://fal.ai
- Get your API key at https://fal.ai/dashboard/keys
- Free plan available for testing

You can configure credentials in:
- A `.env` file:
  ```
  AWS_ACCESS_KEY_ID=your_access_key
  AWS_SECRET_ACCESS_KEY=your_secret_key
  FAL_KEY=your_fal_api_key
  ```
- Or directly in the Streamlit interface (sidebar) ← Recommended for deployment

### 3. Run the application

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Configure your credentials** in the sidebar (if not using `.env`)

2. **Describe your video game** in the main text area
   - Include: genre, visual style, setting, theme, references

3. **Customize generation**:
   - Number of images per category (1-3)
   - Select which categories to generate

4. **Click "Generate Concept Art"**

5. **Wait while generating**:
   - First, prompts are created with Claude (AWS Bedrock)
   - Then, images are generated with FLUX (fal.ai)
   - You'll see images appear in real-time

6. **Results saved in** `outputs/project_name/`

## 📁 Output Structure

```
outputs/
└── project_name/
    ├── main_character/
    │   ├── main_character_1.png
    │   └── main_character_2.png
    ├── enemies/
    ├── environments/
    ├── weapons/
    ├── collectibles/
    ├── npcs/
    ├── ui_elements/
    └── metadata.json
```

## 🎯 Available Categories

- **Main Character**: Main character/protagonist
- **Enemies**: Enemies and antagonists
- **Environments**: Environments and scenarios
- **Weapons**: Weapons and equipment
- **Collectibles**: Collectible items
- **NPCs**: Non-playable characters
- **UI Elements**: User interface elements

## 💡 Description Example

```
Third-person action RPG game, Dark Souls style.
Set in a dark medieval fantasy world.
Gothic castles, dark forests, monstrous creatures.
Realistic aesthetic with gloomy atmosphere.
Inspired by Elden Ring and Bloodborne.
```

## 🔧 Troubleshooting

### Error: "AccessDeniedException"
- Verify your AWS credentials are correct
- Make sure you have Bedrock access in your region
- Check that models are enabled in the AWS Bedrock console

### Error: "Model not found" (AWS)
- Go to AWS Bedrock console → Model access
- Enable Claude 3.5 Sonnet
- Wait a few minutes for activation

### fal.ai Error
- Verify your API key is correct
- Check that you have credits in fal.ai
- Try FLUX Schnell (faster and cheaper)

### Images don't generate well
- Try FLUX Pro for maximum quality
- Adjust the number of images per category
- Try more specific descriptions

## 🌐 Deploy to Streamlit Cloud

1. Push your code to GitHub (`.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. **IMPORTANT**: DO NOT add secrets in Streamlit Cloud
5. Users will enter their own API keys in the interface
6. Each user pays for their own usage
7. Automatic deployment completed

## 📊 Estimated Costs

**Per prompt generation:**
- Claude 3.5 Sonnet (AWS): ~$0.003

**Per generated image:**
- FLUX Dev (fal.ai): ~$0.03
- FLUX Pro (fal.ai): ~$0.05
- FLUX Schnell (fal.ai): ~$0.02

**Example**: 2 images × 3 categories with FLUX Dev = 6 images ≈ **$0.18 USD**

*More affordable and better quality than AWS Titan*

## 🆚 v3.0 Advantages

| Aspect | v2.0 (AWS Titan) | v3.0 (fal.ai FLUX) |
|---------|------------------|---------------------|
| Image quality | Medium | High/Excellent |
| Content filters | Very restrictive ❌ | No filters ✅ |
| Speed | Medium | Fast (Schnell: ultra fast) |
| Cost per image | ~$0.04 | $0.02-$0.05 |
| Available models | 3 (Titan/Nova) | 3 FLUX (Dev/Pro/Schnell) |
| Validation errors | Frequent | None |

## 📝 License

This project is open source. Use it freely for your projects.

---

**v3.0 - Claude 3.5 Sonnet + FLUX**

### Changelog v3.0
- ✨ Migrated from AWS Titan to fal.ai FLUX
- 🚀 Better image quality (FLUX surpasses Titan)
- ⚡ No restrictive AWS content filters
- 💰 More competitive costs
- 🎨 3 FLUX models: Dev, Pro, Schnell
- ⚙️ Dual configuration: AWS (prompts) + fal.ai (images)
