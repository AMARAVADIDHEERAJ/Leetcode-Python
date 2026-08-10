Absolutely. Let's continue.

# RAG — Lesson 5: RAG vs Fine-Tuning vs Long Context vs Agents

This is one of the most important architectural decisions in modern LLM applications.

A lot of beginners ask:

> "Should I use RAG or fine-tuning?"

But that's actually too narrow.

You may have **four different tools**:

```text
                    LLM Application
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
      RAG          Fine-tuning       Long Context
       │
       └──────────────────────┐
                              ↓
                           Agents
```

These solve different problems.

---

# 1. First: What problem are you solving?

Let's take four different requirements.

### Requirement A

> "Answer questions using our company's latest internal documents."

You need **RAG**.

### Requirement B

> "Make the model consistently respond in our company's specific style."

You may need **fine-tuning**.

### Requirement C

> "Analyze this 500-page document."

You may benefit from **long context**.

### Requirement D

> "Research this topic across several sources, perform calculations, and decide what tools to use."

You may need an **agent**.

The mistake is trying to use one technique for all four.

---

# 2. RAG

Let's start with what you already know.

RAG means:

> **Retrieve relevant external information and provide it to the model at runtime.**

Architecture:

```text id="q7k2xp"
User Query
     ↓
Retriever
     ↓
Relevant Knowledge
     ↓
LLM
     ↓
Answer
```

The model itself doesn't need to memorize the information.

The information lives outside the model.

---

# 3. When should you use RAG?

RAG is especially useful when knowledge is:

### Private

```text id="6m0q1s"
Company policies
Internal documents
Customer information
Private knowledge bases
```

### Frequently changing

```text id="3s8p7d"
Today's prices
Current policies
Latest documentation
Product inventory
```

### Large

```text id="8w2f4k"
Thousands/millions of documents
```

### Source-sensitive

You want the answer to be based on specific documents.

---

# 4. RAG example

Suppose your company updates its leave policy:

```text id="q2m7v1"
2025:
20 days

2026:
25 days
```

With RAG, you update the knowledge base.

The LLM doesn't need to be retrained.

```text id="z4r8s2"
New document
    ↓
Chunk
    ↓
Embedding
    ↓
Vector DB
    ↓
Available to RAG
```

That's one of RAG's biggest advantages.

---

# 5. Fine-Tuning

Fine-tuning is different.

Instead of retrieving information at runtime, you modify the model's parameters through additional training.

Conceptually:

```text id="j5p1k8"
Base Model
    +
Training Examples
    ↓
Fine-Tuned Model
```

The purpose isn't normally:

> "Store my company's documents."

Instead, fine-tuning is often used to change **behavior**.

---

# 6. What can fine-tuning improve?

For example, you want the model to consistently produce:

```text id="3x7n4q"
Input:
Customer complaint

Output format:
{
  "category": "...",
  "priority": "...",
  "summary": "..."
}
```

If you have thousands of high-quality examples, fine-tuning can help the model learn this behavior.

Other examples:

* Classification
* Specific output formats
* Specialized task behavior
* Style
* Domain-specific patterns
* Consistent instruction following

---

# 7. RAG vs Fine-Tuning

Think of it like this:

### RAG

> "Here is information. Use it."

### Fine-tuning

> "Learn to behave this way."

That's the simplest mental model.

---

# 8. Don't use fine-tuning as a database

This is a very important rule.

Suppose you have:

```text id="9p3v5t"
500,000 company documents
```

You might think:

> "I'll fine-tune the model on all these documents."

That's usually not the right approach.

Why?

Because company information:

* Changes
* Needs updates
* May need access control
* May need source attribution
* May need deletion
* May be too large

RAG is much better suited to dynamically accessing this information.

---

# 9. Fine-tuning + RAG

They aren't competitors.

You can combine them.

For example:

```text id="q5m8r2"
                 User Query
                     ↓
                  RAG
                     ↓
              Company Knowledge
                     ↓
              Fine-Tuned LLM
                     ↓
                 Answer
```

RAG provides the knowledge.

Fine-tuning provides specialized behavior.

