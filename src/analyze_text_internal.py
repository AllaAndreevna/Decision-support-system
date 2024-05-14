import torch
from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW

def analyze_text_internal(text):
    # Define the device variable
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #  load the trained model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1, output_attentions=False, output_hidden_states=False)
    # model.reset_classifier(num_labels=1)

    # Load the saved classifier.weight and classifier.bias
    model.classifier.weight = torch.load('neural_network_data/classifier_weight.pt')
    model.classifier.bias = torch.load('neural_network_data/classifier_bias.pt')

    # Initialize the classifier layer with random weights
    model.classifier = torch.nn.Linear(model.config.hidden_size, 1)

    model.load_state_dict(torch.load('neural_network_data/trained_model.pt'))

    # Load the trained model weights
    # state_dict = torch.load('trained_model.pt')

    # # Remove the 'classifier' layer from the state dictionary
    # state_dict.pop('classifier.weight')
    # state_dict.pop('classifier.bias')

    # Load the trained weights into the model
    # model.load_state_dict(state_dict)

    # Initialize the classifier layer with random weights
    model.classifier = torch.nn.Linear(model.config.hidden_size, 1)

    model.to(device)
    model.eval()

    # prepare the input data

    # (!) we have already a text from html page
    
    # Load the tokenizer
    input_example = tokenizer.encode_plus(text, return_tensors='pt', truncation=True, padding=True)
    input_ids = input_example['input_ids'].to(device)
    attention_mask = input_example['attention_mask'].to(device)

    # make predictions

    # Note that you should use the torch.no_grad()
    # context manager to disable gradient computation
    # during inference, as it can save memory
    # and improve performance.
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits.squeeze()

        probabilities = torch.nn.functional.sigmoid(logits)
        predicted_label = probabilities.item()

        # predicted_label = logits.item()


        # probabilities = torch.nn.functional.softmax(logits, dim=0)
        # predicted_label = torch.argmax(probabilities)
    
    # print(predicted_label)


    return predicted_label