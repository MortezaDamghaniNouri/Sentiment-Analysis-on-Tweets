import math
import pickle
from tensorflow import keras
from Commons import comment_smoother
from Commons import dictionary_loader
from Commons import nltk_input_list_generator
from Commons import unique_words_counter
from Commons import x_file_reader


# This function returns the final classification of combined model
def final_evaluator(input_nb_results, input_me_results, input_fcnn_results, expected_tag):
    final_results = []
    i = 0
    while i < len(input_nb_results):
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            final_results.append(1)
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            final_results.append(-1)
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            final_results.append(0)
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
            pass
        if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
            pass






        i += 1


























# This function creates the neural network model for testing
def create_model():
    output_model = keras.Sequential()
    output_model.add(keras.layers.Dense(64, activation="relu", input_shape=(47, )))
    output_model.add(keras.layers.Dense(32, activation="relu"))
    output_model.add(keras.layers.Dense(3, activation="softmax"))
    output_model.summary()
    output_model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return output_model


# This function generates Naive Bayes model results for the input test file
def nb_predictor(input_test_file_address, input_positive_dictionary, input_negative_dictionary, input_positive_words_count, input_negative_words_count, input_unique_words_count):
    output_results = []
    test_tweets_file = open(input_test_file_address, "rt", encoding="utf8")
    while True:
        tweet = test_tweets_file.readline().lower()
        if tweet == "":
            break

        tweet = comment_smoother(tweet)
        words_list = tweet.split(" ")
        final_result = 0
        for word in words_list:
            if word in input_positive_dictionary:
                positive_numerator = input_positive_dictionary[word] + 1
            else:
                positive_numerator = 1

            if word in input_negative_dictionary:
                negative_numerator = input_negative_dictionary[word] + 1
            else:
                negative_numerator = 1

            final_result += math.log10((positive_numerator / (input_positive_words_count + input_unique_words_count)) / (negative_numerator / (input_negative_words_count + input_unique_words_count)))
        if final_result > 0:
            output_results.append(1)
        if final_result == 0:
            output_results.append(0)
        if final_result < 0:
            output_results.append(-1)

    return output_results


# This function generates Maximum Entropy model results for the input test file
def me_predictor(input_test_file_address, input_desired_label, input_classifier):
    output_results = []
    test_tweets_list = nltk_input_list_generator(input_test_file_address, input_desired_label, [])
    for tweet_tuple in test_tweets_list:
        tweet_word_dictionary = tweet_tuple[0]
        main_label = tweet_tuple[1]
        predicted_label = input_classifier.classify(tweet_word_dictionary)
        output_results.append(predicted_label)
    return output_results


# This function generates FCNN model results for the input test file
def fcnn_predictor(input_test_x_file_address, input_fcnn_model):
    output_results = []
    test_x = x_file_reader(input_test_x_file_address)
    model_predictions = input_fcnn_model.predict(test_x)
    for prediction in model_predictions:
        maximum = max(prediction[0], prediction[1], prediction[2])
        if maximum == prediction[0]:
            output_results.append(1)
        if maximum == prediction[1]:
            output_results.append(0)
        if maximum == prediction[2]:
            output_results.append(-1)
    return output_results


# This function calculates the precision of different models on different test data and initializes related variable
def precision_calculator(input_results, input_desired_label):
    counter = 0
    for result in input_results:
        if result == input_desired_label:
            counter += 1
    return round((counter / len(input_results)) * 100, 2)



# Main part of the code starts here
# Loading saved models
print("Loading saved models...")
positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
me_model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
me_classifier = pickle.load(me_model_file)
me_model_file.close()
fcnn_model = create_model()
fcnn_model.load_weights("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Checkpoints//Main Trained Model//my_checkpoint1")
number_of_unique_words = unique_words_counter(positive_tweets_dictionary, negative_tweets_dictionary)

# Evaluating the positive test tweets
positive_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
nb_positive_test_results = nb_predictor(positive_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_positive_test_results = me_predictor(positive_test_tweets_file_address, 1, me_classifier)
fcnn_positive_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//positive_test_x_complete.txt"
fcnn_positive_test_results = fcnn_predictor(fcnn_positive_test_tweets_file_address, fcnn_model)

# Evaluating the negative test tweets
negative_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
nb_negative_test_results = nb_predictor(negative_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_negative_test_results = me_predictor(negative_test_tweets_file_address, -1, me_classifier)
fcnn_negative_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//negative_test_x_complete.txt"
fcnn_negative_test_results = fcnn_predictor(fcnn_negative_test_tweets_file_address, fcnn_model)

# Evaluating the neutral test tweets
neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt"
nb_neutral_test_results = nb_predictor(neutral_test_tweets_file_address, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
me_neutral_test_results = me_predictor(neutral_test_tweets_file_address, 0, me_classifier)
fcnn_neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//neutral_test_x_complete.txt"
fcnn_neutral_test_results = fcnn_predictor(fcnn_neutral_test_tweets_file_address, fcnn_model)

NB_POSITIVE_PRECISION = precision_calculator(nb_positive_test_results, 1)
NB_NEGATIVE_PRECISION = precision_calculator(nb_negative_test_results, -1)
NB_NEUTRAL_PRECISION = precision_calculator(nb_neutral_test_results, 0)
ME_POSITIVE_PRECISION = precision_calculator(me_positive_test_results, 1)
ME_NEGATIVE_PRECISION = precision_calculator(me_negative_test_results, -1)
ME_NEUTRAL_PRECISION = precision_calculator(me_neutral_test_results, 0)
FCNN_POSITIVE_PRECISION = precision_calculator(fcnn_positive_test_results, 1)
FCNN_NEGATIVE_PRECISION = precision_calculator(fcnn_negative_test_results, -1)
FCNN_NEUTRAL_PRECISION = precision_calculator(fcnn_neutral_test_results, 0)

# Calculating combined model precision for positive test data
final_evaluator(nb_positive_test_results, me_positive_test_results, fcnn_positive_test_results, 1)

# Calculating combined model precision for negative test data
final_evaluator(nb_negative_test_results, me_negative_test_results, fcnn_negative_test_results, -1)

# Calculating combined model precision for neutral test data
final_evaluator(nb_neutral_test_results, me_neutral_test_results, fcnn_neutral_test_results, 0)











