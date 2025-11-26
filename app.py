"""
Concept Art Generator - Streamlit App
Generates concept art for video games using Claude (prompts) + FLUX (images via fal.ai)
Version 3.0 - Migrated from AWS Titan to fal.ai FLUX
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path
import streamlit as st
import boto3
from botocore.exceptions import ClientError
import fal_client
import requests

# ==================== CONFIGURATION ====================

st.set_page_config(
    page_title="Concept Art Generator",
    page_icon="🎨",
    layout="wide"
)

# ==================== CORE FUNCTIONS ====================

def get_bedrock_client(region, aws_key, aws_secret):
    """Creates AWS Bedrock client (only for Claude - prompt generation)"""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )

def generate_prompts(game_description, bedrock_client, model_id):
    """Generates creative prompts with Claude via AWS Bedrock"""
    system_prompt = """You are an expert in video game concept art.
    Generate detailed prompts optimized for the FLUX image generation model."""

    user_prompt = f"""Video game description: {game_description}

Generate 2 specific prompts for each category (in English, optimized for FLUX):

MAIN_CHARACTER:
- [prompt 1]
- [prompt 2]

ENEMIES:
- [prompt 1]
- [prompt 2]

ENVIRONMENTS:
- [prompt 1]
- [prompt 2]

WEAPONS:
- [prompt 1]
- [prompt 2]

COLLECTIBLES:
- [prompt 1]
- [prompt 2]

NPCS:
- [prompt 1]
- [prompt 2]

UI_ELEMENTS:
- [prompt 1]
- [prompt 2]

Each prompt should be descriptive, include artistic style and technical details."""

    try:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 3000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())
        claude_response = response_body["content"][0]["text"]

        prompts = parse_prompts(claude_response)

        # Verify there are prompts
        total_prompts = sum(len(p) for p in prompts.values())
        if total_prompts == 0:
            st.warning("Claude didn't generate valid prompts. Using fallback prompts...")
            return get_fallback_prompts(game_description)

        return prompts

    except Exception as e:
        st.warning(f"Error with Claude: {str(e)}. Using fallback prompts...")
        return get_fallback_prompts(game_description)

def get_fallback_prompts(game_description):
    """Fallback prompts if Claude fails or is unavailable"""
    base = f"concept art, {game_description}, professional game art, detailed, high quality"

    return {
        "main_character": [
            f"Main character hero design, {base}, full body, dynamic pose",
            f"Protagonist character concept, {base}, front and side view"
        ],
        "enemies": [
            f"Enemy creature design, {base}, menacing, threatening",
            f"Antagonist monster concept, {base}, detailed anatomy"
        ],
        "environments": [
            f"Game environment landscape, {base}, atmospheric, detailed background",
            f"Game world scenery, {base}, cinematic composition"
        ],
        "weapons": [
            f"Weapon design concept, {base}, detailed illustration",
            f"Game weapon asset, {base}, multiple angles"
        ],
        "collectibles": [
            f"Collectible items, {base}, game pickups, power-ups",
            f"Game items concept, {base}, glowing effects"
        ],
        "npcs": [
            f"NPC character design, {base}, friendly character",
            f"Supporting character concept, {base}, full body"
        ],
        "ui_elements": [
            f"Game UI design, {base}, HUD elements, interface mockup",
            f"Menu interface, {base}, buttons and icons"
        ]
    }

def parse_prompts(response_text):
    """Parses Claude's response and extracts prompts by category"""
    category_map = {
        "MAIN_CHARACTER": "main_character",
        "ENEMIES": "enemies",
        "ENVIRONMENTS": "environments",
        "WEAPONS": "weapons",
        "COLLECTIBLES": "collectibles",
        "NPCS": "npcs",
        "UI_ELEMENTS": "ui_elements"
    }

    prompts = {cat: [] for cat in category_map.values()}
    current_category = None

    for line in response_text.split('\n'):
        line = line.strip()
        for key, value in category_map.items():
            if line.upper().startswith(key):
                current_category = value
                break

        if current_category and (line.startswith('-') or line.startswith('*')):
            prompt = line.lstrip('-*').strip()
            if prompt and not prompt.startswith('['):  # Ignore placeholders
                prompts[current_category].append(prompt)

    return prompts

def generate_image_fal(prompt, model_id, fal_api_key):
    """
    Generates an image using fal.ai with FLUX models

    Args:
        prompt: Descriptive text to generate the image
        model_id: FLUX model ID to use (flux/dev, flux-pro, flux/schnell)
        fal_api_key: fal.ai API key

    Returns:
        bytes: Image data in PNG format
    """

    # Configure API key
    os.environ["FAL_KEY"] = fal_api_key

    # Configuration by FLUX model
    model_configs = {
        "fal-ai/flux-pro": {
            "model": "fal-ai/flux-pro",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1
            }
        },
        "fal-ai/flux/dev": {
            "model": "fal-ai/flux/dev",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1
            }
        },
        "fal-ai/flux/schnell": {
            "model": "fal-ai/flux/schnell",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 4,
                "num_images": 1
            }
        }
    }

    config = model_configs.get(model_id, model_configs["fal-ai/flux/dev"])

    try:
        # Call fal.ai
        result = fal_client.subscribe(
            config["model"],
            arguments=config["params"]
        )

        # Download image
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return response.content

        return None

    except Exception as e:
        raise Exception(f"Error with fal.ai: {str(e)}")

def save_image(image_data, category, index, project_dir):
    """Saves image to the file system"""
    category_dir = Path(project_dir) / category
    category_dir.mkdir(parents=True, exist_ok=True)

    filepath = category_dir / f"{category}_{index}.png"
    with open(filepath, "wb") as f:
        f.write(image_data)

    return str(filepath)

