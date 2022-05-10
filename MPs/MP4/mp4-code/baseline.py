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
# Modified Spring 2021 by Kiran Ramnath
"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # Dict/ to hold total sum for different type
    Dict = {}
    # Store/ to hold each words with specific number/type
    Store = {}

    # Processing training data
    n = len(train)
    for sentence_index in range(n):
        for word_pair in train[sentence_index]:
            word = word_pair[0]
            tp = word_pair[1]

            if tp not in Dict:
                Dict[tp] = 0
            Dict[tp] += 1

            if word not in Store:
                Store[word] = {}
            if tp not in Store[word]:
                Store[word][tp] = 0
            Store[word][tp] += 1

    # End training now

    # Count the maximum possible type for each word
    Pair = {}
    for word in Store:
        fn_tp = ''
        fn_ct = 0
        # find the maximum number
        for tp in Store[word]:
            if Store[word][tp] > fn_ct:
                fn_tp = tp
                fn_ct = Store[word][tp]

        Pair[word] = fn_tp

    Max_tp = ''
    Max_nm = 0
    for tpp in Dict:
        if Dict[tpp] > Max_nm:
            Max_tp = tpp
            Max_nm = Dict[tpp]

    # Start to reach for test

    n = len(test)
    ans = []
    for sentence_index in range(n):
        sent = []
        for word in test[sentence_index]:
            # not in Pair, so make maximum tp
            if word not in Pair:
                sent.append((word, Max_tp))
            else:
                sent.append((word, Pair[word]))

        ans.append(sent)

    return ans
