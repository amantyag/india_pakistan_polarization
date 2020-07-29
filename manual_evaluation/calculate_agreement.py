# Script to compute metrics for manual evaluation
# Reproduce Table 2 by running python calculate_agreement.py --set1 annotations_set1.csv --set2 annotations_set2.csv
import pandas
import argparse
from collections import defaultdict, Counter
import math
import numpy as np
import ast
from sklearn.metrics import confusion_matrix, precision_score, recall_score
# See https://en.wikipedia.org/wiki/Fleiss%27_kappa

# calculated for each category, sample, how many raters
# assigned the sample to that category
def reformat(categories, samples):
    retval = []
    for s in samples[0]:
        category_dict = {}
        for c in categories:
            category_dict[c] = 0.0
        retval.append(category_dict)

    for rater in samples:
        for index in range(0, len(rater)):
            retval[index][rater[index]] += 1
    return retval

# for each category, calculate proportion of samples assigned to it
def calculate_pj(samples, num_raters):
    counts = defaultdict(float)
    for sample in samples:
        for c in sample:
            counts[c] += sample[c]

    for k in counts:
        # number of raters * number of samples = total number of ratings
        counts[k] /= len(samples) * num_raters
    sum = 0
    for k in counts:
        sum += counts[k]
    assert (sum - 1.0 < 0.00001), sum
    return counts

# for each sample, calcuate the extent to which raters agree on it
def calculate_pi(ratings_per_category, num_raters):
    sums_squares = [0.0] * len(ratings_per_category)
    for i in range(0, len(ratings_per_category)):
        for c in ratings_per_category[i]:
            sums_squares[i] += ratings_per_category[i][c] * ratings_per_category[i][c]
    scaler = 1. / (num_raters * (num_raters  - 1))
    ret = [scaler * (n - num_raters)  for n in sums_squares]
    return ret


# samples should be a list of frames, where each frame is the annotations by 1 rater
# categories should be list of possible categories
def calculate_fleiss(categories, samples):
    num_raters = len(samples)
    ratings_per_category = reformat(categories, samples)
    pj = calculate_pj(ratings_per_category, num_raters)
    Pi = calculate_pi(ratings_per_category, num_raters)
    P_bar = sum(Pi) / len(ratings_per_category)

    Pe = 0
    for j in pj:
        Pe += pj[j] * pj[j]

    try:
        return (P_bar - Pe) / (1 - Pe)
    except:
        return 0


def calculate_cohen(samples1, samples2):
    count = 0
    category_count1 = defaultdict(int)
    category_count2 = defaultdict(int)
    # count raw accuracy
    for s1, s2 in zip(samples1, samples2):
        if (s1 == s2):
            count += 1
        category_count1[s1] += 1
        category_count2[s2] += 1
    p0 = float(count) / len(samples1)

    # count chance accuracy
    pe = 0.0
    for c in category_count1:
        pe += category_count1[c] * category_count2[c]
    pe /= len(samples1) * len(samples1)
    return (p0 - pe) / (1 - pe)



def nominal_metric(a, b):
    out_val = []
    for i in a:
        if i == b:
            out_val.append(0)
        else:
            out_val.append(1)
    return out_val

def interval_metric(a, b):
    return (a-b)**2

def soft_metric(a, b):
    if a == 'neutral':
        return True
    if b == 'neutral':
        return True
    return a == b

def hard_metric(a, b):
    return a == b

# modified from https://github.com/grrrr/krippendorff-alpha/blob/master/krippendorff_alpha.py

def krippendorff_alpha(data, metric=nominal_metric, force_vecmath=False):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    missing_items: indicator for missing items (default: None)
    '''
    import numpy as np

    # number of coders
    m = len(data)

    # convert input data to a dict of items
    units = defaultdict(list)
    for d in data:
#        diter = enumerate(d)

        for it, g in d.items():
            units[it].append(g)

    n = sum(len(pv) for pv in units.values())  # number of pairable values

    if n == 0:
        raise ValueError("No items to compare.")

    Do = 0.
    for grades in units.values():
        gr = np.asarray(grades)

        Du = sum(np.sum(metric(gr, gri)) for gri in gr)

        Do += Du/float(len(grades)-1)
    Do /= float(n)

    if Do == 0:
        return 1.

    De = 0.
    for g1 in units.values():
        d1 = np.asarray(g1)
        for g2 in units.values():
            De += sum(np.sum(metric(d1, gj)) for gj in g2)
    De /= float(n*(n-1))

    return 1.-Do/De if (Do and De) else 1.

def pairwise_percent_agreement(data, metric):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    missing_items: indicator for missing items (default: None)
    '''

    agreements = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            coder1 = data[i]
            coder2 = data[j]
            keys = set(coder1.keys()).intersection(set(coder2.keys()))
            matched = 0
            for k in keys:
