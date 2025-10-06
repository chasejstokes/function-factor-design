# Text-Aware Visualization Design

This project explores how to use LLM's automatically design visualizations to fit different patterns of text use. 

## Intention

Text elements play a critical role in framing, explaining, and shaping how viewers interpret data. However, text in visualization has historically been understudied compared to graphical encodings.  

This project implements a workflow where LLMs can:

1. **Interpret text functions** using factor loadings and definitions.
2. **Generate design briefs** for visualization redesigns based on factor analysis.
3. **Render redesigned charts** that highlight or minimize certain text functions.

## Background

This work is informed by the paper:  
**"An Analysis of Text Functions in Information Visualization"** by Chase Stokes, Anjana Arunkumar, Marti Hearst, and Lace Padilla.  

The paper identifies **ten text functions** (e.g., identify mappings, compare values, present context) and organizes them into **four higher-level factors**:

- Attribution and Variables  
- Annotation-Centric Design  
- Visual Embellishments  
- Narrative Framing  

By connecting factor loadings to visualization redesign, we can explore how LLMs might systematically adjust or implement the role of text in visualization design.

## Current Scope

- Prototype scripts for calling GPT-5 and Gemini APIs.
- Early integration with Python workflows.

---

This repository is a research and prototyping environment for bridging **information visualization** and **LLM-based design assistance**.
