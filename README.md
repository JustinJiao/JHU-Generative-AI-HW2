# realistic business workflow
1. summarizing meetings into action items
2. Everyone is a user, because everyone who attends a meeting faces a similar challenge: turning the points raised in the meeting into concrete to-do items.
3. Input: The system will be fed a lengthy text that may contain a variety of content, such as small talk or updates on project progress; however, the system needs to identify the relevant sections and list them out.
4. Output: The system requires the user to enter some to-do items, clearly informing them of the tasks that need to be completed.
5. As a great deal is often discussed during routine meetings, relying solely on handwritten notes or memory can lead to omissions; moreover, taking notes whilst listening to a manager's instructions may also result in details being missed. However, by following this approach, all the information can be distilled and organised, providing us with a clearer and more effective to-do list.

## How to Run

### Prerequisites
- Python 3.7+
- Google Gemini API key

### Setup Steps

1. **Activate virtual environment**

   On macOS/Linux:
   ```bash
   cd "/Users/justin/Desktop/JHU/Generative AI/HW2"
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   cd "C:\path\to\JHU\Generative AI\HW2"
   venv\Scripts\activate
   ```

2. **Install dependencies** (if not already installed)
   ```bash
   pip install google-generativeai python-dotenv
   ```

3. **Configure API key**

   Make sure your `.env` file contains:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```

4. **Run the program**
   ```bash
   python app.py
   ```

5. **View results**

   The program will:
   - Display progress in the terminal
   - Save results to `results.json`

6. **Deactivate virtual environment** (when finished)
   ```bash
   deactivate
   ```

## Video
[Watch the video](https://youtu.be/UdEVmoj_HwU)