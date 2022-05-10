# mp4.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created Fall 2018: Margaret Fleck, Renxuan Wang, Tiantian Fang, Edward Huang (adapted from a U. Penn assignment)
# Modified Spring 2020: Jialu Li, Guannan Guo, and Kiran Ramnath
# Modified Fall 2020: Amnon Attali, Jatin Arora
# Modified Spring 2021 by Kiran Ramnath (kiranr2@illinois.edu)

import math

"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""


def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    laplace = 1e-6
    words = {}
    tags = {}

    # total count of words and tags
    for sentence in train:
        for word, tag in sentence:
            # train words
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
            # train tags
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1

    # Dict for hapax
    hapax = {}
    for sentence in train:
        for word, tag in sentence:
            if words[word] == 1:
                hapax[word] = tag

    # Rare words smooth
    Rare_Words = {}
    # init all tags
    for tag in tags:
        Rare_Words[tag] = 0

    for word in hapax:
        Rare_Words[hapax[word]] += 1

    for tag in tags:
        Rare_Words[tag] = (Rare_Words[tag] + laplace) / (len(hapax) + laplace * len(tags))

    # Now calculate 3 HMMs
    # Initial P
    initial = {}
    for tag in tags:
        initial[tag] = 0

    for sentence in train:
        # just first word
        word = sentence[1]
        initial[word[1]] += 1
    # smooth
    for tag in tags:
        initial[tag] = math.log((initial[tag] + laplace)/(len(train) + laplace * len(tags)))

    # Transition P
    transition = {}
    for tag1 in tags:
        transition[tag1] = {}
        for tag2 in tags:
            transition[tag1][tag2] = 0

    for sentence in train:
        n = len(sentence)
        for i in range(n-1):
            word1 = sentence[i][1]
            word2 = sentence[i+1][1]
            transition[word1][word2] += 1

    for tag1 in tags:
        for tag2 in tags:
            transition[tag1][tag2] = math.log((transition[tag1][tag2] + laplace)/(tags[tag1] + laplace * len(tags)))

    # Emission P
    emission = {}
    for tag in tags:
        emission[tag] = {}
        for word in words:
            emission[tag][word] = 0

    for sentence in train:
        for word, tag in sentence:
            emission[tag][word] += 1

    for tag in tags:
        for word in words:
            if word in hapax:
                emission[tag][word] = math.log(emission[tag][word] + laplace * Rare_Words[tag]) - \
                                      math.log(tags[tag] + laplace * Rare_Words[tag] * (1 + len(words)))
            else:
                emission[tag][word] = math.log(emission[tag][word] + laplace) - math.log(
                    tags[tag] + laplace * (1 + len(words)))

    ret = []
    for sentence in test:
        T = len(sentence)
        Less_NUM = -999999
        viterbi = {}
        pre = {}

        for s in tags:
            viterbi[s] = [Less_NUM for i in range(T)]
            pre[s] = [0 for i in range(T)]

        for s in tags:
            if not sentence[1] in emission[s]:
                p = math.log(laplace * Rare_Words[s]) - math.log(tags[s] + laplace * Rare_Words[s] * (1 + len(words)))
            else:
                p = emission[s][sentence[1]]
            viterbi[s][1] = initial[s] + p
            pre[s][1] = 0

        for t in range(2, T):
            for s in tags:
                if not sentence[t] in emission[s]:
                    p = math.log(laplace * Rare_Words[s]) - math.log(tags[s] + laplace * Rare_Words[s] * (1 + len(words)))
                else:
                    p = emission[s][sentence[t]]
                for s1 in tags:
                    val = viterbi[s1][t - 1] + transition[s1][s] + p
                    if val > viterbi[s][t]:
                        viterbi[s][t] = val
                        pre[s][t] = s1

        ans = ''
        for s in tags:
            if viterbi[s][T - 1] > Less_NUM:
                Less_NUM = viterbi[s][T - 1]
                ans = s

        prediction = []
        for t in range(T - 1, 0, -1):
            prediction.append((sentence[t], ans))
            ans = pre[ans][t]
        prediction.append(("START", "START"))
        prediction.reverse()
        ret.append(prediction)

    return ret