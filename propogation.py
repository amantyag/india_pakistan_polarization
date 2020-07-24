import re
import itertools
import csv
import pandas as pd
TAGS_SCORE_CSV = '' # output filename with hashtag score in each row
SEED_HASHTAGS_CSV = '' # seed hashtags filename eg row: SayNoToWar, -1
TWITTER_CSV = '' # CSV file with collected Tweets
dict_tagscore = {}
dict_hashtag = {}


def make_matrix(df_status):
    for x in range(len(df_status)):
        hashtags = []
        hashtags.append(re.findall(r"#(\w+)", str(df_status[x])))
        for y in range(len(hashtags)):
            for z in hashtags[y]:
                for t in hashtags[y]:
                    if t!=z:
                        if z.lower() in dict_hashtag:
                            if t.lower() in dict_hashtag[z.lower()]:
                                #print('here')
                                dict_hashtag[z.lower()][t.lower()] +=s 1
                            else:
                                #print('there')
                                dict_hashtag[z.lower()][t.lower()] = 1
                        else:
                            dict_hashtag[z.lower()] = {}
                            dict_hashtag[z.lower()][t.lower()] = 1
    return


def first_prop():
    repeat = 10000
    for i in range(1,repeat):
        for key_outer in dict_hashtag:
            if key_outer not in dict_tagscore:
                count = 0
                score = 0
                flag = True
                for key_inner in dict_hashtag[key_outer]:
                    if key_inner in dict_tagscore:
                        score += dict_tagscore[key_inner]*dict_hashtag[key_outer][key_inner]
                        count += dict_hashtag[key_outer][key_inner]
                    else:
                        flag = False
                        break
                if flag:
                    dict_tagscore[key_outer] = score*1.0/count
    return


def second_prop():
    gamma = 100
    repeat = 10000
    for i in range(1,repeat):
        level = int(i/gamma)
        for key_outer in dict_hashtag:
            if key_outer not in dict_tagscore:
                count = 0
                score = 0
                flag = True
                neighbor = 0
                neighbor_withDict = 0
                for key_inner in dict_hashtag[key_outer]:
                    neighbor += 1
                    if key_inner in dict_tagscore:
                        neighbor_withDict +=1
                        score += dict_tagscore[key_inner]*dict_hashtag[key_outer][key_inner]
                        count += dict_hashtag[key_outer][key_inner]
                if neighbor_withDict + level > neighbor and count > 0:
                    dict_tagscore[key_outer] = score*1.0/count
    return

def save_file():
    with open('TAGS_SCORE_CSV', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict_tagscore.items():
            writer.writerow([key,value])
    return


def main():
    df_seed = pd.read_csv(SEED_HASHTAGS_CSV)
    df_full = pd.read_csv(TWITTER_CSV, dtype=str)
    print("Read Data")
    for x in range(len(df_seed)):
        dict_tagscore[str(df_seed['Pro_India'][x]).lower()] = -1
        dict_tagscore[str(df_seed['Pro_Pakistan'][x]).lower()] = 1
    dict_tagscore['nan'] = 0
    df_status = df_full['status_text']
    df_full.drop(df_full.index, inplace=True)
    make_matrix(df_status)
    df_status.drop(df_status.index, inplace=True)
    print("Matrix - Done")
    print("Starting First Label propagation")
    first_prop()
    print("Starting second level propagation")
    second_prop()
    print("Saving files")
    save_file()
    print("File Saved... exiting")

if __name__ == "__main__":
    main()
