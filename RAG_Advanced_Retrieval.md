Absolutely. Let's move into **Advanced Retrieval**. This is where RAG starts becoming much more realistic.

# RAG — Lesson 2: Advanced Retrieval

So far, our RAG system looks like:

```text
User Query
    ↓
Embedding
    ↓
Vector Search
    ↓
Top-K Chunks
    ↓
LLM
    ↓
Answer
```

This is called **basic/naive RAG**.

It works, but real-world RAG systems often need much more.

---

# 1. Why basic vector search isn't enough

Imagine your knowledge base contains:

```text
10,000 documents
100,000 chunks
```

User asks:

> "What is the refund policy for order #ORD-98231?"

A vector search might retrieve documents about:

```text
Refund policy
Order cancellation
Return policy
Payment policy
Customer support
```

But perhaps the user specifically needs information about:

```text
ORD-98231
```

That's an **exact identifier**.

Semantic similarity isn't always the best tool for exact strings.

This gives us our first important concept.

---

# 2. Dense Retrieval

The vector-search approach we've learned is usually called **dense retrieval**.

The flow is:

```text
Query
 ↓
Embedding Model
 ↓
Dense Vector
 ↓
Vector Database
 ↓
Similarity Search
 ↓
Results
```

For example:

```text
"How much vacation do employees get?"
              ↓
       [0.81, 0.32, ...]
              ↓
       Vector Search
              ↓
"Employees receive 20 days of annual leave."
```

The strength of dense retrieval is **semantic understanding**.

It can recognize:

```text
vacation ≈ annual leave
car ≈ automobile
purchase ≈ buy
```

even when the exact words don't match.

---

# 3. Sparse Retrieval

Another approach is **sparse retrieval**.

Instead of representing the entire meaning as a dense vector, it focuses heavily on words/tokens and their importance.

A famous algorithm is:

## BM25

BM25 is widely used for keyword-based information retrieval.

Conceptually:

```text
Query
 ↓
Keywords
 ↓
Search documents
 ↓
Term relevance
 ↓
Results
```

For example:

```text
Query:
"ORD-98231 refund"

Document A:
"Refund policy for ORD-98231..."
          ↑
      strong match
```

This can be excellent for:

* Order IDs
* Product codes
* Error codes
* Names
* Technical terms
* Exact phrases
* Rare words

---

# 4. Dense vs Sparse Retrieval

This distinction is extremely important.

### Dense retrieval

Good at:

> **Meaning**

```text
"How much vacation do I get?"
        ↓
"Employees receive 20 days of annual leave."
```

### Sparse retrieval

Good at:

> **Exact words**

```text
"Error XJ-4921"
        ↓
"Error XJ-4921"
```

Think:

```text
Dense = semantic similarity
Sparse = lexical/keyword matching
```

Neither is universally better.

They solve different problems.

---

# 5. Hybrid Search

Now we combine them.

```text
                 Query
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
   Dense Retrieval    Sparse Retrieval
   (Vector Search)        (BM25)
          ↓                 ↓
       Results            Results
          └────────┬────────┘
                   ↓
             Combine Results
                   ↓
                Rerank
                   ↓
             Final Context
```

This is called **hybrid search**.

It's one of the most important techniques in production RAG.

---

# 6. Example of hybrid search

Suppose the user asks:

> "What does error XJ-4921 mean?"

### Dense search might find:

```text
Document A
"Database connectivity errors..."

Document B
"Network connection failures..."

Document C
"System errors and troubleshooting..."
```

They're semantically related.

But perhaps the exact error code appears in:

```text
Document D
"XJ-4921 occurs when the authentication token expires."
```

Sparse search is much more likely to find Document D because of the exact string.

So:

```text
Dense Search
      +
Sparse Search
      ↓
Better candidate set
```

This is the major motivation for hybrid retrieval.

---

# 7. Metadata Filtering

Now let's introduce another extremely important technique.

Remember that we can store metadata with chunks:

```text
Chunk:
"Employees receive 20 days of annual leave."

Metadata:
{
  document: "employee_handbook.pdf",
  department: "HR",
  country: "India",
  year: 2026,
  section: "Leave Policy"
}
```

We can use this metadata during retrieval.

Suppose the user asks:

> "What is the 2026 leave policy for employees in India?"

Instead of searching the entire database:

```text
100,000 chunks
```

we can filter first:

