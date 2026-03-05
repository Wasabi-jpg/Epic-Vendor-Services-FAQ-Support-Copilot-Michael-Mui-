- Used Google Gemini for determining and planning project structure.
- Gemini discussed ideas on how to format JSON, but I chose my own JSON design instead (category, question, answer, source url).
- Gemini simplified code for loading JSON from seed data.
- Cursor used for engine.py and memory.py, where I prompted for sliding window memory for memory.py and provided
context into how I wanted questions and faq matching should be done.
- Cursor also organized "Commands to run" for later setup.
- Gemini helped plan main.py, while I coded it.
- Gemini used for index.html, for the sake of quick testing and getting basic UI.

- Post Standup
- Using Cursor Planning Mode to determine changes/different approach to current retrieval methods due to the current version sounding inacurrate.
    - Reasoning through why not just send in seed_data to llm everytime, versus current implementation which is to send in most "relevant" faq seed data to the llm based on basic scoring system.
    