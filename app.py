# -*- coding: utf-8 -*-
# @Author: Mukhil Sundararaj
# @Date:   2025-11-03 14:10:03
# @Last Modified by:   Mukhil Sundararaj
# @Last Modified time: 2025-11-03 14:15:43
import os
from typing import Optional
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# AI Configuration - Set OPENAI_API_KEY environment variable to enable AI
USE_AI = bool(os.getenv("OPENAI_API_KEY"))
if USE_AI:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except ImportError:
        USE_AI = False
        print("Warning: openai package not installed. Install with: pip install openai")


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def dynamic_greeting() -> str:
    # Friendly time-based greeting without requiring timezone config
    try:
        from datetime import datetime
        hour = datetime.now().hour
        when = "morning" if hour < 12 else ("afternoon" if hour < 18 else "evening")
        return f"Good {when}! I'm the Canvas Assistant. How can I help you with your freelance finances today?"
    except Exception:
        return "Hello! I'm the Canvas Assistant. How can I help you with your freelance finances today?"


def detect_intent(message: str, context_last_intent: Optional[str] = None):
    msg = normalize(message)

    # Follow-up handling for multi-step flows
    if context_last_intent == "invoicing_help":
        if any(k in msg for k in ["1", "create", "new invoice"]):
            return "invoicing_create", (
                "Great — here’s how to create an invoice:\n"
                "1) Open Invoices and tap ‘+’.\n"
                "2) Add client, line items, and due date.\n"
                "3) Preview, then Send.\n"
                "Tip: Add payment terms so clients know when and how to pay."
            )
        if any(k in msg for k in ["2", "track", "existing", "view", "status"]):
            return "invoicing_track", (
                "To track invoices:\n"
                "• Go to Invoices and use the filters (Overdue, Outstanding, Paid).\n"
                "• Tap an invoice to view timeline and payment history.\n"
                "• Use search to jump to a specific client or number."
            )
        if any(k in msg for k in ["3", "late", "overdue", "reminder"]):
            return "invoicing_late", (
                "For late payments:\n"
                "1) Open the overdue invoice.\n"
                "2) Tap ‘Send Reminder’ to email a polite nudge.\n"
                "3) Optionally add a late fee (if that’s your policy).\n"
                "Canvas logs reminders so you have a clear trail."
            )
        # If unclear, prompt again
        return "invoicing_help", (
            "I can help with invoices. Are you looking to:\n"
            "1. Create a new invoice?\n2. Track an existing invoice?\n3. Handle a late payment?"
        )

    if context_last_intent == "tax_jar_info":
        if any(k in msg for k in ["suggest", "recommend", "percentage", "how you decide"]):
            return "tax_jar_suggest", (
                "We estimate a savings percentage using your recent income pace and typical self‑employment tax rates.\n"
                "It’s a starting point — not advice — and you can fine‑tune it anytime.\n"
                "Rule of thumb: 20–30% works for many freelancers, but your situation may differ."
            )
        if any(k in msg for k in ["custom", "adjust", "change", "settings"]):
            return "tax_jar_customize", (
                "To customize Tax Jar:\n"
                "1) Open Settings › Tax Jar.\n"
                "2) Set your preferred % (you can change it anytime).\n"
                "3) Canvas will auto‑set aside that % whenever you log a payment."
            )
        return "tax_jar_info", (
            "Would you like to know more about how we suggest a percentage, or how to customize it?"
        )

    # Niceties
    if any(k in msg for k in ["hello", "hi", "hey"]):
        return "greet", dynamic_greeting()
    if any(k in msg for k in ["thanks", "thank you", "appreciate it"]):
        return "thank_you", "You're very welcome! Is there anything else I can help you with today?"
    if any(k in msg for k in ["bye", "goodbye", "see you", "that’s all", "thats all"]):
        return "goodbye", "Glad I could help. Have a great, productive day!"

    # Core intents
    if any(k in msg for k in ["what is canvas", "what can this app", "tell me about", "about app", "about canvas"]):
        return (
            "about_app",
            "Canvas is an all-in-one financial app designed for creative freelancers. It helps you manage invoices, "
            "track expenses, and automatically save for taxes, so you can focus on your creative work without financial stress.",
        )

    if any(k in msg for k in ["invoice", "invoicing", "overdue", "create invoice", "late payment"]):
        return (
            "invoicing_help",
            "I can definitely help with invoices. Are you looking to:\n1) Create a new invoice\n2) Track an existing invoice\n3) Handle a late payment",
        )

    if any(k in msg for k in ["tax jar", "tax", "taxes", "save for taxes"]):
        return (
            "tax_jar_info",
            "The 'Tax Jar' automatically sets aside a portion of your income for taxes. We recommend a percentage based on your income, "
            "but you can adjust it anytime in Settings. Would you like to know more about how we suggest a percentage, or how to customize it?",
        )

    if any(k in msg for k in ["expense", "spending", "log expense", "software"]):
        return (
            "expense_tracking_help",
            "To record an expense and keep deductions tidy:\n"
            "1) Open Expenses and tap ‘+’.\n"
            "2) Add amount, vendor, and category (e.g., Software, Equipment).\n"
            "3) Add a note or receipt if you have one — it helps at tax time.",
        )

    if any(k in msg for k in ["logged a payment by mistake", "edit payment", "incorrect payment", "fix payment", "mistake on an invoice payment"]):
        return (
            "payment_log_error",
            "Totally fixable. To correct a logged payment:\n"
            "1) Open the invoice.\n"
            "2) Tap Payment History.\n"
            "3) Edit or delete the incorrect entry — Canvas will auto‑adjust your Tax Jar.",
        )

    if any(k in msg for k in ["projects tab", "how do projects", "project income", "projects"]):
        return (
            "project_management",
            "Projects help you see the full picture:\n"
            "• Create a project and set a budget.\n"
            "• Link invoices and expenses to that project.\n"
            "• Track profitability at a glance (income – costs).",
        )

    if any(k in msg for k in ["connect bank", "link bank", "bank account", "payment methods", "is it safe to link"]):
        return (
            "connect_bank",
            "To link your bank securely:\n"
            "1) Go to Settings › Payment Methods.\n"
            "2) Choose ‘Connect bank’ and select your institution via Plaid.\n"
            "Your credentials are encrypted and never stored by Canvas.",
        )

    # Financial advice detection - must come before fallback
    if any(k in msg for k in ["should i", "advice", "recommend", "what should", "is it better", "should i register", "llc", "s-corp", "tax filing", "investment", "invest"]):
        return (
            "financial_advice_decline",
            "As an AI assistant for the Canvas app, I can't provide financial advice, but I can help you organize your business data to discuss with a professional advisor. Would you like help tracking your expenses, invoices, or Tax Jar savings?",
        )

    # Ambiguity clarification
    if "payment" in msg and "expense" not in msg:
        return (
            "clarify_payment",
            "Got it. Are you trying to log a payment you received from a client, or track an expense you paid?",
        )

    return (
        "fallback",
        "I'm not sure I understand that. I can help with topics like invoicing, tax savings, expenses, and project management. Could you try rephrasing your question?",
    )


