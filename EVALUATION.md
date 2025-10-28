## Test Output (Actual System Results on the Terminal)

This document demonstrates the value of the RAG (Retrieval-Augmented Generation) pipeline by comparing its performance against the base llama3.2 model. The goal is to test the system's ability to handle specific queries and to mitigate common LLM failures such as hallucination and factual errors.

Each query was run against:

1. Base LLM (No RAG): The llama3.2 model, to test its baseline knowledge.

2. RAG Pipeline: My system (ChromaDB + nomic-embed-text + llama3.2), which was grounded in the wikipedia document.

Terminal Output:"""
(base) danielmendoza@Daniels-MacBook-Pro-3 RAG_Cornerstone % python RAG.py


**Testing RAG system**


Query 1

 Query: Who coined the term 'machine learning' in 1959?

 Retrieving relevant chunks.
 Retrieved 3 chunks

 Chunk 1: Statistics and mathematical optimisation (mathematical programming) methods comprise the
 foundation...
 Chunk 2: The earliest machine learning program was introduced in the 1950s when Arthur Samuel invented a
 com...
 Chunk 3: and machine learning algorithms work under nodes, or artificial neurons used by computers to
 commun...

 Generating answer

 ANSWER:
 Arthur Samuel, an IBM employee and pioneer in computer gaming and artificial intelligence, coined the term 'machine learning' in 1959.


Query 2

 Query: What is Tom M. Mitchell's formal definition of machine learning?

 Retrieving relevant chunks.
 Retrieved 3 chunks

 Chunk 1: Tom M. Mitchell provided a widely quoted, more formal definition of the algorithms studied in the
 m...
 Chunk 2: Machine learning

 Machine learning (ML) is a field of study in artificial intelligence concerned wi...
 Chunk 3: Statistics and mathematical optimisation (mathematical programming) methods comprise the
 foundation...

 Generating answer

 ANSWER:
 Tom M. Mitchell provided a widely quoted, more formal definition of the algorithms studied in the machine learning field: "A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P if its performance at tasks in T, as measured by P, improves with experience E."


Query 3

 Query: What was the 'Cybertron' machine developed by Raytheon Company in the 1960s?

 Retrieving relevant chunks.
 Retrieved 3 chunks

 Chunk 1: By the early 1960s, an experimental "learning machine" with punched tape memory, called Cybertron,
 ...
 Chunk 2: Neuromorphic computing

 Neuromorphic computing refers to a class of computing systems designed to e...
 Chunk 3: Relationships to other fields

 Artificial intelligence

 As a scientific endeavour, machine learnin...

 Generating answer

 ANSWER:
 By the early 1960s, an experimental "learning machine" with punched tape memory, called Cybertron, had been developed by Raytheon Company to analyse sonar signals, electrocardiograms, and speech patterns using rudimentary reinforcement learning.



**Testing without using the RAG systems**


Query 1

The term "Machine Learning" was indeed coined by Arthur Samuel in 1956 (not 1959), not by one person but rather by two people, 

1. Arthur Samuel (in his paper of 1957) who proposed a type of programming called "Learning Machine", and 
2. Frank Rosenblatt (in his book of 1960) who wrote about the concept in the context of neural networks.

However, after both, John McCarthy coined this term in a conference at Dartmouth in 1959


Query 2

Tom M. Mitchell, an American computer scientist, provided a widely accepted and influential formal definition of machine learning in his 1997 book "Machine Learning". According to him:

"Machine learning is a subfield of artificial intelligence that provides systems the ability to automatically improve their performance on a task without being explicitly programmed for that task."

In other words, Mitchell defines machine learning as a type of artificial intelligence where algorithms learn from data and improve their performance over time through experience, rather than relying solely on explicit programming.


Query 3

I couldn't find any information on a "Cybertron" machine developed by Raytheon Company in the 1960s. However, I did find that Cybernetics Corporation was a real company that developed various technologies and systems in the mid-20th century.

One of the most notable developments from Cybernetics Corporation is the "Cybernetron", which was an experimental particle accelerator built in the late 1950s. It was designed to accelerate charged particles to high speeds for research purposes.
"""



Query 1 (Arthur Samuel):

* Why the Base LLM Failed: The model's general knowledge was a "mess" of conflicting facts, dates, and names. It tried to average all of them and produced a contradictory, incorrect answer.

* Why RAG Succeeded: The RAG system retrieved the one correct fact from the document, forcing the LLM to ignore its muddled internal knowledge and provide the precise answer.

Query 2 (Tom M. Mitchell):

Why the Base LLM Failed: The model hallucinated. It didn't know the specific quote, so it invented a plausible-sounding definition that was completely wrong.

Why RAG Succeeded: The RAG system ensured faithfulness. By retrieving the exact quote, it gave the LLM the correct information and forced it to use that text, preventing the hallucination.

Query 3 ('Cybertron'):

Why the Base LLM Failed: This was a simple knowledge gap. The term was too niche and was not in the model's training data, so it correctly admitted it didn't know (but then guessed wrong).

Why RAG Succeeded: The RAG system augmented the model's knowledge. It found the obscure fact in the document and "handed" it to the LLM, allowing it to answer a question it knew nothing about.