```text
country = India
year = 2026
department = HR
```

Then search:

```text
100,000 chunks
      ↓
Metadata filter
      ↓
5,000 chunks
      ↓
Vector search
      ↓
Top 10
```

This can improve both **accuracy and performance**.

---

# 8. Metadata is more powerful than it looks

You might store:

```text
{
  document_id: "doc_123",
  filename: "employee_handbook.pdf",
  page: 42,
  section: "Leave Policy",
  department: "HR",
  country: "India",
  language: "English",
  created_at: "2026-01-10",
  version: "3.0"
}
```

Now queries can be constrained.

For example:

> "What did the policy say in 2024?"

```text
year = 2024
```

Or:

> "What does the engineering handbook say?"

```text
department = Engineering
```

This is called **metadata filtering**.

---

# 9. Top-K isn't always enough

Earlier we had:

```text
Vector Search
 ↓
Top 5
```

But there's a subtle problem.

Suppose:

```text
Chunk A → 0.91
Chunk B → 0.90
Chunk C → 0.89
Chunk D → 0.88
Chunk E → 0.87
```

They look good.

But similarity scores don't necessarily mean:

> "These are the five best chunks for answering the question."

They only tell us how similar the chunks are according to the retrieval model.

This leads to **reranking**.

---

# 10. What is reranking?

Reranking is a second stage of retrieval.

Instead of:

```text
Query
 ↓
Vector Search
 ↓
Top 5
 ↓
LLM
```

we can do:

```text
Query
 ↓
Vector Search
 ↓
Top 20
 ↓
Reranker
 ↓
Top 5
 ↓
LLM
```

Why retrieve 20 first?

Because we want **high recall**.

Then the reranker can carefully decide which candidates are most relevant.

---

# 11. What does a reranker do?

A reranker looks at the actual relationship between:

```text
Query + Candidate Document
```

For example:

```text
Query:
"What is the parental leave eligibility?"

Candidate A:
"Employees receive 20 days of annual leave."

Candidate B:
"Employees become eligible for parental leave after
12 months of continuous employment."
```

The reranker might produce:

```text
Candidate A → 0.21
Candidate B → 0.96
```

So Candidate B moves to the top.

The important idea:

> **The initial retriever finds candidates. The reranker orders those candidates more carefully.**

---

# 12. Recall vs Precision

This introduces two important information-retrieval concepts.

### Recall

> Did we retrieve the information we needed?

Suppose the correct chunk exists in the database.

If we retrieve 20 candidates and the correct chunk is among them:

```text
Recall = good
```

### Precision

> How many of the retrieved results are actually relevant?

Suppose we retrieve 20 chunks and only 2 are useful:

```text
Precision = poor
```

So a common architecture is:

```text
Retriever
 ↓
Optimize for recall
 ↓
Large candidate set
 ↓
Reranker
 ↓
Optimize for precision
 ↓
Small high-quality set
```

This is a very important production pattern.

---

# 13. The two-stage retrieval architecture

You should remember this:

```text
                    Query
                      ↓
              Candidate Retrieval
                      ↓
                  Top 20-100
                      ↓
                   Reranker
                      ↓
                    Top 3-10
                      ↓
                     LLM
```

The exact numbers depend on the application.

The key concept is:

> **Retrieve broadly, then rank carefully.**

---

# 14. Similarity threshold

Another technique is a **similarity threshold**.

Suppose we have:

```text
Chunk A → 0.94
Chunk B → 0.91
Chunk C → 0.87
Chunk D → 0.42
Chunk E → 0.31
```

Instead of saying:

> Always return 5 chunks.

we could say:

> Only return chunks above a certain relevance threshold.

For example:

```text
threshold = 0.80
```

Then:

```text
A → 0.94 ✓
B → 0.91 ✓
C → 0.87 ✓
D → 0.42 ✗
E → 0.31 ✗
```

This can prevent obviously irrelevant information from reaching the LLM.

However, **similarity scores aren't universally calibrated across models or datasets**, so blindly choosing one global threshold can be dangerous.

---

# 15. Query rewriting

Now let's look at the query itself.

Users don't always ask questions that are good search queries.

Suppose the conversation is:

```text
User:
"What are the company's parental leave benefits?"

Assistant:
"Employees receive 16 weeks..."

User:
"What about eligibility?"
```

The query:

```text
"What about eligibility?"
```

is ambiguous.

A query rewriting component can transform it into:

