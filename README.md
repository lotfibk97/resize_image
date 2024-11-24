# FastAPI Image Processing API

This project is a FastAPI application that processes CSV files to generate images, applies custom image processing techniques, and provides APIs to interact with the processed images. It includes functionalities to:

- Upload a CSV file and convert it into an image.
- Resize the generated image.
- Apply a custom colormap to the image.
- Store the processed images in a database.
- Retrieve images based on depth ranges.
- Retrieve images by their IDs.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [Contact](#contact)

## Features

- **CSV to Image Conversion**: Converts uploaded CSV files into grayscale images.
- **Image Resizing**: Resizes images to a width of 150 pixels while maintaining aspect ratio.
- **Custom Colormap Application**: Applies a custom colormap to images using OpenCV.
- **Database Storage**: Stores resized images along with metadata in a database.
- **Depth-Based Image Retrieval**: Retrieves images based on specified depth ranges.
- **Image Retrieval by ID**: Fetches images directly using their unique IDs.

## Prerequisites

- **Python 3.9 or higher**
- **Virtual Environment Manager** (optional but recommended)
- **Docker** (optional, for containerization)
- **Git** (to clone the repository)
- **SQLite** (default database) or **PostgreSQL** (if configured)

## Installation

### Clone the Repository

```bash
git clone https://github.com/lotfibk97/resize_image.git
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **On Unix or MacOS:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

The application uses environment variables for configuration. You can set them in your shell or create a `.env` file in the root directory.

- **`DATABASE_URL`**: The URL of the database to use.

  - For SQLite (default):

    ```
    DATABASE_URL=sqlite:///./images.db
    ```

  - For PostgreSQL:

    ```
    DATABASE_URL=postgresql://user:password@localhost:5432/database_name
    ```

## Database Setup

If you're using SQLite (default), the database will be created automatically.

For PostgreSQL:

1. Install PostgreSQL and ensure it's running.
2. Create a database and a user with appropriate privileges.
3. Update the `DATABASE_URL` environment variable with your database credentials.
4. The application will create the necessary tables upon startup.

## Running the Application

### Run with Uvicorn

You can run the application locally using Uvicorn.

```bash
uvicorn app.main:app --reload
```

- Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Run with Docker (Optional)

If you prefer to use Docker:

1. Build the Docker image:

   ```bash
   docker build -t fastapi-image-processing .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 8000:8000 fastapi-image-processing
   ```

## Testing

Tests are located in the `tests` directory.

### Run Tests

```bash
pytest
```

Ensure you have `pytest` installed:

```bash
pip install pytest
```

## API Endpoints

### Upload CSV File

- **Endpoint**: `/upload_csv/`
- **Method**: `POST`
- **Description**: Uploads a CSV file, converts it to an image, resizes it, applies a custom colormap, stores the resized image in the database, and returns the colored and resized image.
- **Form Data**:
  - `file`: The CSV file to upload.
- **Response**: Returns the processed image as a PNG file.
- **Example**: localhost:8000/upload_csv/ or https://python-challenge-production.up.railway.app/upload_csv/

### Get Images by Depth Range

- **Endpoint**: `/images/`
- **Method**: `GET`
- **Query Parameters**:
  - `depth_min`: Minimum depth value (float).
  - `depth_max`: Maximum depth value (float).
- **Description**: Retrieves a list of images within the specified depth range.
- **Response**: JSON list of image metadata.
- **Example**: localhost:8000/images/ or https://python-challenge-production.up.railway.app/images/

### Get Image by ID

- **Endpoint**: `/images/{image_id}`
- **Method**: `GET`
- **Description**: Retrieves an image by its ID.
- **Response**: Returns the image as a PNG file.
- **Example**: localhost:8000/images/{image_id} or https://python-challenge-production.up.railway.app/images/{image_id}

## Deployment

### Deploying to Railway

This app is deployed to railway and you can test it using this url: https://python-challenge-production.up.railway.app/upload_csv/

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── image_processing.py
│   └── (other modules)
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── uploads/
│   └── img.csv
├── requirements.txt
├── Dockerfile
├── .env (optional)
└── README.md
```

- **`app/`**: Contains the application code.
- **`tests/`**: Contains test cases for the application.
- **`uploads/`**: Directory for uploading files during testing.
- **`requirements.txt`**: Lists all Python dependencies.
- **`Dockerfile`**: Defines how to build the Docker image.
- **`.env`**: Contains environment variables.

## Notes

- **Temporary Files**: The application creates temporary files in the `temp` directory during processing. These files are cleaned up automatically.
- **Logging**: Logging is configured to display informational messages.
- **Error Handling**: The application includes error handling for invalid inputs and server errors.
- **Security Considerations**:
  - Filenames are sanitized using UUIDs to prevent collisions.
  - File uploads are validated for type and size.
- **Performance**: The application uses asynchronous file operations to improve performance.