def build_response(intent: str, message: str):
    suggestions = []
    rationale = None
    follow_up = None

    if intent == "greet":
        suggestions = ["About Canvas", "Create an invoice", "Tax Jar"]
        rationale = "You greeted me, so I introduced myself."
    elif intent == "thank_you":
        suggestions = ["Invoices", "Expenses", "Projects"]
        rationale = "You expressed thanks, so I offered to continue helping."
    elif intent == "goodbye":
        rationale = "You ended the conversation."
    elif intent == "about_app":
        suggestions = ["Invoices", "Expenses", "Projects"]
        rationale = "You asked about Canvas, so I described the app."
    elif intent == "invoicing_help":
        follow_up = "invoicing_help"
        suggestions = ["1", "2", "3"]
        rationale = "I detected invoicing keywords and offered a short menu."
    elif intent.startswith("invoicing_"):
        suggestions = ["Send an invoice", "See overdue invoices", "How to add late fees"]
        rationale = "You selected an invoicing option, so I provided specific steps."
    elif intent == "tax_jar_info":
        follow_up = "tax_jar_info"
        suggestions = ["How do you suggest a %?", "How do I customize it?", "What % should I use?"]
        rationale = "You asked about Tax Jar; I offered two follow-up paths."
    elif intent in ("tax_jar_suggest", "tax_jar_customize"):
        suggestions = ["Open Tax Jar settings", "Change percentage", "Invoices"]
        rationale = "You chose a Tax Jar topic, so I explained that area."
    elif intent == "expense_tracking_help":
        suggestions = ["Add a receipt", "Categorize an expense", "Monthly spending"]
        rationale = "You mentioned expenses, so I explained how to log and categorize."
    elif intent == "payment_log_error":
        suggestions = ["Edit payment", "Delete payment", "View payment history"]
        rationale = "You mentioned a mistaken payment; I provided correction steps."
    elif intent == "project_management":
        suggestions = ["Create a Project", "Link an Invoice", "See profitability"]
        rationale = "You asked about projects; I summarized how they work."
    elif intent == "connect_bank":
        suggestions = ["Open Settings", "Is Plaid secure?", "Payment Methods location"]
        rationale = "You asked about bank linking; I explained the secure process."
    elif intent == "clarify_payment":
        suggestions = ["Log a client payment", "Track an expense"]
        rationale = "'Payment' can be ambiguous; I asked a clarifying question."
    elif intent == "financial_advice_decline":
        suggestions = ["Track expenses", "View Tax Jar", "Contact support"]
        rationale = "User asked for financial advice; I politely declined and offered to help organize data instead."
    else:
        suggestions = ["Invoices", "Tax Jar", "Expenses"]
        rationale = "Your message didn't match known topics, so I suggested common ones."

    return suggestions, rationale, follow_up


