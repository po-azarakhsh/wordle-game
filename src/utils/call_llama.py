import ollama

def call_llama_func(model, prompt, stream=False):
    if stream:
        # Streaming response
        stream = ollama.chat(
            model=model, messages=[
            {"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            yield chunk["message"]["content"]
    else:
        # Single complete response
        response = ollama.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"]
