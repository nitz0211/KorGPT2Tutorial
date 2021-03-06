from transformers import GPT2LMHeadModel, GPT2Config
from new_tokenizer import MyTokenizer
import torch

vocab_file_path = '../tokenizer/vocab.json'
merge_file_path = '../tokenizer/merges.txt'

tokenizer = MyTokenizer(vocab_file_path, merge_file_path)
bos = tokenizer.convert_tokens_to_ids('<s>')
eos = tokenizer.convert_tokens_to_ids('</s>')
pad = tokenizer.convert_tokens_to_ids('<pad>')
unk = tokenizer.convert_tokens_to_ids('<unk>')


config = GPT2Config(vocab_size=52000, resid_pdrop=0, embd_pdrop=0, attn_pdrop=0, summary_first_dropout=0)
model = GPT2LMHeadModel(config)

model_dir = '../KorGPT-2SampleModel/pytorch_model.bin'

model.load_state_dict(torch.load(model_dir), strict=False)
model.to('cpu')

def encoding(text):
    tokens = ['<s>'] + tokenizer.tokenize(text)
    return torch.tensor(tokenizer.convert_tokens_to_ids(tokens)).unsqueeze(0)

def decoding(ids):
    return tokenizer.convert_ids_to_tokens(ids[0])

input_ids = encoding('이순신은 조선')
# greedy_output = model.generate(input_ids, max_length=100, bos_token_id=bos, pad_token_id=pad, eos_token_id=eos, do_sample=True)
#beam_output = model.generate(
#    input_ids, 
#    max_length=200, 
#    num_beams=5, 
#    no_repeat_ngram_size=2, 
#    early_stopping=True
#)
sample_outputs = model.generate(
    input_ids,
    do_sample=True, 
    max_length=200, 
    top_k=50, 
    top_p=0.95, 
    num_return_sequences=3, bad_words_ids=[[unk]]
)
print(decoding(sample_outputs.tolist()))

# check https://huggingface.co/blog/how-to-generate :-)