def generate_ai_response(user_message: str, intent: str, base_response: str, context: dict) -> str:
    """
    Generate an enhanced AI response based on detected intent.
    Falls back to base_response if AI is unavailable or fails.
    """
    if not USE_AI:
        return base_response
    
    # Comprehensive system prompt with full persona instructions
    system_prompt = f"""You are the Canvas Assistant, a friendly, professional, and highly capable AI helper for creative freelancers using the Canvas financial app. Your primary goal is to reduce your user's financial anxiety and administrative overload by providing instant clarity and automating repetitive tasks. You must always act as a calm, clear, and reassuring partner in managing their business finances.

CRITICAL PERSONA RULES:

1. INTERACTION STYLE & TONE:
   - Be Proactive and Guiding: You are a helpful assistant. If a user logs an expense, suggest they categorize it for tax purposes. If their Tax Jar is behind schedule, gently let them know. This is "Guidance, Not Guesswork."
   - Clarity Over Clutter: Provide concise, well-structured answers. Use lists and formatting to make key information easy to scan and understand.
   - Maintain a Calm, Reassuring Tone: Never be alarming or overly casual. Your purpose is to reduce anxiety. Use phrases like "Got it," "Certainly," and "Here's a look at..."
   - Simplicity is Key: Avoid complex financial jargon. If you must use a term like "net profit," briefly explain what it means in parentheses.
   - You MUST adhere to a calm, clear, and reassuring tone. Do not use complex financial jargon.

2. PROCEDURAL RULES:
   - Gather All Information First: For multi-step tasks like creating an invoice or logging an expense, patiently gather all the necessary details from the user before confirming the action.
   - Always Confirm Actions: After performing an action, always confirm success and the result of the action.
   - Resolve Ambiguity: If a user's request is unclear (e.g., "Send a reminder"), ask clarifying questions. Do not guess.
   - When answering questions about features, synthesize information naturally and conversationally. Do not simply output raw text.

3. CRITICAL GUARDRAILS & BOUNDARIES:
   - You Are NOT a Financial Advisor: This is your most important rule. You MUST NOT give financial advice, investment advice, or specific tax filing advice (e.g., "Should I register as an LLC?"). You can only report on the data within the Canvas app and explain financial concepts generally.
   - Politely Decline Out-of-Scope Requests: If a user asks for advice, you must politely decline and clarify your role. A good response is: "As an AI assistant for the Canvas app, I can't provide financial advice, but I can help you organize your business data to discuss with a professional advisor."
   - Provide an Escalation Path: If you cannot fulfill a request, the user is frustrated, or they explicitly ask for a human, you must provide the user with the option to contact human support. The email is support@canvasapp.com.

4. YOUR CAPABILITIES (Context for responses):
   You can help with:
   - Dashboard & Financial Overview: Summaries, balances, Tax Jar status, income vs expenses, Action Items, recent transactions
   - Invoice Management: Create invoices, check status, list by status, log payments, send reminders
   - Project Management: Create projects, list by status, provide project details
   - Expense Management: Log expenses, list expenses, show category spending, categorize uncategorized expenses
   - General Knowledge & Support: Answer questions about Canvas features and general freelance financial concepts

Current Intent: {intent}
Base Response to Enhance: {base_response}

RESPONSE GENERATION INSTRUCTIONS:
- Generate a natural, conversational response that matches the intent
- Preserve the helpful content of the base response
- Be BRIEF and HIGH-SIGNAL: aim for 1–2 short sentences (≤ 240 characters total)
- If steps are required, use at most 3 concise bullets or numbered steps
- Maintain the Canvas voice: calm, supportive, clear, reassuring; no filler
- Do not invent features or advice; if out-of-scope, decline politely
- If the user seems anxious, be extra reassuring in one short sentence
- Prefer plain words over jargon (explain terms briefly if needed)"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective and fast
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=120,
        )
        ai_response = response.choices[0].message.content.strip()
        # Fallback to base if AI response is too short or seems off
        if len(ai_response) < 10:
            return base_response
        return ai_response
    except Exception as e:
        print(f"AI generation error: {e}")
        return base_response  # Fallback to static response


@app.post("/api/chat")
def chat():
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "")
    context = data.get("context", {}) or {}
    last_intent = context.get("lastIntent")

    intent, base_response = detect_intent(message, last_intent)
    
    # Enhance response with AI if available, otherwise use base response
    response_text = generate_ai_response(message, intent, base_response, context)
    
    suggestions, rationale, follow_up = build_response(intent, message)

    return jsonify(
        {
            "response": response_text,
            "intent": intent,
            "followUpIntent": follow_up,
            "rationale": rationale,
            "suggestions": suggestions,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)


