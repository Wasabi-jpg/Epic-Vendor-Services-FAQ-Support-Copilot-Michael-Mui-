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
- Cursor Planning Mode helped not only in changing how model reasoned from FAQ (full dataset vs subset selection), but also helped in coming up with better system prompts for the model to obey. Forced the model to adhere to a standard response format for manual parsers to digest and provide to users.
- Cursor provided thoughts on the lack of reliability gap between 8B vs 3B parameter model, leading to my opting of a 3B parameter model.
- Cursor helped in resolving source grounding, where model was returning sources in wrong format (Sources: [1],[2] vs Sources: 1,2), evading parsers to be able to return grounded data. I directed it to create new Regex filters to find model's used sources. 
- Cursor helped in improving showing memory references, where I directed it to adjsut certain return values and introduce new functions to ultimately allow llama3.2:3b to reason whether it wants to use memory or not.
- Cursor, side note, has issues with shell display (text disappears).
- Overall thoughts, coding agent is potent, but I was able to direct it to be specific on what I want edited.
- Cursor developed testing suite.