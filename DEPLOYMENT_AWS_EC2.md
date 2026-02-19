# AWS EC2 Deployment Guide - Career Compass

Complete step-by-step guide to deploying Career Compass on AWS EC2.

---

## Prerequisites

- AWS account with EC2 access
- Your `GEMINI_API_KEY` ready
- SSH key pair created in AWS

---

## Step 1: Launch EC2 Instance

1. Go to **AWS Console > EC2 > Launch Instance**
2. **Name**: `career-compass-prod`
3. **AMI**: Ubuntu 22.04 LTS (or Amazon Linux 2023)
4. **Instance type**: `t3.small` (minimum) or `t3.medium` (recommended)
5. **Key pair**: Create or select existing
6. **Storage**: 20 GB gp3
7. Click **Launch instance**

---

## Step 2: Configure Security Group

In the security group, add these **Inbound rules**:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH | TCP | 22 | Your IP |
| Custom TCP | TCP | 8501 | 0.0.0.0/0 |

Outbound: Allow all.

---

## Step 3: Connect to Instance

```bash
ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

## Step 4: Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
```

---

## Step 5: Clone Repository

```bash
git clone https://github.com/nasir331786/career-compass-genai-chatbot.git
cd career-compass-genai-chatbot
```

---

## Step 6: Set Up Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 7: Configure Environment Variables

```bash
nano .env
```

Add:
```env
GEMINI_API_KEY=your_production_api_key_here
PYTHONUNBUFFERED=1
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

---

## Step 8: Create Logs Directory

```bash
mkdir -p logs
```

---

## Step 9A: Run in Background (Quick)

```bash
export $(cat .env | xargs)
nohup .venv/bin/streamlit run app/main.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true > logs/nohup.log 2>&1 &

echo "App running. PID: $!"
```

Access at: `http://<EC2_PUBLIC_IP>:8501`

---

## Step 9B: Run as systemd Service (Production)

1. Create service file:
```bash
sudo nano /etc/systemd/system/career-compass.service
```

2. Paste:
```ini
[Unit]
Description=Career Compass GenAI Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/career-compass-genai-chatbot
EnvironmentFile=/home/ubuntu/career-compass-genai-chatbot/.env
ExecStart=/home/ubuntu/career-compass-genai-chatbot/.venv/bin/streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable career-compass
sudo systemctl start career-compass
sudo systemctl status career-compass
```

---

## Step 10: Verify Deployment

```bash
# Check service status
sudo systemctl status career-compass

# View logs
tail -f logs/app.log

# Test from outside
curl -I http://<EC2_PUBLIC_IP>:8501
```

Access the app at: `http://<EC2_PUBLIC_IP>:8501`

---

## Updating the App

```bash
cd career-compass-genai-chatbot
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart career-compass
```

---

## Production Hardening Tips

- Put NGINX reverse proxy in front for HTTPS + custom domain
- Use AWS Secrets Manager instead of `.env` for the API key
- Enable CloudWatch logs for centralized monitoring
- Restrict security group port 8501 to your office/VPN CIDR
- Set up EC2 Auto Recovery for high availability
- Rotate `GEMINI_API_KEY` every 90 days
