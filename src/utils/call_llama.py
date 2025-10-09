import ollama

def call_llama_func(model, prompt, stream=False, messages=None):
    if messages is None:
        message_list = [{"role": "user", "content": prompt}]
    else:
        message_list = messages.copy()
        message_list.append({"role": "user", "content": prompt})


    if stream:
        # Streaming response
        stream = ollama.chat(
            model=model, messages=message_list,
            stream=True
        )
        
        for chunk in stream:
            yield chunk["message"]["content"]
    else:
        # Single complete response
        response = ollama.chat(model=model, messages=message_list, stream=False)
        return response["message"]["content"]
