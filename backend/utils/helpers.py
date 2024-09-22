import markdown  
from textwrap import dedent
from langchain_text_splitters import RecursiveCharacterTextSplitter


def markdown_to_html(markdown_text):
    return markdown.markdown(dedent(markdown_text.strip()), extensions=['fenced_code', 'tables', 'codehilite'])


def get_middle_x_chars(s, x):
    if len(s) <= x:
        return s
    else:
        start = (len(s) - x) // 2
        end = start + x
        return s[start:end]
    

def get_middle_truncated_text(text, max_tokens=4000):
        
        if not text or not text.strip():
            return ""

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=max_tokens,
            chunk_overlap=min(200, max_tokens // 2),
        )
        texts = text_splitter.split_text(text)

        # get middle chunk
        print(texts, len(texts) // 2)
        middle_chunk = texts[max(0, (len(texts) // 2) - 1)]
        return middle_chunk

def recursive_truncate(text, max_length):
    '''
        Tries to truncate the text to the max_length by removing words from the middle of the text.
        If text is already less than max_length, returns the text as is.
        If text is longer than max_length, removes words from the middle of the text and replaces them with a truncation text.
        If text is still longer than max_length, then removes words from middle of left and right halves of the text and replaces them with a truncation text, recursively.
        
    '''
    l = len(text)
    chunks = [text]

    while chunks:
        trial_text = f"...".join(chunks)
        print(chunks, trial_text, len(trial_text), "\n")
        if len(trial_text) <= max_length:
            return trial_text
        else:
            for _ in range(len(chunks)):
                chunk = chunks.pop(0)
                half = len(chunk) // 2
                
                left = chunk[:half]
                left = left[:left.rfind(" ")].strip()

                right = chunk[half:]
                right = right[right.find(" "):].strip()

                chunks.append(left)
                chunks.append(right)
                # print(chunks)
        input()  # for debugging, to stop at each iteration

    return trial_text


# trying out
if __name__ == "__main__":

    md = dedent(
    """
    | Header 1   | Header 2   | Header 3   |
    |------------|------------|------------|
    | Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
    | Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
    | Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |

    """
    )



    md = dedent(
    """
    # Project Overview

    ## Introduction
    This document provides an overview of the project.

    ### Key Features
    - **Feature 1**: Description of feature 1.
    - **Feature 2**: Description of feature 2.
    - **Feature 3**: Description of feature 3.

    ## Specifications

    ### Table of Specifications
    | Specification   | Description       | Value         |
    |-----------------|-------------------|---------------|
    | OS              | Operating System  | Linux         |
    | Language        | Programming       | Python        |
    | Framework       | Web Framework     | Django        |

    ### Sample Code
    Here’s a sample Python function:

    ```python
    def greet(name):
        return f"Hello, {name}!"
    ```

    ## Conclusion
    In conclusion, this project aims to provide a solution for...

    """
    )
    # html = markdown_to_html(md)
    # print(html)

    text = "This is a long example sentence that we want to truncate intelligently while preserving the important parts of the text. The sentence is long and yaps on and on."
    max_length = 15
    # truncated_text = recursive_truncate(text, max_length)


    # Example usage
    string = "Hello, this is a sample string."
    string = ""
    x = 3
    result = get_middle_truncated_text(text=string, max_tokens=x)
    print(result)