#                if coder1[k] == coder2[k]:
                if metric(coder1[k], coder2[k]):
                    matched += 1
            agreements.append(float(matched) / len(keys))
    return agreements[0] # sum(agreements)  / len(agreements)


def set_value(v):
    if v in ['cant_say', 'Cant Say', 'Neutral', 'Unclassified']:
        return 'neutral'
    if 'cant say' in v.lower() or 'neutral' in v.lower():
        return 'neutral'
    else:
        return v.lower()


def score_classifier(df, classifier, gold, metric):
    correct = 0.0
    count = 0.0
    vals = set()
    for i,row in df.iterrows():
        # if row[classifier] == 'Unclassified':
        #     continue
        if metric(set_value(row[classifier]), set_value(row[gold])):
            correct += 1
        count += 1
    return correct / count, count

# col1 and col2 are the headers for each annotator
def reformat_data(df1, col1, col2):
    # answers = set(df1[col1])
    # print(answers)
    # answers = set(df1[col2])
    # print(answers)
    reformatted_data = [{}, {}]
    for i,row in df1.iterrows():
        reformatted_data[0][i] = set_value(row[col1])
        reformatted_data[1][i] = set_value(row[col2])

    for i in reformatted_data:
        s = Counter()
        for j,k in i.items():
            s[k] += 1
        print(s)
    return reformatted_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--set1')
    parser.add_argument('--set2')
    args = parser.parse_args()

    df1 = pandas.read_csv(args.set1)
    df2 = pandas.read_csv(args.set2)
    df = pandas.concat([df1, df2])
    print("Number of samples", len(df))

    data = reformat_data(df, 'stance_anno1', 'stance_anno2')
    alpha = krippendorff_alpha(data, metric=nominal_metric, force_vecmath=False)
    print("Krippendorff's Alpha stance:", alpha)
    print("Percent agreement", pairwise_percent_agreement(data, hard_metric))
    print("Soft Percent agreement", pairwise_percent_agreement(data, soft_metric))
    print("Classifier score", score_classifier(df, 'predicted_stance', 'stance_gold', hard_metric))
    print("Nice classifier score", score_classifier(df, 'predicted_stance', 'stance_gold', soft_metric))


    data = reformat_data(df, 'country_anno1', 'country_anno2')
    alpha = krippendorff_alpha(data, metric=nominal_metric, force_vecmath=False)
    print("Krippendorff's Alpha country:", alpha)
    print("Percent agreement", pairwise_percent_agreement(data, hard_metric))
    print("Percent agreement", pairwise_percent_agreement(data, soft_metric))

    print("Classifier score", score_classifier(df, 'predicted_country', 'country_gold', hard_metric))
    print("Nice classifier score", score_classifier(df, 'predicted_country', 'country_gold', soft_metric))

    for i,row in df.iterrows():
        if row['predicted_stance'] == 'Unclassified':
            print(row['stance_gold'])

    print("stance_gold", Counter(df['stance_gold']))
    print("predicted_stance", Counter(df['predicted_stance']))


    print("country_gold", Counter(df['country_gold']))
    print("predicted_country", Counter(df['predicted_country']))

    gold = [set_value(v) for v in df['country_gold']]
    preds = [set_value(v) for v in df['predicted_country']]
    print("Country confusion matrix")
    print(confusion_matrix(preds, gold, labels=['pro_india', 'pro_pakistan', 'neutral']))

    b_preds = [x if x == 'pro_war' else 'No' for x in preds]
    b_gold = [x if x == 'pro_war' else 'No' for x in gold]
    print("Pro-war precision", precision_score(b_gold, b_preds, pos_label='pro_war'))
    print("Pro-war recall", recall_score(b_gold, b_preds, pos_label='pro_war'))



    gold = [set_value(v) for v in df['stance_gold']]
    preds = [set_value(v) for v in df['predicted_stance']]
    print("Stance confusion matrix")
    print(confusion_matrix(preds, gold, labels=['pro_war', 'anti_war', 'neutral']))


    zipped = [x for x in zip(df['predicted_stance'], df['stance_gold']) if x[0] != "Unclassified"]
    print(len(zipped))

    b_preds = [x if x == 'pro_war' else 'No' for x,y in zipped]
    b_gold = [y if y == 'pro_war' else 'No' for x,y in zipped]
    print("Pro-war precision", precision_score(b_gold, b_preds, pos_label='pro_war'))
    print("Pro-war recall", recall_score(b_gold, b_preds, pos_label='pro_war'))


if __name__ == "__main__":
    main()
