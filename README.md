# AI Chatbot LCD
An AI chatbot that communicates through an LCD display connected to an Arduino on Windows.

## Prerequisites
- Arduino (configured for COM9)
- Python (added to PATH)
- ngrok (added to PATH)
- VS Code or Notepad
- Render.com account
- Groq API key

## Hardware Setup
1. Connect Arduino to laptop
2. Configure Arduino to COM9:
   - Device Manager → Ports → Arduino Uno → Properties → Port Settings → Advanced → COM Port Number (9)

## Software Setup

### 1. Start Serial Bridge
```bash
cd Desktop\ChatbotLCD
python serial_bridge.py
```

### 2. Start ngrok Tunnel
Open new PowerShell tab:
```bash
ngrok http 5000
```
Note the generated URL (e.g., `https://32b643aa110a.ngrok-free.app/`)

### 3. Deploy n8n on Render
1. Go to [Render.com](https://render.com)
2. Click "Deploy your app for free" → Sign in → "New Web Service" → "Existing Image"
3. Get Docker image from [n8n.io](https://n8n.io):
   - Go to n8n.io → "Get started for free" → "Open installation docs" → "Docker Installation Guide"
   - Copy: `docker.n8n.io/n8nio/n8n`
4. Paste in "Image URL" → Connect → Select free instance → Deploy
5. Wait for deployment and note the generated URL (e.g., `https://n8n-jpa3.onrender.com`)

### 4. Configure n8n Workflow
1. Access your n8n URL and create account
2. Create workflow with these nodes:

#### Chat Trigger
- Add "Chat Trigger" as first step

#### AI Agent
- Add "AI Agent" after Chat Trigger
- Chat Model: Select "Groq"
- Get Groq API key from [console.groq.com/keys](https://console.groq.com/keys)
- Create new credential with your API key
- Memory: Select "Simple Memory"
- System Message: "You are a helpful assistant. Keep message under 32 characters for lcd display."

#### HTTP Request
- Method: POST
- URL: `[your-ngrok-url]/display` (e.g., `https://e42cae760d76.ngrok-free.app/display`)
- Send Body: ON
- Body Content Type: JSON
- Specify Body: Using Fields Below
  - Name: `message`
  - Value: `{{ $node["AI Agent"].json["output"] }}`

## File Structure
```
Desktop/
└── ChatbotLCD/
    └── serial_bridge.py
```

## Usage
1. Complete hardware setup
2. Run serial bridge
3. Start ngrok tunnel
4. Deploy and configure n8n workflow
5. Chat with your AI through the LCD display!

## Notes
- ngrok URLs are unique for each session
- Render free tier resets after inactivity
- Arduino must be on COM9 (configurable in code)
- LCD messages limited to 32 characters
