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

"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""
import math


def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # Dict/ to hold total sum for different type
    Dict = []
    # initial sum
    initial_Dict = {}
    # Store/ to hold each words with specific number/type
    Store = {}

    # record the preword and word order
    tag_pair = {}
    n = len(train)
    # initial_log number
    len_ini = 0
    type_ini = 0
    for sentence_index in range(n):
        sent_n = len(train[sentence_index])
        for word_index in range(sent_n):
            word_pair = train[sentence_index][word_index]
            word = word_pair[0]
            tp = word_pair[1]
            if tp not in Dict:
                Dict.append(tp)

            if word_index == 0:

                if tp not in initial_Dict:
                    initial_Dict[tp] = 0
                initial_Dict[tp] += 1

                # if word not in initial_Store:
                #         initial_Store[word] = {}
                # if tp not in initial_Store[word]:
                #         initial_Store[word][tp] = 0
                # initial_Store[word][tp] += 1
            if word_index > 0:
                if train[sentence_index][word_index - 1][1] not in tag_pair:
                    tag_pair[train[sentence_index][word_index - 1][1]] = {}
                if train[sentence_index][word_index][1] not in tag_pair[train[sentence_index][word_index - 1][1]]:
                    tag_pair[train[sentence_index][word_index - 1][1]][train[sentence_index][word_index][1]] = 1
                else:
                    tag_pair[train[sentence_index][word_index - 1][1]][train[sentence_index][word_index][1]] += 1

            if tp not in Store:
                Store[tp] = {}
            if word not in Store[tp]:
                Store[tp][word] = 0
            Store[tp][word] += 1

    # initial
    initial_P = {}
    for tag in initial_Dict:
        len_ini += initial_Dict[tag]
        type_ini += 1
    for tag in initial_Dict:
        initial_P[tag] = math.log((initial_Dict[tag] + 0.001) / (len_ini + 0.001 * (type_ini + 1)))
    initial_u = math.log(0.001 / (len_ini + 0.001 * (type_ini + 1)))
    # print("initial_P",initial_P)
    # transition
    tagtag_P = {}
    tagtag_un = {}
    for pre in tag_pair:
        len_tag = 0
        type_tag = 0
        for tag in tag_pair[pre]:
            type_tag += 1
            len_tag += tag_pair[pre][tag]

        for tag in tag_pair[pre]:
            tagtag_P[(pre, tag)] = math.log((tag_pair[pre][tag] + 0.01) / (len_tag + 0.01 * (type_tag + 1)))

        tagtag_un[pre] = math.log(0.01 / (len_tag + 0.01 * (type_tag + 1)))
    # print("tagtag_P",tagtag_P)
    # emission
    wordtag_P = {}
    wordtag_un = {}
    for tag in Store:
        type_word = 0
        len_word = 0
        for word in Store[tag]:
            type_word += 1
            len_word += Store[tag][word]
        for word in Store[tag]:
            wordtag_P[(tag, word)] = math.log((Store[tag][word] + 0.0001) / (len_word + 0.0001 * (type_word + 1)))
        wordtag_un[tag] = math.log(0.0001 / (len_word + 0.0001 * (type_word + 1)))

    res = []

    test_time = 0

    for sentence in test:
        v = []
        b = []
        length = len(sentence)
        for i in range(length):
            word = sentence[i]
            vk = {}
            bk = {}
            for tag1 in Dict:
                if i == 0:
                    if tag1 in initial_P:
                        p1 = initial_P[tag1]
                    else:
                        p1 = initial_u
                    if (tag1, word) in wordtag_P:
                        p2 = wordtag_P[(tag1, word)]
                    else:
                        p2 = wordtag_un[tag1]
                    vk[tag1] = p1 + p2
                    bk[tag1] = ''
                else:
                    maxa = 0
                    max_p = -math.inf
                    for tag2 in Dict:
                        if (tag2, tag1) in tagtag_P:
                            p2 = tagtag_P[(tag2, tag1)]
                        else:
                            if tag2 in tagtag_un:
                                p2 = tagtag_un[tag2]
                            else:
                                p2 = 0
                        if (tag1, word) in wordtag_P:
                            p3 = wordtag_P[(tag1, word)]
                        else:
                            p3 = wordtag_un[tag1]

                        p = v[i - 1][tag2] + p2 + p3
                        if p > max_p:
                            max_p = p
                            maxa = tag2

                    vk[tag1] = max_p
                    bk[tag1] = maxa
            v.append(vk)
            b.append(bk)

        k = length - 1
        new_sent = []
        arg_b = []
        # find last
        max_tag = 0
        max_p = -math.inf
        for tag in v[k]:
            if v[k][tag] > max_p:
                max_p = v[k][tag]
                max_tag = tag
        arg_b.insert(0, max_tag)

        while not k < 1:
            max_tag = b[k][max_tag]
            arg_b.insert(0, max_tag)
            k -= 1

        for i in range(length):
            new_sent.append((sentence[i], arg_b[i]))

        res.append(new_sent)

    return res
