# Duke Atlas Chatbot Project Documentation

![CI/CD Status](https://github.com/Duke-CREATE/registrar-ai-tool/actions/workflows/heroku-deploy.yml/badge.svg)

Project Lead: Daniel Medina

## Problem Statement
Duke Students often find the course registration process challenging and cumbersome. The system currently in place can be confusing and lacks intuitive interaction, leading to a frustrating experience that can impact their academic journey.

## Purpose
The purpose of the Duke Atlas Chatbot is to simplify the course registration process for Duke University students. By providing a user-friendly chat interface, the chatbot aims to offer real-time assistance, answer queries related to course information and registration, and guide students through the registration steps more efficiently.

## General Architecture

![Architecture Diagram](arch-diagram.png)

### Backend
- **Technology**: Flask (Python)
- **Main Features**:
  - **API Routing**: Utilizes Flask Blueprints to handle routing, making the application modular and scalable.
  - **OpenAI Integration**: Leverages OpenAI's GPT model to generate intelligent and context-aware responses based on user queries.
  - **Redis Caching**: Implements Redis for caching conversation threads to enhance performance and maintain state across the session.
  - **Data Storage**: Connects to MongoDB for persistent storage of user data and logs, ensuring that data retrieval is efficient and secure.

### Frontend
- **Technology**: Next.js (React framework)
- **Main Features**:
  - **Interactive UI**: Offers a dynamic chat interface that is responsive and accessible to users.
  - **State Management**: Utilizes React hooks to manage state locally, including messages, user inputs, and interaction history.
  - **Session Continuity**: Employs local storage to maintain session state across page reloads, improving user experience.

## Deployment
- **Heroku**:
  - Used for deploying the backend service.
  - Automates deployments using GitHub Actions which handle Docker containerization and push to Heroku.
- **Vercel**:
  - Deploys the Next.js frontend.
  - Ensures seamless CI/CD pipeline integration for frontend changes, directly linking GitHub for continuous deployment.
 
  - ## AI-Driven Response Generation

The AI component of the Duke Atlas Chatbot employs the Retrieval-Augmented Generation (RAG) model to deliver intelligent, context-aware responses. This section details the integration of RAG and the architecture supporting it.

### Overview of RAG
RAG combines the power of transformer-based language models with a neural retrieval mechanism. This approach enables the system to dynamically retrieve relevant documents and use this context to generate responses. For the Duke Atlas Chatbot, RAG enhances the ability to provide precise and informative answers to user queries about course registration and details.

### Data Structuring and Retrieval
- **Vector Databases**:
  - **Course Information Database**: This database stores structured data on courses. The data was already segmented by individual courses when provided, which made the setup of this vector database straightforward.
  - **Registration Logistics Database**: This database contains information regarding registration procedures, scraped from the Duke registration website. Unlike the course information, this data required manual chunking to ensure that the stored segments are coherent and contextually relevant.

### Query Processing and Embedding
- **User Query Embedding**: Upon receiving a user query, the system first embeds the query using a dedicated endpoint provided by Hugging Face's Gist embedding model. This embedding process converts the textual query into a vector form that can be used for efficient similarity search.
- **Decision Logic for Database Querying**: Based on the type of question identified from the user's input on the frontend—either a course-related query or a registration logistics query—the system determines which vector database to query.
- **MongoDB Atlas Search**: Both vector databases leverage MongoDB Atlas's search capabilities for similarity searching. This setup enables the chatbot to quickly find the most relevant information segments in response to the user's embedded query.

### Response Generation
Once the relevant information is retrieved from the appropriate vector database, RAG utilizes this context to generate a coherent and contextually appropriate response. This response is then sent back to the user, providing them with precise information tailored to their specific query.

### Benefits of RAG in Duke Atlas
The integration of RAG into the Duke Atlas Chatbot ensures that responses are not only based on pre-defined templates but are dynamically generated based on the most relevant and up-to-date information available. This approach significantly improves the accuracy and helpfulness of the chatbot, making it a robust tool for assisting Duke students with their course registration needs.

This AI-driven system not only enhances user experience by providing tailored information but also streamlines the process of managing and updating content, as the retrieval mechanisms automatically adjust to changes in the underlying data.

## Security Measures
- **HTTPS**: Enforces HTTPS to secure the data in transit, protecting it from interception by malicious actors.
- **Authentication**: Plans to implement OAuth for user authentication to ensure that access to the user-specific data is secure and personalized.

## Future Enhancements
- **AI Training**: To improve response accuracy and context understanding by training the model specifically on academic and registration-related queries.
- **Input Classification**: To improve user experience, implement an ML model that classifies the type of input such that the system can respond accordingly.
- **User Personalization**: Introduction of personalized responses based on the user’s academic history and preferences.
