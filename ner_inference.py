def predict_entities(text):
    # Placeholder: use HuggingFace model or LLM API here
    print(f"Processing text:\n{text}")
    return [("3pcs", "B-PRODUCT"), ("silicon", "I-PRODUCT"), ("brush", "I-PRODUCT")]

if __name__ == "__main__":
    with open("data/telegram_data.csv", "r", encoding="utf-8") as f:
        next(f)  # skip header
        for i, line in enumerate(f.readlines()):
            message = line.split(',')[3]
            entities = predict_entities(message)
            print(f"[{i+1}] Entities: {entities}")
