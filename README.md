# CinemaAI

CinemaAI is designed to help movie enthusiasts discover and discuss films they'll love. Offering real-time chat capabilities, CinemaAI allows users to interact with an AI for personalized movie recommendations, filter options by IMDb scores, directors, release dates, and much more.

# CinemaAI

Welcome to **CinemaAI** – your ultimate AI-powered companion for discovering and discussing movies! Whether you're a movie enthusiast or a developer exploring AI and web technologies, CinemaAI is designed to offer an immersive and intuitive experience. Get personalized movie recommendations, explore detailed movie data, and interact with our advanced AI chatbot seamlessly.

![CinemaAI Logo](./app/static/cinemaAI_logo.webp)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
  - [Interacting with CinemaAI](#interacting-with-cinemaai)
  - [Exploring the Playground](#exploring-the-playground)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Personalized Movie Recommendations**: Engage with our AI to receive movie suggestions tailored to your preferences.
- **Advanced Search Capabilities**: Filter movies by title, genres, year, director, and cast members.
- **Real-time Interactions**: Enjoy quick and interactive responses from our AI for a seamless user experience.
- **Detailed Movie Information**: Access comprehensive details about movies, including ratings, awards, plot summaries, and more.
- **Interactive Playground**: Experiment with AI capabilities through our intuitive web interface.
- **Scalable and Modular Design**: Built with a modular architecture to support future enhancements and scalability.

## Technologies Used

CinemaAI is powered by a robust stack of modern technologies:

### Backend

- **FastAPI**: A modern, high-performance web framework for building APIs with Python.
- **Pydantic**: Provides data validation and settings management using Python type annotations.
- **MongoDB**: A flexible, NoSQL database for storing movie data and chat logs.
- **OpenAI API**: Integrates OpenAI's powerful language models to enable the AI chat functionality.

### Frontend

- **HTML5**: Interrface providing the structure and content.
- **CSS3**: Defines the visual styling and layout of our application.
- **JavaScript**: Adds basic interactivity and dynamic elements to the user experience.
- **Jinja2 Templates**: Used for rendering dynamic HTML pages within FastAPI.

### DevOps

- **Docker**: For containerization, simplifying deployment and scaling of the application.
- **GitHub Actions**: Enables continuous integration and deployment workflows.

## Demo

Experience CinemaAI in action: [CinemaAI Live Demo](#) (Link to a live demo or video walkthrough)

![CinemaAI Screenshot](./app/static/screenshot.png)

## Getting Started

Follow these steps to set up and run CinemaAI on your local machine.

### Prerequisites

- **Python 3.12.4+**: Download and install the latest version from [Python's official site](https://www.python.org/downloads/).
- **MongoDB**: Set up a MongoDB instance, either locally with a docker image or via [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). Utilizing MongoDB Compass as a GUI may also come in handy.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/RGimenez1/CinemaAI.git
   cd CinemaAI
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables**:
   Create a `.env` file in the root directory with the following configuration:

   ```env
   MONGO_USERNAME=<your_mongo_username>
   MONGO_PASSWORD=<your_mongo_password>
   MONGO_CLUSTER_URL=<your_mongo_cluster_url>
   MONGO_DB_NAME=<your_mongo_database_name>
   OPENAI_API_KEY=<your_openai_api_key>
   OPENAI_MODEL=<openai_model_name>
   SYSTEM_PROMPT_VERSION=<default_system_prompt_version>
   TOOL_VERSION=<default_tool_version>
   ```

2. **Update Settings**:
   Adjust any additional settings in `app/core/config.py` to fit your environment.

## Usage

### Running the Application

1. **Start the FastAPI Server**:

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the Application**:

   - Open your browser and go to `http://localhost:8000`.

3. **Add your OpenAI API Key**:

   - Add OpenAI API Key and chat away!

   Important factors:
   1- Model used is currently GPT-4o. May be upgraded as new models are released.
   2- We do **NOT** store, track, use or are responsible for api keys in ANY way, shape or form.
   3- Monitor your usage on OpenAIs platform.

### API Endpoints

Explore the key API endpoints:

- **Movie Search**: `GET /api/movies`

  - Search for movies using filters like title, genres, year, director, and cast member.
  - Example:
    ```bash
    curl -X GET "http://localhost:8000/api/movies?title=Inception&year=2010" -H "accept: application/json"
    ```

- **Chat with AI**: `POST /api/chat`

  - Engage with CinemaAI for personalized recommendations.
  - Example:
    ```bash
    curl -X POST "http://localhost:8000/api/chat" -H "Content-Type: application/json" -d '{"context_id": "1234", "message": "Recommend me a movie like Inception"}'
    ```

- **System Prompt**: `GET /api/system-prompt`
  - Fetch the current system prompt version.
  - Example:
    ```bash
    curl -X GET "http://localhost:8000/api/system-prompt" -H "accept: application/json"
    ```

For a complete list of endpoints and their usage, visit the interactive API docs at `http://localhost:8000/docs`.

### Interacting with CinemaAI

- **Chat Interface**: Use the `/api/chat` endpoint to converse with the AI and get personalized movie suggestions.
- **Movie Search**: Utilize the `/api/movies` endpoint to search and filter movies based on your interests.
- **System Prompts and Tools**: Explore the underlying prompts and tools with `/api/system-prompt` and `/api/tools`.

### Exploring the Playground

CinemaAI features an interactive playground where you can experience its capabilities firsthand:

1. **Access the Playground**:

   - Navigate to `http://localhost:8000` to explore the static interface.

2. **Features**:

   - **Chat with AI**: Use the intuitive chat window to interact with CinemaAI.
   - **Movie Search**: Perform detailed searches using the web interface.
   - **Simple interface to experiment with prompts and tools**: Change it on the go, without much commitment until results are seen.
   - **Simple Design**: Enjoy a seamless experience across various devices.

3. **Customization**:
   - Modify `index.html`, `styles.css`, and `script.js` in the `app/static` directory to tailor the playground to your needs.

## Contributing

We welcome contributions to enhance CinemaAI!

1. **Fork the Repository**: Click on the `Fork` button at the top of the repository page.
2. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**:
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to Your Branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request**: Navigate to your forked repository and click on `Compare & pull request`.

For detailed guidelines, refer to our [Contributing Guide](#) (link to a separate contributing guide if available).

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contact

For any inquiries or support, feel free to reach out:

- **GitHub Issues**: [Report Issues](https://github.com/RGimenez1/CinemaAI/issues)
- **Email**: [renatogimenez96@gmail.com](mailto:renatogimenez96@gmail.com)
