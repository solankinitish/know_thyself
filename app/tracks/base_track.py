from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.llm.llm_client import LLMClient
from app.memory.session_memory import SessionMemory
from app.memory.persistent_memory import PersistentMemory
from app.prompts.summary_prompts import SummaryPrompts


class BaseTrack:
    def __init__(self, system_prompt, user_id, track, n_exchanges):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("system", "Relevant context from past sessions:\n{past_memories}"),
            ("human", "{human_message}")
        ])
        self.llm = LLMClient()
        self.s_memory = SessionMemory()
        self.p_memory = PersistentMemory()
        self.summary_prompts = SummaryPrompts()

        self.user_id = user_id
        self.track = track
        self.exchange_count = 0
        self.session_no = 1
        self.n_exchanges = n_exchanges
    
    def _summarize_and_store(self):
        history = self.s_memory.get_history()
        # convert history to string
        history_s = "\n".join([msg.content for msg in history])
        # get the right summary_prompt
        prompt_template = getattr(self.summary_prompts, self.track)
        summary_prompt = prompt_template.format(conversation=history_s)
        # generate summary using LLM
        summary = self.llm.chat(summary_prompt)
        # store in persistent memory
        self.p_memory.store(
            user_id=self.user_id,
            track=self.track,
            session_no=self.session_no,
            memory_type="session_summary",
            content=summary
        )
        self.exchange_count = 0
        self.session_no += 1
    
    def respond(self, message: str) -> str:
        results = self.p_memory.retrieve(self.user_id, self.track, message)
        history_p = "\n".join([match.metadata["content"] for match in results.matches])
        messages = self.prompt.format_messages(
            history=self.s_memory.get_history(),
            past_memories=history_p,
            human_message=message)
        self.exchange_count += 1
        response = self.llm.generate(messages)
        self.s_memory.add_interaction(message, response)
        if self.exchange_count == self.n_exchanges:
            self._summarize_and_store()

        return response
