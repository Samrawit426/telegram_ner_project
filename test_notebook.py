#!/usr/bin/env python3
"""
Test script to verify the NER training notebook components work correctly.
"""

import os
import sys
import json
from pathlib import Path

def test_data_loading():
    """Test if the data file can be loaded correctly."""
    print("Testing data loading...")
    
    data_file = "../data/labeled_telegram_product_price_location.txt"
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return False
    
    try:
        # Test the read_conll function
        def read_conll(filepath):
            sentences = []
            labels = []
            tokens = []
            tags = []

            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        if tokens:
                            sentences.append(tokens)
                            labels.append(tags)
                            tokens, tags = [], []
                    else:
                        splits = line.split()
                        if len(splits) >= 2:
                            tokens.append(splits[0])
                            tags.append(splits[1])

            return sentences, labels

        tokens, ner_tags = read_conll(data_file)
        print(f"✅ Data loaded successfully: {len(tokens)} sentences")
        print(f"   Sample tokens: {tokens[0][:5]}")
        print(f"   Sample tags: {ner_tags[0][:5]}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available."""
    print("\nTesting dependencies...")
    
    required_packages = [
        'transformers',
        'datasets', 
        'torch',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {missing_packages}")
        print("Please install them using: pip install " + " ".join(missing_packages))
        return False
    
    return True

def test_model_loading():
    """Test if the model can be loaded."""
    print("\nTesting model loading...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForTokenClassification
        
        model_checkpoint = "xlm-roberta-base"
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        print(f"✅ Tokenizer loaded: {model_checkpoint}")
        
        # Test with a small model first
        model = AutoModelForTokenClassification.from_pretrained(
            model_checkpoint,
            num_labels=5  # Small number for testing
        )
        print(f"✅ Model loaded successfully")
        print(f"   Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing NER Notebook Components\n")
    print("=" * 50)
    
    tests = [
        test_data_loading,
        test_dependencies,
        test_model_loading
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    if all(results):
        print("✅ All tests passed! The notebook should work correctly.")
        print("\n🎉 You can now run the fixed notebook: notebook/train_ner_model_fixed.ipynb")
    else:
        print("❌ Some tests failed. Please fix the issues before running the notebook.")
        print("\n💡 Common fixes:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Check if data file exists: data/labeled_telegram_product_price_location.txt")
        print("   - Ensure you have enough disk space for model downloads")

if __name__ == "__main__":
    main() 