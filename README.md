# Text-Aware Visualization Redesign

This project explores how to automatically **extract, analyze, and redesign visualization text** using large language models (LLMs) such as **GPT-5** and **Gemini**.

## Intention

Text elements play a critical role in framing, explaining, and shaping how viewers interpret data. However, text in visualization has historically been understudied compared to graphical encodings.  

This project implements a workflow where LLMs can:

1. **Extract chart data and text** (e.g., titles, captions, annotations).
2. **Interpret text functions** using factor loadings and definitions.
3. **Generate design briefs** for visualization redesigns based on factor analysis.
4. **Render redesigned charts** (e.g., in D3.js) that highlight or minimize certain text functions.

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
- JSON schemas for structured extraction of chart data and text.
- Early integration with Python workflows.

---

This repository is a research and prototyping environment for bridging **information visualization** and **LLM-based design assistance**.
