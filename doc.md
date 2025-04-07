# Gemini by Example

> Gemini is Google's most capable AI model for generating text, code, images, and more. Please visit the [official documentation](https://ai.google.dev/gemini-api/docs) to learn more.

Gemini by Example is a hands-on introduction to Google's Gemini SDK and API using annotated code examples. This site takes inspiration from [gobyexample.com](https://gobyexample.com), from which I learned many things about the Go programming language.

Examples here assume Python `>=3.9` and the latest version of the Gemini SDK/API (the [`google-genai`](https://pypi.org/project/google-genai/) package). Try to upgrade to the latest versions if something isn't working.

Note: A more comprehensive version of this file / documentation is available at [https://geminibyexample.com/llms-ctx.txt](https://geminibyexample.com/llms-ctx.txt), which contains the full text of all examples including code samples and terminal output. You could paste that into Cursor or Gemini or another IDE or AI model to then ask questions and get it to generate code with the Gemini examples as its context.

## Text

- [Simple text generation](https://geminibyexample.com/001-basic-generation/)
- [Streaming text](https://geminibyexample.com/002-streaming-text/): This example demonstrates how to use the Gemini API to generate text content and stream the output..
- [System prompt](https://geminibyexample.com/003-system-prompt/): This example demonstrates how to use system instructions to guide the model's behavior..
- [Reasoning models](https://geminibyexample.com/019-reasoning-models/): This example demonstrates how to access the reasoning trace of a Gemini model and then the final text output.
- [Structured output](https://geminibyexample.com/020-structured-output/): This example shows how to generate structured data using a pydantic model to represent Cats with name, colour, and special ability..

## Images

- [Image question answering](https://geminibyexample.com/004-image-q-a/): This example demonstrates how to use the Gemini API to analyze or understand images of cats, including using image URLs and base64 encoding..
- [Image generation (Gemini and Imagen)](https://geminibyexample.com/005-image-generation/): This example demonstrates generating images using both Gemini 2.0 Flash and Imagen 3 models, focusing on cat-related prompts..
- [Edit an image](https://geminibyexample.com/006-editing-images/): This example demonstrates how to edit an existing image of a cat to add a hat using the Gemini API..
- [Bounding boxes](https://geminibyexample.com/007-bounding-boxes/): This example demonstrates how to use the Gemini API to detect an object (a cat) in an image and retrieve its bounding box coordinates..
- [Image segmentation](https://geminibyexample.com/008-image-segmentation/): This example demonstrates how to use the Gemini API to perform image segmentation on a picture of a cat..

## Audio

- [Audio question answering](https://geminibyexample.com/009-audio-q-a/): This example demonstrates how to ask a question about the content of an audio file using the Gemini API..
- [Audio transcription](https://geminibyexample.com/010-audio-transcription/): This example demonstrates how to transcribe an audio file by providing the audio data inline with the request..
- [Audio summarization](https://geminibyexample.com/011-audio-summarization/): This example demonstrates how to summarize the content of an audio file using the Gemini API..

## Video

- [Video question answering](https://geminibyexample.com/012-video-q-a/): This example demonstrates how to ask questions about a video using the Gemini API.
- [Video summarization](https://geminibyexample.com/013-video-summarization/): This example demonstrates how to summarize the content of a video using the Gemini API.
- [Video transcription](https://geminibyexample.com/014-video-transcription/): This example demonstrates how to transcribe the content of a video using the Gemini API.
- [YouTube video summarization](https://geminibyexample.com/015-youtube-video-summarization/): This example demonstrates how to summarize a YouTube video using its URL..

## PDFs and other data types

- [PDF and CSV data analysis and summarization](https://geminibyexample.com/016-pdf-csv-analysis/): This example demonstrates how to use the Gemini API to analyze data from PDF and CSV files..
- [Translate documents](https://geminibyexample.com/017-content-translation/): This example demonstrates how to load content from a URL and translate it into Chinese using the Gemini API.
- [Extract structured data from a PDF](https://geminibyexample.com/018-structured-data-extraction/): This example demonstrates how to extract structured data from a PDF invoice using the Gemini API and Pydantic..

## Agentic behaviour

- [Function calling & tool use](https://geminibyexample.com/021-tool-use-function-calling/): This example demonstrates how to use the Gemini API to call external functions..
- [Code execution](https://geminibyexample.com/022-code-execution/): This example demonstrates how to use the Gemini API to execute code (agent-style) and calculate the sum of the first 50 prime numbers..
- [Model Context Protocol](https://geminibyexample.com/023-mcp-model-context-protocol/): This example demonstrates using a local MCP server with Gemini to get weather information..
- [Grounded responses with search tool](https://geminibyexample.com/024-grounded-responses/): This example demonstrates how to use the Gemini API with the Search tool to get grounded responses.

## Token counting & context windows

- [Model context windows](https://geminibyexample.com/025-model-context-windows/): This example demonstrates how to access the input and output token limits for different Gemini models..
- [Counting chat tokens](https://geminibyexample.com/026-token-counting/): This example demonstrates how to count tokens in a chat history with the Gemini API, incorporating a cat theme..
- [Calculating multimodal input tokens](https://geminibyexample.com/027-calculate-input-tokens/): This example demonstrates how to calculate input tokens for different data types when using the Gemini API, including images, video, and audio..
- [Context caching](https://geminibyexample.com/028-context-caching/): This example demonstrates how to use the Gemini API's context caching feature to efficiently query a large document multiple times without resending it with each request.

## Miscellaneous

- [Rate limits and retries](https://geminibyexample.com/029-rate-limits-retries/): This example demonstrates generating text with the Gemini API, handling rate limiting errors, and using exponential backoff for retries..
- [Concurrent requests and generation](https://geminibyexample.com/030-async-requests/): This example demonstrates how to generate text using concurrent.futures to make parallel requests to the Gemini API, with a focus on cat-related prompts..
- [Embeddings generation](https://geminibyexample.com/031-embeddings/): This example demonstrates generating text embeddings for cat-related terms using the Gemini API..
- [Safety settings and filters](https://geminibyexample.com/032-safety-filters/): This example demonstrates how to adjust safety settings to block content based on the probability of unsafe content..
- [LiteLLM](https://geminibyexample.com/033-litellm/): This example demonstrates how to use the LiteLLM library to make calls to the Gemini API.

## Resources

- [Official Gemini Documentation](https://ai.google.dev/gemini-api/docs)
- [Source Code](https://github.com/strickvl/geminibyexample)
- [Author's Blog](https://mlops.systems)
- [Author's LinkedIn](https://linkedin.com/in/strickvl)

Last updated: April 6, 2025