---

# 10. Example

Imagine you're building a medical-document assistant.

You want:

1. Answers based on your private documents.
2. A very specific JSON output format.
3. Consistent terminology.

Potential architecture:

```text id="c3k7w1"
Private Documents
       ↓
      RAG
       ↓
Retrieved Context
       ↓
Fine-Tuned Model
       ↓
Structured Answer
```

Different techniques solve different problems.

---

# 11. Long Context

Now let's introduce the third option.

Modern LLMs can process very large contexts.

For example:

```text id="u7n2p4"
Question
+
Large Document
+
Instructions
        ↓
       LLM
```

You might not need retrieval if the entire relevant document can fit comfortably into the model's context window.

---

# 12. When is long context useful?

Suppose the user uploads:

```text id="k3m9x1"
one 300-page contract
```

and asks:

> "Summarize this contract and identify conflicts between Section 4 and Section 18."

You may want the model to have access to broad portions of the document.

RAG could retrieve only some chunks.

But the question may require understanding relationships across the entire document.

Long context can be useful here.

---

# 13. RAG vs Long Context

### RAG

```text id="s5q1v9"
Huge Knowledge Base
       ↓
Retrieve relevant pieces
       ↓
LLM
```

### Long Context

```text id="j8r2x4"
Large Document
       ↓
Put large portion into context
       ↓
LLM
```

So:

```text id="c7m3n8"
RAG = selective retrieval

Long Context = broad context
```

---

# 14. Is long context replacing RAG?

No.

For a small number of documents:

```text id="w6p2k9"
Long context can be enough.
```

For:

```text id="f4r7x1"
Millions of documents
```

you can't realistically put everything into the context.

So RAG remains extremely useful.

---

# 15. Hybrid approach

You can combine them:

```text id="x8m3q7"
Huge Knowledge Base
       ↓
     RAG
       ↓
Relevant Documents
       ↓
Large Context
       ↓
LLM
```

This gives the model:

> A large amount of **relevant** information rather than a huge amount of irrelevant information.

---

# 16. Agents

Now let's move to the fourth concept.

An **agent** is an LLM-based system that can decide what actions to take.

For example:

```text id="b4k8p2"
User:
"Find the latest sales numbers,
compare them with last year,
calculate the percentage growth,
and prepare a summary."
```

The system might decide:

```text id="d7m2x9"
1. Search latest sales data
2. Search previous year's data
3. Calculate growth
4. Analyze results
5. Write summary
```

The key idea is:

> **The system decides what steps/tools to use.**

---

# 17. RAG vs Agent

RAG is primarily:

```text id="q1n5s7"
Retrieve information
      ↓
Generate answer
```

An agent is:

```text id="m8k3v2"
Goal
 ↓
Think/plan
 ↓
Choose tool
 ↓
Observe result
 ↓
Decide next action
 ↓
Repeat
 ↓
Final answer
```

An agent may use RAG as one of its tools.

---

# 18. Agentic RAG

Now combine them.

```text id="v5k2r8"
                       User
                        ↓
                      Agent
                        ↓
             ┌──────────┼──────────┐
             ↓          ↓          ↓
           RAG        Search       API
             ↓          ↓          ↓
             └──────────┼──────────┘
                        ↓
                     Agent
                        ↓
                     Answer
```

The agent decides:

> "I need to search the knowledge base."

Then:

> "I need another search."

Then:

> "I need to call the sales API."

Then:

> "I have enough information."

Then it answers.

---

# 19. The four-way comparison

Here's the mental model I want you to remember:

| Technology       | Main purpose                       |
| ---------------- | ---------------------------------- |
| **RAG**          | Give the model external knowledge  |
| **Fine-tuning**  | Change model behavior              |
| **Long context** | Give the model broad context       |
| **Agent**        | Let the model decide actions/tools |

---

# 20. Concrete examples

### "What's our refund policy?"

```text id="p7k2m9"
RAG ✓
```

### "Always output customer tickets as JSON."

```text id="x4n8q1"
Fine-tuning ✓
```

### "Analyze this entire 400-page contract."

