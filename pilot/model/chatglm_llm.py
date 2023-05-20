#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import torch 

@torch.inference_mode()
def chatglm_generate_stream(model, tokenizer, params, device, context_len=2048, stream_interval=2):
    
    """Generate text using chatglm model's chat api """
    messages = params["prompt"]
    max_new_tokens = int(params.get("max_new_tokens", 256))
    temperature = float(params.get("temperature", 1.0))
    top_p = float(params.get("top_p", 1.0))
    echo = params.get("echo", True)

    generate_kwargs = {
        "max_new_tokens": max_new_tokens,
        "do_sample": True if temperature > 1e-5 else False,
        "top_p": top_p,
        "logits_processor": None
    }

    if temperature > 1e-5:
        generate_kwargs["temperature"] = temperature

    hist = [] 
    for i in range(0, len(messages) - 2, 2):
        hist.append(messages[i][1], messages[i + 1][1])

    query = messages[-2][1]
    output = ""
    i = 0
    for i, (response, new_hist) in enumerate(model.stream_chat(tokenizer, query, hist, **generate_kwargs)):
        if echo:
            output = query + " " + response
        else:
            output = response
        
        yield output

    yield output