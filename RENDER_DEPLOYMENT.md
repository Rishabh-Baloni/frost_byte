# Deploy Telegram Weather Bot to Render

This guide will help you deploy your Telegram weather bot using webhooks on Render.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your bot code should be in a GitHub repository
3. **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather)
4. **OpenWeatherMap API Key**: Get from [OpenWeatherMap](https://openweathermap.org/api)

## Step 1: Prepare Your Repository

Your repository should contain these files:
- `webhook_app.py` - Main Flask webhook application
- `requirements.txt` - Python dependencies
- `Procfile` - Render deployment configuration
- `render.yaml` - Render service configuration (optional)

## Step 2: Deploy to Render

### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" and select "Web Service"

2. **Connect Your Repository**
   - Connect your GitHub account if not already connected
   - Select your bot repository
   - Choose the branch (usually `main` or `master`)

3. **Configure the Service**
   - **Name**: `frostbyte-weather-bot` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python webhook_app.py`

4. **Set Environment Variables**
   Click "Environment" and add these variables:
   ```
   TELEGRAM_TOKEN=your_actual_telegram_bot_token
   WEATHER_API_KEY=your_actual_openweathermap_api_key
   WEBHOOK_URL=https://your-app-name.onrender.com
   WEBHOOK_PORT=10000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (usually 2-3 minutes)

### Option B: Using render.yaml (Blue-Green Deployment)

If you have the `render.yaml` file in your repository:

1. Go to Render Dashboard
2. Click "New +" and select "Blueprint"
3. Connect your repository
4. Render will automatically detect the `render.yaml` file
5. Set the environment variables in the dashboard
6. Deploy

## Step 3: Configure the Webhook

Once your service is deployed and running:

1. **Get Your App URL**
   - Your app will be available at: `https://your-app-name.onrender.com`

2. **Set the Webhook**
   Visit this URL in your browser:
   ```
   https://your-app-name.onrender.com/set_webhook
   ```

   Or use curl:
   ```bash
   curl -X POST https://your-app-name.onrender.com/set_webhook
   ```

3. **Verify Webhook Status**
   Visit:
   ```
   https://your-app-name.onrender.com/webhook_info
   ```

## Step 4: Test Your Bot

1. **Test the Endpoints**
   ```bash
   python test_webhook.py
   ```
   Enter your app URL when prompted.

2. **Test in Telegram**
   - Open Telegram and find your bot
   - Send `/start`
   - Try other commands like `/weather London`

## Step 5: Monitor and Debug

### Check Logs
- Go to your Render dashboard
- Click on your service
- Go to "Logs" tab
- Monitor for any errors

### Health Check
Visit: `https://your-app-name.onrender.com/health`

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

2. **Webhook Not Working**
   - Verify the webhook URL is correct
   - Check that the service is running
   - Look at the logs for errors

3. **Bot Not Responding**
   - Check if the webhook is set correctly
   - Verify environment variables are set
   - Test the `/health` endpoint

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_TOKEN` | Your Telegram bot token | Yes |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `WEBHOOK_URL` | Your Render app URL | Yes |
| `WEBHOOK_PORT` | Port (usually 10000 for Render) | No |

## Render-Specific Features

### Auto-Deploy
- Render automatically deploys when you push to your main branch
- You can disable this in the dashboard

### Custom Domains
- You can add a custom domain in the dashboard
- Update `WEBHOOK_URL` accordingly

### Environment Variables
- Set sensitive data as environment variables
- Never commit tokens to your repository

### Scaling
- Render automatically scales based on traffic
- Free tier has limitations

## Troubleshooting

### Service Won't Start
1. Check the logs in Render dashboard
2. Verify the start command is correct
3. Ensure all dependencies are installed

### Webhook Errors
1. Check if the service is running
2. Verify the webhook URL is accessible
3. Test the endpoints manually

### Bot Not Responding
1. Check if webhook is set: `/webhook_info`
2. Verify environment variables
3. Look at application logs

## Cost Considerations

- **Free Tier**: Limited to 750 hours/month
- **Paid Plans**: Start at $7/month for unlimited usage
- **Sleep Mode**: Free services sleep after 15 minutes of inactivity

## Security Best Practices

1. **Environment Variables**: Never commit sensitive data
2. **HTTPS**: Render provides SSL certificates automatically
3. **Logs**: Monitor logs for suspicious activity
4. **Updates**: Keep dependencies updated

## Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Render Support**: Available in the dashboard
- **Telegram Bot API**: [core.telegram.org/bots/api](https://core.telegram.org/bots/api)

## Next Steps

After successful deployment:

1. **Monitor Performance**: Check Render dashboard regularly
2. **Add Features**: Deploy updates by pushing to your repository
3. **Scale**: Upgrade to paid plan if needed
4. **Custom Domain**: Add your own domain if desired

Your bot is now running on Render with webhooks! 🎉
