# Prompts for Meeting Action Items Extraction

## Prompt (initial version)
```
You are an AI assistant that extracts action items from meeting transcripts.

Given a meeting transcript, extract all actionable to-do items.

For each action item, provide:
- Task description
- Responsible person (if mentioned)
- Deadline (if mentioned)

Meeting transcript:
{transcript}
```

## Prompt (revision1 - adding rules)
```
You are an AI assistant that extracts action items from meeting transcripts.

Given a meeting transcript, extract all actionable to-do items.

For each action item, provide:
- Task description
- Responsible person (if mentioned)
- Deadline (if mentioned)

Rules:
- Only extract clear, actionable tasks
- Do NOT hallucinate information that is not in the transcript
- Ignore completed tasks and general discussion
- If no action items exist, return an empty list

Meeting transcript:
{transcript}
```


## Prompt (revision2 - structured output)

```
You are an AI assistant that extracts action items from meeting transcripts.

Given a meeting transcript, extract all actionable to-do items.

For each action item, provide:
- Task description
- Responsible person (if mentioned)
- Deadline (if mentioned)

Rules:
- Only extract clear, actionable tasks
- Do NOT hallucinate information that is not in the transcript
- Ignore completed tasks and general discussion
- If no action items exist, return an empty list

Format your response as a JSON array:
[
  {
    "task": "task description",
    "owner": "person name or null",
    "deadline": "deadline or null"
  }
]

Meeting transcript:
{transcript}
```

1. In the initial version, I simply told the large language model what my task was and what I needed it to do. 
2. In the first revised version, I added some rules to restrict the responses, with the aim of reducing the number of answers and obtaining clearer results.
3. I subsequently made further revisions, specifying that the response should be in JSON format, so that I could load it directly upon receipt and obtain the final standardised output.

1. One issue with the first version was that the output was a single block of text, so I had to search through it to find the answer. I therefore added some rules to obtain a simpler result.
2. In the second version, the response was simpler, but it was still a block of text that could not be directly parsed or stored, so I added functionality to have it return JSON format.
3. I am very satisfied with the third version, as it returns JSON format; however, there might still be issues, so I added JSON parsing to the app to achieve the desired result.