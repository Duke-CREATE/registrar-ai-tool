from transformers import pipeline

def classify_sample():

    classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
    
    samples = ["machine learning courses",
               "environmental engineering courses",
               "What courses to take if I'm interested in AI",
               "Courses available on Tuesdays and Thursdays afternoons"]
    candidate_labels = ["course by topic", "course by skill", "course by times offered"]
    results = []
    for sample in samples:
        result = classifier(sample, candidate_labels)
        results.append(result)
    
    return results

if __name__ == "__main__":
    results = classify_sample()
    print(results)
    print()