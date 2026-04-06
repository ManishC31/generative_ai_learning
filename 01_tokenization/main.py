### Library to convert text into tokens of a particular model - tiktoken
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there! My name is Manish Chavan"

# encode the text
tokens = enc.encode(text)
print("Tokens:", tokens)
# Tokens: [25216, 1354, 0, 3673, 1308, 382, 3265, 1109, 1036, 24803]

# decode the same text
decoded_text = enc.decode([25216, 1354, 0, 3673, 1308, 382, 3265, 1109, 1036, 24803])
print(decoded_text)