# ==================== STREAMLIT INTERFACE ====================

# Category names
CATEGORY_NAMES = {
    "main_character": "Main Character", "enemies": "Enemies",
    "environments": "Environments", "weapons": "Weapons",
    "collectibles": "Collectibles", "npcs": "NPCs",
    "ui_elements": "UI Elements"
}

st.title("🎨 Concept Art Generator")
st.markdown("Generate concept art for video games using **Claude + FLUX** (fal.ai)")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("🧠 Claude (Prompts)")
    aws_key = st.text_input("AWS Access Key ID", type="password",
                             value=os.getenv("AWS_ACCESS_KEY_ID", ""))
    aws_secret = st.text_input("AWS Secret Access Key", type="password",
                               value=os.getenv("AWS_SECRET_ACCESS_KEY", ""))
    aws_region = st.selectbox("AWS Region",
                              ["us-east-1", "us-west-2", "eu-west-1"],
                              index=0)

    st.divider()

    st.subheader("🎨 fal.ai (Images)")
    fal_api_key = st.text_input("fal.ai API Key", type="password",
                                 value=os.getenv("FAL_KEY", ""),
                                 help="Get your API key at https://fal.ai/dashboard/keys")

    image_model = st.selectbox(
        "FLUX Model",
        [
            "fal-ai/flux/dev",
            "fal-ai/flux-pro",
            "fal-ai/flux/schnell"
        ],
        index=0,
        help="FLUX Dev: Quality/speed balance | Pro: Maximum quality | Schnell: Ultra fast"
    )

    images_per_category = st.slider("Images per category", 1, 3, 2)

    st.divider()

    categories_to_generate = st.multiselect(
        "Categories to generate",
        ["main_character", "enemies", "environments", "weapons",
         "collectibles", "npcs", "ui_elements"],
        default=["main_character", "enemies", "environments"]
    )

# Main area
st.header("📝 Video Game Description")

game_description = st.text_area(
    "Describe your video game in detail (genre, style, setting, etc.)",
    height=150,
    placeholder="Example: Third-person action RPG game, Dark Souls style..."
)

project_name = st.text_input("Project name (optional)",
                              placeholder="my_project")

# Main button
if st.button("🚀 Generate Concept Art", type="primary"):

    # Validations
    if not game_description:
        st.error("Please enter a video game description")
        st.stop()

    if not aws_key or not aws_secret:
        st.error("Please configure your AWS credentials for Claude in the sidebar")
        st.stop()

    if not fal_api_key:
        st.error("Please configure your fal.ai API Key in the sidebar")
        st.stop()

    if not categories_to_generate:
        st.error("Select at least one category to generate")
        st.stop()

    # Start generation
    try:
        # Create project directory
        if not project_name:
            project_name = "project_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        project_dir = Path("outputs") / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Bedrock client
        bedrock_client = get_bedrock_client(aws_region, aws_key, aws_secret)

        # STEP 1: Generate prompts with Claude
        with st.spinner("🧠 Generating creative prompts with Claude..."):
            prompts = generate_prompts(
                game_description,
                bedrock_client,
                "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            )
            st.success("✅ Prompts generated successfully")

            # Show generated prompts
            with st.expander("🔍 View generated prompts"):
                for cat, cat_prompts in prompts.items():
                    if cat in categories_to_generate and cat_prompts:
                        st.markdown(f"**{CATEGORY_NAMES.get(cat, cat)}:**")
                        for i, p in enumerate(cat_prompts[:images_per_category], 1):
                            st.text(f"{i}. {p[:100]}...")

        # STEP 2: Generate images
        st.header("🖼️ Generating Images")

        all_generated_images = {}
        total_generated = 0

        for category in categories_to_generate:
            st.subheader(f"📂 {CATEGORY_NAMES.get(category, category)}")

            category_prompts = prompts.get(category, [])[:images_per_category]

            if not category_prompts:
                st.warning(f"No prompts available for {category}")
                continue

            cols = st.columns(len(category_prompts))
            generated_paths = []

            for idx, (col, prompt) in enumerate(zip(cols, category_prompts), 1):
                with col:
                    with st.spinner(f"Generating {idx}/{len(category_prompts)}..."):
                        try:
                            image_data = generate_image_fal(
                                prompt,
                                image_model,
                                fal_api_key
                            )

                            if image_data:
                                filepath = save_image(image_data, category, idx, project_dir)
                                generated_paths.append(filepath)
                                st.image(image_data, caption=f"Image {idx}", use_column_width=True)
                                st.caption(f"💬 {prompt[:80]}...")
                                total_generated += 1
                            else:
                                st.error(f"Error generating image {idx}")

                        except Exception as e:
                            st.error(f"Error: {str(e)}")

            all_generated_images[category] = generated_paths

        # Final summary
        st.divider()
        st.success(f"🎉 Generation completed: {total_generated} images created")
        st.info(f"📁 Project saved at: `{project_dir}`")

        # Save metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "game_description": game_description,
            "prompts": prompts,
            "images": all_generated_images,
            "total_images": total_generated
        }

        with open(project_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    except ClientError as e:
        st.error(f"❌ AWS Error: {str(e)}")
        st.info("Verify your credentials and Bedrock permissions")

    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>Concept Art Generator v3.0 | Powered by Claude + FLUX</p>
    <p>Claude 3.5 Sonnet (prompts) + FLUX via fal.ai (images)</p>
</div>
""", unsafe_allow_html=True)
