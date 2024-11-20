def iterative_truncate(text, max_length):
    truncate_text = "..."
    '''
        Tries to truncate the text to the max_length by removing words from the middle of the text.
        
    '''





if __name__ == '__main__':

    # Example usage
    text = "This is a long example sentence that we want to truncate intelligently while preserving the important parts of the text. The sentence is long and yaps on and on."
    max_length = 15
    truncated_text = iterative_truncate(text, max_length)
    print(truncated_text)
