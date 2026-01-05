from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI
from config.settings import settings
import datetime

# Initialize LLM
llm = OpenAI(
    model_name=settings.OPENROUTER_LLM_MODEL,
    api_key=settings.OPENROUTER_API_KEY,
    api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
     additional_kwargs={
        "headers": {
            "HTTP-Referer": "http://localhost:8501/",  # Optional, for tracking
            "X-Title": "Personal Knowledge OS",       # Optional, for tracking
        },
    }
)

# Tools Implementation
reminders = []  # In-memory storage for reminders

def generate_weekly_summary() -> str:
    """Generate a summary of key insights from the past week."""
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    return f"""
Weekly Knowledge Digest ({week_ago} to {today})

Top Themes:
- [Auto-analyzed from recent uploads]

Key Learnings:
- New concepts discovered
- Important notes highlighted

Action Items:
- Things to follow up on
- Questions to explore next
    """

def set_reminder(reminder_text: str, due_date: str = None) -> str:
    """Set a reminder from notes."""
    reminder = {
        "text": reminder_text,
        "due": due_date or "No date set",
        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    reminders.append(reminder)
    return f"Reminder set: '{reminder_text}' (Due: {reminder['due']})"

def list_reminders() -> str:
    """List all active reminders."""
    if not reminders:
        return "No reminders set yet."
    return "\n".join([f"• {r['text']} (Due: {r['due']})" for r in reminders])

def draft_email(subject: str, tone: str = "professional") -> str:
    """Draft an email based on context from knowledge base."""
    return f"""
Subject: {subject}

Dear [Recipient],

[Opening based on {tone} tone]

[Body drawing from your notes and insights]

[Closing]

Best regards,
[Your Name]
    """

class ProactiveChatEngine:
    def __init__(self, llm):
        self.llm = llm
        self.chat_history = []
    
    def chat(self, prompt: str) -> str:
        """Handle chat interactions with tool calling."""
        # Add user message to history
        self.chat_history.append(ChatMessage(role=MessageRole.USER, content=prompt))
        
        # Simple intent detection
        prompt_lower = prompt.lower()
        
        if "summary" in prompt_lower or "weekly" in prompt_lower:
            response = generate_weekly_summary()
        elif "remind" in prompt_lower and "list" not in prompt_lower:
            response = set_reminder(prompt)
        elif "list" in prompt_lower and "remind" in prompt_lower:
            response = list_reminders()
        elif "email" in prompt_lower or "draft" in prompt_lower:
            response = "I can help you draft emails. Please provide a subject and the tone you'd like (professional/friendly/casual)."
        else:
            response = "I can help you with weekly summaries, setting reminders, listing reminders, and drafting emails. How can I assist you today?"

        # Add assistant response to history
        self.chat_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=response))
        return response

# Create the chat engine
chat_engine = ProactiveChatEngine(llm=llm)

# Export for use in UI
__all__ = ["chat_engine"]