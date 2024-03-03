# Project Mashup

Welcome to Project Mashup! This is a simple utility web application that allows users to create personalized music mashups. Users can enter the singer's name, specify the number of songs they want, and set the duration for each song. Once the preferences are set, the web app will generate a custom mashup and email it to the user.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Live Link](#live-link)
- [Dependencies](#dependencies)

## Features

- **Personalized Mashups**: Tailor your music mashup by specifying the singer's name, the number of songs, and the duration for each song.
- **Email Delivery**: Receive your custom mashup directly in your email inbox.
- **FastAPI Framework**: Built using the FastAPI framework for efficient and fast web development.

## Getting Started

To get started with Project Mashup, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/sanyamgoyal401/mashup.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

4. Open your web browser and go to `http://localhost:8000` to access the web application.

## Usage

1. Enter the singer's name.
2. Specify the number of songs you want in your mashup.
3. Set the duration for each song.
4. Click on the "Generate Mashup" button.
5. Enter your email address.
6. Check your email for the personalized mashup.

## Live Link

Visit the live version of Project Mashup [here](https://mashup-7w8k.onrender.com).

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python 3.7+.