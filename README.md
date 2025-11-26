# 🎨 Concept Art Generator v3.0

Video game concept art generator using **Claude (prompts) + FLUX (images)** with a modern web interface.

**Version 3.0**: Migrated from AWS Titan to fal.ai FLUX for better quality and no restrictive filters.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials (optional, you can also do it in the UI)
cp .env.example .env
# Edit .env with:
#   - AWS credentials (for Claude)
#   - fal.ai API Key (for FLUX)

# 3. Run the application
streamlit run app.py
```

The app will automatically open at `http://localhost:8501`

## ✨ Features

- **Modern Web Interface**: Intuitive and responsive Streamlit UI
- **Better Quality**: FLUX generates superior images compared to AWS Titan
- **No Restrictive Filters**: No more content validation errors
- **Dual AI**:
  - **Claude 3.5 Sonnet** (AWS Bedrock) for creative prompts
  - **FLUX** (via fal.ai) for high-quality image generation
- **Customizable**: Select categories and number of images
- **Real-Time Visualization**: See images as they're generated
- **Automatic Organization**: Saves images by category with metadata
- **3 FLUX Models**: Dev (balanced), Pro (maximum quality), Schnell (ultra fast)

## 📋 Requirements

- Python 3.8+
- **AWS Account** with Bedrock access:
  - Claude 3.5 Sonnet (inference profile: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`)
  - Only for creative prompt generation
- **fal.ai Account**:
  - Sign up at https://fal.ai
  - Get your API key at https://fal.ai/dashboard/keys
  - Free plan available for testing

## 📁 Project Structure

```
concept-art-generator/
├── app.py                    # ⭐ Main Streamlit application
├── requirements.txt          # Dependencies (6 packages)
├── .env.example             # Configuration template
├── .env                     # Your configuration (create this)
├── README.md                # This file
├── README_STREAMLIT.md      # Detailed usage guide
├── AWS_BEDROCK_SETUP.md     # AWS configuration guide
└── outputs/                 # Generated images
    └── project_name/
        ├── main_character/
        ├── enemies/
        ├── environments/
        └── ...
```

## 🎯 Art Categories

- **Main Character**: Main protagonist
- **Enemies**: Enemies and antagonists
- **Environments**: Environments and scenarios
- **Weapons**: Weapons and equipment
- **Collectibles**: Collectible items
- **NPCs**: Non-playable characters
- **UI Elements**: Interface elements

## 💡 Usage Example

1. Describe your video game:
   ```
   Third-person action RPG game, Dark Souls style.
   Set in a dark medieval fantasy world.
   Gothic castles, dark forests, monstrous creatures.
   Realistic aesthetic with gloomy atmosphere.
   ```

2. Select categories (e.g., Character, Enemies, Environments)

3. Adjust number of images per category (1-3)

4. Click "Generate Concept Art"

5. Images will be generated and saved automatically

## 📊 Estimated Costs

- **Claude 3.5 Sonnet** (AWS): ~$0.003 per prompt generation
- **FLUX Dev** (fal.ai): ~$0.03 per image
- **FLUX Pro** (fal.ai): ~$0.05 per image
- **FLUX Schnell** (fal.ai): ~$0.02 per image

**Example**: 2 images × 3 categories = 6 images with FLUX Dev ≈ **$0.18 USD**

*More affordable and better quality than AWS Titan*

## 🌐 Deploy to Streamlit Cloud

1. Push the project to GitHub (make sure `.env` is in `.gitignore`)
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. **IMPORTANT**: DO NOT add your credentials to secrets
4. Users must enter their own API keys in the interface
5. Each user uses their own credentials (AWS + fal.ai)
6. Deploy ready! Each person pays for their own usage

## 🔧 AWS Bedrock Configuration

See [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) for detailed instructions on:
- Creating AWS account
- Enabling Bedrock
- Activating models
- Configuring credentials

## 📖 Documentation

- **[README_STREAMLIT.md](README_STREAMLIT.md)**: Complete usage guide
- **[AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)**: AWS Bedrock setup

## 🛠️ Troubleshooting

### Error: "AccessDeniedException" (AWS)
- Verify AWS credentials in the sidebar
- Confirm Bedrock access is enabled in your account
- Use us-east-1 region (recommended)

### Error: "Model not found" (AWS)
- Go to AWS Console → Bedrock → Model access
- Enable Claude 3.5 Sonnet
- Wait a few minutes

### fal.ai Error
- Verify your fal.ai API key is correct
- Check that you have credits in your fal.ai account
- Try FLUX Schnell (faster and more economical)

### Images don't look good
- Describe your game in more detail
- Try FLUX Pro for maximum quality
- Adjust the number of images

## 📄 License

Apache 2.0 License - Use it freely

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) - Web interface
- [Claude 3.5 Sonnet](https://www.anthropic.com/claude) - Creative prompt generation
- [FLUX](https://fal.ai/models/flux) - High-quality image generation
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Claude API access

---

**v3.0 - Built with ❤️ using Streamlit, Claude 3.5 Sonnet, and FLUX**

### Changelog v3.0
- ✨ Migrated from AWS Titan to fal.ai FLUX
- 🚀 Better image quality
- ⚡ No restrictive content filters
- 💰 More competitive costs
- 🎨 3 FLUX models available (Dev, Pro, Schnell)
