# LINE Chatbot with ChatGPT

A simple LINE chatbot powered by OpenAI's ChatGPT (GPT-3.5-turbo), hosted on AWS Lambda using Python.

## Prerequisites

- Python 3.9
- LINE account and LINE Developers account
- AWS account
- OpenAI API key

## Setup

1. Clone the repository and navigate to the project directory:

```
git clone https://github.com/kzmkts/line-chatgpt
cd line-chatgpt
```

2. Set up the LINE Messaging API, AWS Lambda function, IAM role, OpenAI API, and webhook following the detailed instructions provided in the conversations with ChatGPT.

3. Replace the placeholders in the `lambda_function.py` file with the appropriate environment variables for your LINE channel access token, LINE channel secret, and OpenAI API key.

4. Deploy your chatbot by packaging and uploading the code to AWS Lambda as instructed by ChatGPT.

## Usage

After deployment, send messages to the chatbot via the LINE chat app, and it will respond using ChatGPT.

---

This project was created using OpenAI's ChatGPT. All instructions and code snippets were generated during the conversation with the AI model.
