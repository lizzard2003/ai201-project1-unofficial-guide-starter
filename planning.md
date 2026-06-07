# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain was off campus housing experience in Texas State University. When searching for answers it was hard to find because I was bombarded by apartment complexes using the search as a marketing avenue. The words that were used in the search did not filter out apartment complexes with the key words.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source                 | Description                                                                 | URL or location                                                                                      |
| --- | ---------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | Reddit                 | Thread about housing                                                        | https://www.reddit.com/r/txstate/comments/1llyjp9/off_campus_housing/                                |
| 2   | Reddit                 | Thread asking about 4 bedroom apt                                           | https://www.reddit.com/r/txstate/comments/1hjd6ez/off_campus_housing/                                |
| 3   | Texas State University | University info page                                                        | https://offcampushousing.txstate.edu                                                                 |
| 4   | Reddit                 | Thread about horrible housing reviews                                       | https://www.reddit.com/r/txstate/comments/1bh90an/offcampus_housing/                                 |
| 5   | Grove Apartment        | Apartment complex off campus offering housing                               | https://groveatsanmarcos.com/                                                                        |
| 6   | Reddit                 | Looking for apartements that are affordable                                 | https://www.reddit.com/r/txstate/comments/1nep0pi/off_campus_housing/                                |
| 7   | Reddit                 | Asking how off campuses expenses are                                        | https://www.reddit.com/r/txstate/comments/1l25m3k/what_are_off_campus_expenses_like/                 |
| 8   | Reddit                 | Asking how to start looking for apartments                                  |                                                                                                      |
| 9   | Facebook Post          | Looking for a 1 bed 1 bath apartment post                                   | https://www.facebook.com/groups/TXSTSubleasesRoommates/posts/2866319006910091/                       |
| 10  | The University Star    | Article on how the University should be more involved in off campus housing | https://universitystar.com/21135/opinions/texas-state-should-be-more-involved-in-off-campus-housing/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
100 characters
**Overlap:**
40 characters
**Reasoning:**
200 character chunck size would be good because they are going to be small sentences on reviews from reddit. 40 character overlap would preserve cross boundary relationships.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
bge-base-en-v1.5 via sentence transformer
**Top-k:**
5
**Production tradeoff reflection:**
If you set the Top-K the return will be return irrelevant chunks. If it is too high you will have alot of noise in your results.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question                                                                                   | Expected answer                                     |
| --- | ------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| 1   | What apartment complex should be avoided when living off campus at Texas State University? | Redpoint, The Outpost                               |
| 2   | What are the cost of apartments outside of Texas State?                                    | 650.00 per month, 820.00 per month, 739 per month   |
| 3   | Does Texas State University have a guide to help choose a place to live off campus?        | Yes, Texas State has a guide to live off campus     |
| 4   | What ammenities can you get by living off campus?                                          | 24 hour gym, resort-style pool, recreational courts |
| 5   | how safe are the complexes off campus?                                                     | Some have car breakins, scorpions                   |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Because of the question being so filtered it might not result in off topic retrivals.

2. We can also get incosistent documents because the key words used are used for marketing.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Text Documents --> chunking 300 characters --> bge-base-en-v1.5 --> Chroma--> Knowledge Ingestion --> Generation

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

I will use Claude to help with my chuncking strategy and have it chuck at the 200 character size with an overlap of 40. I will then analyze the return. Compare the questions and answers.
**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
