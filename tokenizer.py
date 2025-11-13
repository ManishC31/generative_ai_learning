# convert text into tokens.

import tiktoken

# encoder
enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello there,  my name is Manish Chavan"

tokens = enc.encode(text)

print("tokens:", tokens)
# tokens: [13225, 1354, 11, 220, 922, 1308, 382, 3265, 1109, 1036, 24803]

# decode the same tokens

decoded = enc.decode([13225, 1354, 11, 220, 922, 1308, 382, 3265, 1109, 1036, 24803])
print("decoded:", decoded)


DACH25
