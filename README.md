# Tender to Discourse

## Overview

This project is designed to download categories, discussions, and comments from the Tender API and save them locally in a structured format. The data is organized into directories and JSON files for easy access and analysis.

A second script will be developed to upload the downloaded data to a Discourse instance, allowing you to migrate your Tender forum to Discourse.

## Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project. You can use the `.env.example` file as a template:

    ```sh
    cp .env.example .env
    ```

4. Obtain your Tender API key from your profile edit page on the Tender website and add it to the `.env` file:

    ```env
    TENDER_API_KEY=your_api_key_here
    ```

## Usage

Run the `download-tender.py` script to start downloading the data:

```sh
python download-tender.py
```

The script will create a `data` directory and organize the downloaded data into subdirectories based on categories, discussions, and comments.

## Directory Structure

The downloaded data will be organized as follows:

```text
data/
    categories/
        <category-slug>/
            category.json
            <discussion-id>/
                discussion.json
                comments/
                    <comment-id>/
                        comment.json
                        <asset-filename>
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
