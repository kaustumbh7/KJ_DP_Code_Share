import argparse
import sys
import os
import json
import logging
import pickle


############################################  NOTE  ########################################################
#
#           Creates NER training data in Spacy format from JSON downloaded from Dataturks.
#
#           Outputs the Spacy training data as a pickle file which can be used during Spacy training.
#
#           Run: python Dataturks_to_Spacy.py <dataturks_JSON_FilePath> <training_output_FilePath>
#
#
############################################################################################################

#enable info logging.
logging.getLogger().setLevel(logging.INFO)


def convertSingleItem(dataturks_labeled_item):
    try:
        data = json.loads(dataturks_labeled_item)
        text = data['content']
        entities = []
        for annotation in data['annotation']:
            #only a single point in text annotation.
            point = annotation['points'][0]
            labels = annotation['label']
            # handle both list of labels or a single label.
            if not isinstance(labels, list):
                labels = [labels]

            for label in labels:
                #dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                entities.append((point['start'], point['end'] + 1 ,label));

        return (text, {"entities" : entities});

    except Exception as e:
        logging.exception("Unable to process item " + dataturks_labeled_item + "\n" + "error = " + str(e))
        return None


def main(dataturks_JSON_FilePath='data.json', training_output_FilePath='output.pkl'):
    #make sure everything is setup.
    if (not os.path.exists(dataturks_JSON_FilePath)):
        logging.exception(
            "Please specify a valid path to dataturks JSON output file, " + dataturks_JSON_FilePath + " doesn't exist")
        return

    if (not os.path.exists(os.path.dirname(training_output_FilePath))):
        logging.exception(
            "Please specify a valid path to output file, " + os.path.dirname(training_output_FilePath) + " directory doesn't exist")
        return

    with open(training_output_FilePath, "a+") as f:
        logging.info("File " + training_output_FilePath + " exists....")

    logging.info("Converting " + dataturks_JSON_FilePath + " ...");

    lines = []
    with open(dataturks_JSON_FilePath, 'r') as f:
        lines = f.readlines()

    if (not lines or len(lines) == 0):
        logging.exception(
            "Please specify a valid path to dataturks JSON output file, " + dataturks_JSON_FilePath + " is empty")
        return

    count = 0;
    success = 0
    training_data = []
    for line in lines:
        result = convertSingleItem(line)
        if (result):
            training_data.append(result)
            success = success + 1

        count += 1;
        if (count % 100 == 0):
            logging.info(str(count) + " items done ...")


    with open(training_output_FilePath, 'wb') as output:
        pickle.dump(training_data, output, pickle.HIGHEST_PROTOCOL)

    logging.info(
        "Completed: " + str(success) + " items done, " + str(len(lines) - success) + " items ignored due to errors")


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='Converts Dataturks NER output JSON file to Spacy training file format.')
    parser.add_argument('dataturks_JSON_FilePath',
                    help='Path to the JSON file downloaded from Dataturks.')
    parser.add_argument('training_output_FilePath',
                        help='Path to the file where Spacy training data will be stored as pickle output.')
    return parser

if __name__ == '__main__':
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    dataturks_JSON_FilePath = parsed_args.dataturks_JSON_FilePath
    training_output_FilePath = parsed_args.training_output_FilePath
    main(dataturks_JSON_FilePath, training_output_FilePath)