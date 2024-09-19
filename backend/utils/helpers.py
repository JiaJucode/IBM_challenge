import markdown  
from textwrap import dedent

def markdown_to_html(markdown_text):
    return markdown.markdown(dedent(markdown_text.strip()), extensions=['fenced_code', 'tables', 'codehilite'])



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
    html = markdown_to_html(md)
    print(html)
