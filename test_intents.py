#!/usr/bin/env python3
"""
Test script to verify intent detection logic without Flask server.
Run: python3 test_intents.py
"""

import sys
sys.path.insert(0, '.')

from app import detect_intent, build_response

def test_intent(message, expected_intent_prefix=None, context=None):
    """Test a single intent detection."""
    intent, response = detect_intent(message, context)
    suggestions, rationale, follow_up = build_response(intent, message)
    
    print(f"\n{'='*60}")
    print(f"Input: '{message}'")
    if context:
        print(f"Context: {context}")
    print(f"Detected Intent: {intent}")
    print(f"Response: {response[:80]}...")
    print(f"Follow-up: {follow_up}")
    print(f"Rationale: {rationale}")
    print(f"Suggestions: {suggestions}")
    
    if expected_intent_prefix:
        assert intent.startswith(expected_intent_prefix), f"Expected intent starting with '{expected_intent_prefix}', got '{intent}'"
        print(f"✓ PASS: Intent matches expected prefix")
    else:
        print(f"✓ Intent detected")
    
    return intent, response

# Test cases
print("Testing Canvas Assistant Intent Detection\n")

# Test greeting
test_intent("Hello", "greet")

# Test about app
test_intent("What is Canvas?", "about_app")

# Test invoicing (multi-step)
test_intent("How do I create an invoice?", "invoicing_help")
test_intent("1", "invoicing_create", context="invoicing_help")
test_intent("late payment", "invoicing_late", context="invoicing_help")

# Test tax jar (multi-step)
test_intent("What is the Tax Jar?", "tax_jar_info")
test_intent("how do you suggest", "tax_jar_suggest", context="tax_jar_info")
test_intent("customize", "tax_jar_customize", context="tax_jar_info")

# Test expense tracking
test_intent("How do I add an expense?", "expense_tracking_help")

# Test payment error
test_intent("I logged a payment by mistake", "payment_log_error")

# Test project management
test_intent("How do projects work?", "project_management")

# Test bank connection
test_intent("How do I connect my bank?", "connect_bank")

# Test thank you
test_intent("Thanks!", "thank_you")

# Test goodbye
test_intent("Bye", "goodbye")

# Test fallback
test_intent("What is the weather?", "fallback")

# Test ambiguity clarification
test_intent("I need help with a payment", "clarify_payment")

print(f"\n{'='*60}")
print("All tests completed!")
print("To test the full Flask server, run: python3 app.py")
print("Then test with: curl -X POST http://localhost:3000/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"Hello\"}'")

