# Configuration Guide - AWS Bedrock + fal.ai (v3.0)

This guide will help you configure Concept Art Agent v3.0 using:
- **AWS Bedrock** (only for Claude - prompt generation)
- **fal.ai** (for FLUX - image generation)

## Why this configuration?

- **AWS Bedrock (Claude)**: To generate high-quality creative prompts
- **fal.ai (FLUX)**: Better image quality than AWS Titan
- **No restrictive filters**: No more AWS content validation errors
- **More economical**: Competitive costs for image generation

## Step 1: Get AWS Credentials

### 1.1 Access AWS Console

1. Go to [AWS Console](https://console.aws.amazon.com)
2. Sign in with your account

### 1.2 Create Access Keys

1. Go to **IAM** (Identity and Access Management)
2. Navigate to **Users** → Select your user
3. Go to **Security credentials** tab
4. In the **Access keys** section, click **Create access key**
5. Select **Use case**: "Third-party service" or "CLI"
6. Save both the **Access Key ID** and **Secret Access Key**

**IMPORTANT**: The Secret Access Key is only shown once. Save it securely.

### 1.3 Required Permissions

Your AWS user must have permissions for:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

You can use the managed policy: `AmazonBedrockFullAccess`

## Step 2: Verify Claude Access in Bedrock

### 2.1 Access Amazon Bedrock

1. In AWS Console, search for **Amazon Bedrock**
2. Go to **Model access** in the sidebar
3. Verify you have access to:
   - ✅ **Claude 3.5 Sonnet** (us.anthropic.claude-3-5-sonnet-20241022-v2:0)

**NOTE v3.0**: You NO longer need access to Stability AI or Titan, because we'll use fal.ai for images

### 2.2 Verify Region

Bedrock is not available in all regions. Recommended regions:
- **us-east-1** (N. Virginia) - Recommended
- **us-west-2** (Oregon)
- **eu-west-1** (Ireland)

## Step 3: Configure fal.ai

### 3.1 Create fal.ai account

1. Go to https://fal.ai
2. Sign up with your email or GitHub
3. They have a free plan for testing

### 3.2 Get API Key

1. Go to https://fal.ai/dashboard/keys
2. Click **Create new key**
3. Copy your API key (save it securely)

## Step 4: Configure .env file

Open your `.env` file and configure the credentials:

```env
# ========================================
# CONCEPT ART AGENT v3.0 - CONFIGURATION
# ========================================

# AWS (for Claude - creative prompt generation)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# fal.ai (for FLUX - image generation)
FAL_KEY=your_fal_api_key_here
```

### Available Models

**Claude (AWS Bedrock) - For prompts:**
- Automatically uses: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

**FLUX (fal.ai) - For images:**
- `fal-ai/flux/dev` - Quality/speed balance (Recommended)
- `fal-ai/flux-pro` - Maximum quality
- `fal-ai/flux/schnell` - Ultra fast and economical

## Step 5: Test Configuration

### 5.1 Install dependencies

```bash
pip install -r requirements.txt
```

### 5.2 Run Streamlit application

```bash
streamlit run app.py
```

### 5.3 Test generation

1. The app will open in your browser (http://localhost:8501)
2. Enter your credentials in the sidebar:
   - AWS Access Key ID
   - AWS Secret Access Key
   - fal.ai API Key
3. Describe your video game
4. Select FLUX model (recommended: flux/dev)
5. Click "Generate Concept Art"

## Estimated Costs (v3.0)

### Claude (AWS Bedrock) - Prompt Generation

**Claude 3.5 Sonnet:**
- Input: ~$3.00 / 1M tokens
- Output: ~$15.00 / 1M tokens
- **Per project: ~$0.003** (very low usage)

### FLUX (fal.ai) - Image Generation

**FLUX Dev:**
- ~$0.03 per image
- Project (14 images): ~$0.42

**FLUX Pro:**
- ~$0.05 per image
- Project (14 images): ~$0.70

**FLUX Schnell:**
- ~$0.02 per image
- Project (14 images): ~$0.28

**Total per project (FLUX Dev)**: ~$0.42 + $0.003 ≈ **$0.42 USD**

## Version Comparison

| Feature | v2.0 (AWS Titan) | v3.0 (fal.ai FLUX) |
|---|---|---|
| Price per image | $0.04 | $0.02 - $0.05 |
| Quality | Medium | High/Excellent |
| Content filters | Very restrictive ❌ | No filters ✅ |
| Speed | Medium | Fast/Ultra fast |
| Project (14 imgs) | ~$0.56 | $0.28 - $0.70 |
| Validation errors | Frequent | None |
| **Total project** | **$0.57** | **$0.42** (Dev) |

## Troubleshooting

### AWS Bedrock Errors (Claude)

**Error: "Could not connect to the endpoint"**
- Verify your region supports Bedrock
- Use `us-east-1` (recommended)
- Verify Bedrock is enabled in your account

**Error: "AccessDeniedException"**
- Go to IAM and add the `AmazonBedrockFullAccess` policy
- Verify your user has `bedrock:InvokeModel` permissions

**Error: "ValidationException: Model not found"**
- Go to AWS Bedrock → Model access
- Enable Claude 3.5 Sonnet
- Wait a few minutes for activation

**AWS credentials don't work**
- Verify credentials are correctly copied
- There should be no extra spaces
- Access Key ID must start with `AKIA`

### fal.ai Errors (FLUX)

**Authentication error**
- Verify your fal.ai API key is correct
- Copy it without extra spaces from the dashboard

**Error: "Insufficient credits"**
- Check your balance at https://fal.ai/dashboard
- Reload credits if necessary
- Free plan has limits

**Images don't generate**
- Try FLUX Schnell first (faster and cheaper)
- Verify your prompt is not empty
- Check error logs in the app

**Timeout or very slow**
- FLUX Schnell is the fastest (4 steps)
- FLUX Dev is balanced (28 steps)
- FLUX Pro is the slowest but best quality

## Security

### Best Practices

1. **Don't share your `.env`**: This file contains private credentials
2. **Use .gitignore**: Make sure `.env` is in `.gitignore`
3. **Rotate credentials**: Change your Access Keys periodically
4. **Minimum permissions**: Give only necessary permissions to your user
5. **Monitor usage**: Check AWS CloudWatch to detect abnormal usage

### Revoke Access Keys

If you believe your credentials are compromised:

1. Go to IAM → Users → Your user
2. Security credentials
3. Find the compromised Access Key
4. Click "Actions" → "Deactivate" or "Delete"
5. Create new credentials

## Additional Resources

### AWS Bedrock
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude Models in Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html)
- [AWS Pricing Calculator](https://calculator.aws/#/)

### fal.ai
- [fal.ai Documentation](https://fal.ai/docs)
- [FLUX Models](https://fal.ai/models/flux)
- [fal.ai Dashboard](https://fal.ai/dashboard)
- [fal.ai Pricing](https://fal.ai/pricing)

## Support

If you have problems:

1. **AWS**: Check the [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
2. **fal.ai**: Consult [fal.ai docs](https://fal.ai/docs)
3. **App**: Check error logs in the Streamlit interface
4. Run `streamlit run app.py` and check the console

---

## Changelog v3.0

✨ **Main changes**:
- Migrated from AWS Titan to fal.ai FLUX for image generation
- AWS Bedrock only for Claude (creative prompts)
- Better image quality with FLUX
- No restrictive content filters
- 3 FLUX models available (Dev, Pro, Schnell)
- More competitive costs

Ready! Now you can generate high-quality concept art with Claude + FLUX.