```text id="c9m3r7"
Long Context ✓
```

### "Research three websites, compare the results, calculate the difference, and email me."

```text id="v2k6p5"
Agent ✓
```

---

# 21. More realistic combinations

Real systems often look like:

### RAG + Agent

```text id="e8q4m1"
Agent
 ↓
RAG
 ↓
Knowledge
```

### RAG + Long Context

```text id="j6p2s9"
RAG
 ↓
Relevant Documents
 ↓
Large Context
 ↓
LLM
```

### RAG + Fine-tuning

```text id="a3m7x5"
RAG
 ↓
Context
 ↓
Fine-Tuned Model
```

### Agent + RAG + APIs

```text id="k8r4v2"
                 Agent
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
      RAG         API        Search
```

This is increasingly common in enterprise AI.

---

# 22. A decision framework

When you're designing an LLM application, ask these questions.

### Question 1

> Does the model need external/private knowledge?

If yes:

```text id="h2x7m4"
Consider RAG
```

### Question 2

> Does the information change frequently?

If yes:

```text id="u8q3n6"
RAG/API
```

rather than trying to encode it into model parameters.

### Question 3

> Do I need to change the model's behavior?

If yes:

```text id="p5m9k2"
Consider fine-tuning
```

### Question 4

> Does the model need to understand a relatively large document at once?

If yes:

```text id="v7x4c8"
Consider long context
```

### Question 5

> Does the model need to perform multiple actions or decide which tools to use?

If yes:

```text id="n3k8s1"
Consider an agent
```

---

# 23. Production RAG starts here

Now we've reached an important point in your learning path.

You understand:

```text id="r8m3q6"
What RAG is
       ↓
How embeddings work
       ↓
How retrieval works
       ↓
Dense / Sparse / Hybrid
       ↓
Reranking
       ↓
Query transformation
       ↓
RAG failure modes
       ↓
RAG evaluation
       ↓
Advanced RAG
       ↓
RAG vs Fine-tuning
       ↓
RAG vs Long Context
       ↓
RAG vs Agents
```

So now we can start talking about **production RAG engineering**.

---

# 🚀 Lesson 6: Production RAG Architecture

This is where we'll move from:

> "How does RAG work?"

to:

> **"How do I design a RAG system that can actually run in production?"**

We'll cover:

### 1. Document ingestion pipelines

```text
PDF
Word
HTML
Database
API
     ↓
Parsing
     ↓
Cleaning
     ↓
Chunking
     ↓
Metadata
     ↓
Embedding
     ↓
Index
```

### 2. Updating documents

How do you handle:

```text
New document
Updated document
Deleted document
Version 2
Expired document
```

without rebuilding the entire vector database?

### 3. Multi-tenancy

For example:

```text
Company A
 ├── Documents
 └── Users

Company B
 ├── Documents
 └── Users
```

Company A must **never** retrieve Company B's documents.

### 4. Access control

If Alice can access:

```text
Document A
Document B
```

but Bob can only access:

```text
Document A
```

retrieval itself must respect those permissions.

### 5. Latency

We'll break down:

```text
Query processing       50ms
Embedding              30ms
Vector search          50ms
Reranking             100ms
LLM                    2s
────────────────────────────
Total                  ~2.2s
```

and discuss how to optimize it.

### 6. Cost

We'll look at:

```text
Embedding cost
Vector DB cost
Reranking cost
LLM token cost
Caching
```

### 7. Observability

We'll learn how to trace:

```text
User Query
   ↓
Retrieved chunks
   ↓
Scores
   ↓
Reranker
   ↓
Prompt
   ↓
LLM
   ↓
Answer
```

This is essential when debugging production RAG.

### 8. Security

We'll cover:

```text
Prompt injection
Data leakage
Tenant isolation
Permission-aware retrieval
Malicious documents
PII
Tool abuse
```

Once we finish Lesson 6, you'll have a pretty complete **production-level conceptual understanding of RAG**.

Then we can move into the implementation phase you wanted to postpone: **building RAG from scratch, followed by frameworks and real-world architecture.**