```text
"What are the eligibility requirements
for the company's parental leave policy?"
```

Then retrieval happens.

```text
Conversation
    ↓
Query Rewriter
    ↓
Better Search Query
    ↓
Retriever
```

This is especially useful for conversational RAG.

---

# 16. Query rewriting doesn't change the user's question

This is subtle.

The system isn't supposed to invent new requirements.

It's trying to make the **search query explicit**.

For example:

```text
Conversation:
"What is the refund policy?"

"What about international orders?"
```

could become:

```text
"What is the refund policy for international orders?"
```

The final answer is still generated based on retrieved evidence.

---

# 17. Multi-query retrieval

Sometimes one query doesn't capture all aspects of a question.

Suppose the user asks:

> "What are the costs, benefits, and eligibility requirements of the company's health insurance?"

Instead of one search:

```text
Query
 ↓
Search
```

we can generate several:

```text
Original Query
      ↓
 ┌────┼────┐
 ↓    ↓    ↓
Q1   Q2   Q3
 ↓    ↓    ↓
Search Search Search
 └────┼────┘
      ↓
Combine Results
      ↓
Rerank
      ↓
LLM
```

For example:

```text
Q1:
"What is the cost of company health insurance?"

Q2:
"What benefits are included in company health insurance?"

Q3:
"What are the eligibility requirements?"
```

This can improve **recall**.

---

# 18. Multi-query vs query rewriting

Don't confuse them.

### Query rewriting

One query becomes a better query:

```text
Q
 ↓
Better Q
```

### Multi-query

One query becomes multiple queries:

```text
Q
 ↓
Q1 + Q2 + Q3
```

The goal of both is better retrieval, but the mechanisms are different.

---

# 19. Reciprocal Rank Fusion

When we have multiple retrieval systems, we need a way to combine their rankings.

For example:

```text
Dense Search:

A
B
C
D
```

and:

```text
BM25:

C
A
E
B
```

How do we combine these?

One popular technique is:

**Reciprocal Rank Fusion (RRF)**.

The basic intuition is:

> A document that appears highly ranked across multiple retrieval methods should receive a strong combined ranking.

Conceptually:

```text
Dense ranking
      +
BM25 ranking
      ↓
     RRF
      ↓
Combined ranking
```

You don't need to memorize the formula yet.

Just remember:

> **RRF is one way to combine rankings from multiple retrieval strategies.**

---

# 20. Parent-Child Retrieval

Here's another useful pattern.

Suppose we have:

```text
Parent Document
      │
      ├── Child Chunk 1
      ├── Child Chunk 2
      ├── Child Chunk 3
      └── Child Chunk 4
```

We create embeddings for the small child chunks.

Why?

Small chunks can provide precise retrieval.

But after finding a relevant child chunk, we can return the larger parent context.

```text
Query
 ↓
Search child chunks
 ↓
Child Chunk 3 matches
 ↓
Retrieve parent
 ↓
Larger context
 ↓
LLM
```

So we get:

```text
Precise retrieval
      +
More context
```

This is often better than simply making every chunk huge.

---

# 21. The context problem

Consider this chunk:

```text
"The policy was introduced in 2024."
```

If retrieved alone, the LLM might ask:

> Which policy?

Maybe the preceding section says:

```text
Remote Work Policy
```

But the chunk lost that context.

This leads to another technique:

## Contextual Retrieval

Before indexing, we can enrich a chunk with relevant surrounding context.

Conceptually:

```text
Original chunk:

"The policy was introduced in 2024."
```

could become something like:

```text
Context:
"This section describes the company's Remote Work Policy."

Chunk:
"The policy was introduced in 2024."
```

The indexed representation becomes more informative.

---

# 22. Dense + Sparse + Reranking

Now our system is becoming much more sophisticated:

```text
                         User Query
                              ↓
                       Query Processing
                              ↓
                ┌─────────────┴─────────────┐
                ↓                           ↓
         Dense Retrieval              Sparse Retrieval
         Vector Search                    BM25
                ↓                           ↓
                └─────────────┬─────────────┘
                              ↓
                       Candidate Set
                              ↓
                             RRF
                              ↓
                          Reranker
                              ↓
                         Top Results
                              ↓
                           Context
                              ↓
                             LLM
                              ↓
                           Answer
```

This is much closer to what you'd find in a serious RAG application.

---

# 23. Basic RAG vs Advanced RAG

