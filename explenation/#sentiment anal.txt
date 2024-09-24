#sentiment anal


### **Key Data to Save**

1. **Characters:**
   - Names
   - Relationships (e.g., Eve, Rafe, Papa)
   - Traits or emotions associated with characters

2. **Settings:**
   - Location (e.g., home, storm, drive)
   - Time references (e.g., "nine thirty," "winter")

3. **Themes:**
   - Family dynamics
   - Emotional tension (e.g., fear, love, uncertainty)
   - Conflict (internal and external)

4. **Narrative Structure:**
   - Plot points (e.g., arrival of Papa, dinner setting)
   - Important dialogues

5. **Symbolism:**
   - Objects (e.g., the wine glass, clock)
   - Weather conditions as metaphors for emotions
```bash
### **Data Structure Example**

The extracted data could be saved in a JSON format as follows:

```json
{
  "characters": [
    {
      "name": "Eve",
      "relationships": {
        "husband": "Rafe",
        "father": "Papa"
      },
      "emotions": ["calm", "nostalgic", "conflicted"]
    },
    {
      "name": "Rafe",
      "relationships": {
        "wife": "Eve",
        "father-in-law": "Papa"
      },
      "emotions": ["agitated", "formal"]
    },
    {
      "name": "Papa",
      "relationships": {
        "daughter": "Eve",
        "grandchild": "Zach"
      },
      "emotions": ["weary", "vulnerable"]
    }
  ],
  "settings": {
    "location": "home",
    "time": "nine thirty",
    "weather": "stormy"
  },
  "themes": ["family", "conflict", "uncertainty"],
  "plot_points": [
    "Arrival of Papa",
    "Dinner preparations",
    "Eve's internal conflict about her father's accusations"
  ],
  "symbols": [
    {
      "object": "wine glass",
      "symbolism": "calmness and normalcy"
    },
    {
      "object": "storm",
      "symbolism": "emotional turmoil"
    }
  ]
}
```
```bash
### **Processing Steps**

1. **Input Text:**
   The script will accept the narrative text as input.

2. **Text Analysis:**
   - **Tokenization:** Split the text into sentences and words for easier analysis.
   - **Named Entity Recognition (NER):** Identify characters, locations, and time references.
   - **Sentiment Analysis:** Analyze emotional tones associated with different parts of the text.

3. **Data Extraction:**
   - Use pattern matching (e.g., regex) to identify relationships and emotions.
   - Create a data structure (like the JSON example) to store extracted information.

4. **Saving Data:**
   - Save the extracted data in a structured format (JSON, CSV, etc.) to a designated output file (e.g., `narrative_analysis.json`).

5. **Output Summary:**
   - Print a summary of the analysis to the console, showing key characters, themes, and any notable insights.

### **Example Walkthrough of the Script Path**

1. **Initialization:**
   - The script starts by loading necessary libraries (e.g., `json`, `nltk`, `spacy`).
   - It defines functions for text processing, analysis, and saving data.

2. **Input Handling:**
   - The script reads the narrative from a text file or takes it directly from user input.

3. **Processing:**
   - **Tokenization:** The narrative is split into sentences:
     ```python
     sentences = nltk.sent_tokenize(narrative)
     ```
   - **NER:** Characters and locations are identified:
     ```python
     entities = nlp(narrative).ents
     for entity in entities:
         if entity.label_ in ['PERSON', 'GPE', 'TIME']:
             # Save relevant data
     ```
   - **Emotion Detection:** The script analyzes sentences for emotional cues:
     ```python
     emotions = analyze_emotions(sentences)
     ```

4. **Data Structuring:**
   - As data is extracted, it is structured into the defined JSON format.

5. **Saving Data:**
   - The JSON data is saved to a file:
     ```python
     with open('narrative_analysis.json', 'w') as outfile:
         json.dump(data, outfile, indent=4)
     ```

6. **Completion:**
   - The script prints a summary of the analysis:
     ```python
     print("Analysis complete. Data saved to narrative_analysis.json.")
     ```

