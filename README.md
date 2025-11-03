# Canvas Assistant Chatbot

A conversational AI assistant for the Canvas financial app, designed for creative freelancers. Built with Flask (Python) backend and vanilla HTML/CSS/JavaScript frontend.

## Features

- **11 Intent Handlers**: Greeting, thank you, goodbye, about app, invoicing (multi-step), tax jar (multi-step), expenses, payment errors, projects, bank connection, and fallback
- **Multi-step Conversations**: Guided flows for invoicing and tax jar with follow-up questions
- **Quick Reply Suggestions**: Context-aware suggestion chips for faster interaction
- **Rationale Display**: "Why this?" toggle shows reasoning behind responses (design principles)
- **Feedback Controls**: Thumbs up/down for user feedback
- **Responsive Design**: Mobile-first UI with Canvas brand colors

## Project Structure

```
.
├── app.py              # Flask backend with intent detection
├── api/
│   └── chat.py        # Vercel serverless function entry point
├── index.html         # Frontend chat UI (HTML/CSS/JS)
├── requirements.txt   # Python dependencies
├── vercel.json       # Vercel deployment configuration
└── README.md         # This file
```

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:3000`

3. Open `index.html` in a browser or serve it:
```bash
# Using Python's built-in server
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

**Note**: For local testing, you may need to update the fetch URL in `index.html` to `http://localhost:3000/api/chat` if serving HTML separately.

### Test Intent Detection

Run the test script to verify intent detection logic:
```bash
python3 test_intents.py
```

### Manual API Testing

Test the API endpoint with curl:
```bash
# Test greeting
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Test invoicing (multi-step)
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I create an invoice?"}'

# Test follow-up (requires context)
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "1", "context": {"lastIntent": "invoicing_help"}}'
```

## Deployment to Vercel

### Option 1: Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

Follow the prompts to link your project and deploy.

### Option 2: Vercel Dashboard

1. Push your code to GitHub/GitLab/Bitbucket
2. Go to [vercel.com](https://vercel.com) and import your repository
3. Vercel will auto-detect Python and deploy

### Verify Deployment

After deployment, test the public URL:
- Frontend: `https://your-project.vercel.app`
- API: `https://your-project.vercel.app/api/chat`

## Design Principles Integration

This chatbot implements several AI design principles:

- **Design Responsibly**: Stateless, no PII storage; clear limitations
- **Mental Models**: Rationale display helps users understand bot behavior
- **Co-Creation**: Quick-reply suggestions guide effective interactions
- **Appropriate Trust**: Transparent about capabilities and limitations
- **Imperfection**: Graceful fallback and clarification mechanisms

## Canvas Brand Colors

- Brand Purple: `#5D3FD3` (header)
- Accent Teal: `#1ABC9C` (buttons, suggestions)
- Background: `#F7F7FA`
- User Bubble: `#E8F8F5` (light teal tint)

## Intent Examples

| User Query | Intent | Response Type |
|------------|--------|---------------|
| "Hello" | `greet` | Greeting + suggestions |
| "What is Canvas?" | `about_app` | App overview |
| "How do I create an invoice?" | `invoicing_help` | Multi-step menu |
| "1" (after invoicing) | `invoicing_create` | Specific steps |
| "What is the Tax Jar?" | `tax_jar_info` | Overview + follow-up options |
| "Thanks!" | `thank_you` | Polite acknowledgment |
| "Random question" | `fallback` | Graceful error + suggestions |

## License

This project is part of a CS-GY 6543 HCI assignment.

