# AI Lesson Path
This project is used to learn to concepts about AI and Semantic Kernel Agents and Plugins

## To Run
* `python -m venv .venv`
* `.\.venv\Scripts\activate` or `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `python single_agent_main.py`
```
You: what time does the store open on tuesday?
Jeeves: 'The store opens at 9:00 AM on Tuesday.'
You: what are teh specials?
Jeeves: 'The specials are as follows:
- **Special Soup:** Clam Chowder
- **Special Salad:** Cobb Salad
- **Special Drink:** Chai Tea'
You: how much for tea?
Jeeves: 'The price for Chai Tea is $2.99.'
```

* `python multi_agent_main.py`
```
You: slogan for certified cars
CopyWriter: '"Certified Cars: Because ‘almost’ isn’t in our vocabulary."'
ArtDirector: 'The slogan is not legally sound as it uses the term "certified," which could imply a guarantee or warranty regarding the cars. To fix this, avoid language that suggests guarantees or official certifications unless you can substantiate those claims. Refine the slogan by focusing on the quality or reliability of the cars without implying certification.'
CopyWriter: '"Reliable Rides: Quality You Can Trust."'
ArtDirector: 'The slogan "Reliable Rides: Quality You Can Trust" is approved. It communicates trust and quality without any legal implications.'
```
