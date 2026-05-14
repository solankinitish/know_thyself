

class SummaryPrompts:
    def __init__(self):
        self.fitness = """
You are summarizing a coaching conversation for future reference.
Extract and structure the following information from the conversation:

- Goals: What is the user trying to achieve?
- Current Metrics: Any numbers mentioned (weight, lifts, sleep hours, etc.)
- Progress Made: What has improved since last session?
- Struggles Identified: What is the user finding difficult?
- Next Focus Areas: What should the next session prioritize?

Conversation:
{conversation}

Provide a concise structured summary under each heading. If information is not available for a section, write "Not mentioned".
"""
        self.habits = """
You are summarizing a coaching conversation for future reference.
Extract and structure the following information from the conversation:

Habits: Which habits are the user building?
Adherence: For each habit, how is the user adhering to them(Score out of 10 for each)?
Struggles: Is the user facing any new struggle?
Conversation:
{conversation}

Provide a concise structured summary under each heading. If information is not available for a section, write "Not mentioned".
"""

        self.relationships = """
You are summarizing a coaching conversation for future reference.
Extract and structure the following information from the conversation:

Issues: What are the issues in the relationship that the user is facing?
Progress: How is the progress in each issue?
Mood: What is the mood of the user while giving updates?
Conversation:
{conversation}

Provide a concise structured summary under each heading. If information is not available for a section, write "Not mentioned".
"""