Let's compare them.

| Basic RAG           | Advanced RAG                      |
| ------------------- | --------------------------------- |
| Vector search       | Dense + sparse                    |
| Simple chunking     | Structure/semantic chunking       |
| Top-K               | Candidate retrieval + reranking   |
| Single query        | Query rewriting / multi-query     |
| No/limited metadata | Metadata filtering                |
| One chunk size      | Parent-child strategies           |
| Basic context       | Contextual retrieval              |
| Simple prompt       | Context selection                 |
| No evaluation       | Retrieval + generation evaluation |

---

# 24. A practical example

Suppose we're building a **company policy assistant**.

User asks:

> "What is the maternity leave policy for employees in India in 2026?"

A naive system:

```text
Question
 ↓
Embedding
 ↓
Vector Search
 ↓
Top 5
 ↓
LLM
```

A better system:

```text
Question
 ↓
Query processing
 ↓
Extract metadata:
 country = India
 year = 2026
 policy = maternity leave
 ↓
Metadata filtering
 ↓
 ┌──────────────┬──────────────┐
 ↓              ↓
Vector Search  BM25
 ↓              ↓
 └───────┬──────┘
         ↓
     Candidate Set
         ↓
        RRF
         ↓
      Reranker
         ↓
      Top 5 chunks
         ↓
   Parent/context expansion
         ↓
        LLM
         ↓
      Answer
```

Notice how much more work happens **before the LLM**.

That's a major lesson:

> **A high-quality RAG system is often more about retrieval engineering than about prompting the LLM.**

---

# 25. An important production principle

A common beginner reaction to a bad RAG answer is:

> "Let's improve the prompt."

Sometimes the prompt is the problem.

But often the real problem is:

```text
Wrong chunks
    ↓
LLM receives wrong context
    ↓
Bad answer
```

No amount of prompt engineering can reliably compensate for completely missing evidence.

Think:

```text
Good retrieval
      +
Good context
      +
Good generation
      =
Good RAG
```

---

# 26. The advanced retrieval mental model

You can now upgrade your original mental model.

### Basic:

```text
Query
 ↓
Embedding
 ↓
Vector Search
 ↓
Top-K
 ↓
LLM
```

### Advanced:

```text
                         Query
                           ↓
                    Query Processing
                           ↓
                 ┌─────────┴─────────┐
                 ↓                   ↓
            Dense Search         Sparse Search
            Vector Search            BM25
                 ↓                   ↓
                 └─────────┬─────────┘
                           ↓
                    Candidate Set
                           ↓
                     Result Fusion
                           ↓
                       Reranker
                           ↓
                  Metadata / Filters
                           ↓
                   Context Expansion
                           ↓
                    Final Context
                           ↓
                          LLM
                           ↓
                        Answer
```

---

# 27. What you've learned so far

At this point, your RAG knowledge is roughly:

```text
                 RAG
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
    INDEXING             RETRIEVAL
        │                   │
        ↓                   ↓
    Documents            Query
        ↓                   ↓
    Chunking            Embedding
        ↓                   ↓
    Embeddings       Dense Retrieval
        ↓                   ↓
  Vector Database     Sparse Retrieval
                            ↓
                       Hybrid Search
                            ↓
                         Reranking
                            ↓
                    Context Selection
                            ↓
                            LLM
                            ↓
                          Answer
```

That's a strong foundation.

---

# 🚀 Next Lesson: RAG Failure Modes

Before jumping into frameworks like LangChain or LlamaIndex, I recommend one more conceptual lesson.

We'll study **why RAG systems fail**, including:

1. **Bad chunking**
2. **Wrong embeddings**
3. **Poor retrieval**
4. **Lost context**
5. **Too many chunks**
6. **Too few chunks**
7. **Semantic similarity mismatch**
8. **Retrieval of conflicting documents**
9. **Hallucination despite correct retrieval**
10. **Stale documents**
11. **Duplicate chunks**
12. **Long-context problems**
13. **Multi-hop questions**
14. **"I don't know" / no-answer handling**
15. **Security problems such as prompt injection in retrieved documents**

Then we'll learn how to **evaluate RAG properly**—with metrics such as **Recall@K, Precision@K, MRR, NDCG, faithfulness, answer relevance, and groundedness**.

After that, we'll be ready to start **building RAG from scratch in Python**, without hiding the important pieces behind a framework.
