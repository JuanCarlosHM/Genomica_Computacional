# -*- coding: utf-8 -*-

import numpy as np

match_score    = 1
mismatch_score = -1
gap_penalty    = -2

def valor_match(alpha, beta):
    if alpha == beta:
        return match_score
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_score


def nw(secx, secy):
    len_x = len(secx)
    len_y = len(secy)
    matrix_score = np.zeros(shape=(len_x + 1, len_y + 1))


    for i in range(0, len_x + 1):
        for j in range(0, len_y + 1):
            if i == 0:
                matrix_score[0, j] = gap_penalty * j
            elif j == 0:
                matrix_score[i, 0] = gap_penalty * i
            else:
                match = matrix_score[i - 1, j - 1] + valor_match(secx[i-1], secy[j-1])
                delete = matrix_score[i - 1, j] + gap_penalty
                insert = matrix_score[i, j - 1] + gap_penalty
                matrix_score[i, j] = max(match, delete, insert)

    align_x = ''
    align_y = ''
    i = len_x
    j = len_y

    while i > 0 and j > 0:
        score_current = matrix_score[i, j]
        score_diagonal = matrix_score[i - 1, j - 1]
        score_up = matrix_score[i, j - 1]
        score_left = matrix_score[i - 1, j]

        if score_current == score_diagonal + valor_match(secx[i-1], secy[j-1]):
            align_x += secx[i-1]
            align_y += secy[j-1]
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align_x += secx[i-1]
            align_y += '-'
            i -= 1
        elif score_current == score_up + gap_penalty:
            align_x += '-'
            align_y += secy[j-1]
            j -= 1

    while i > 0:
        align_x += secx[i-1]
        align_y += '-'
        i -= 1

    while j > 0:
        align_x += '-'
        align_y += secy[j-1]
        j -= 1

    results(align_x, align_y)

def sw(secx, secy):
    len_x = len(secx)
    len_y = len(secy)
    max_score = 0
    matrix_score = np.zeros(shape=(len_x + 1, len_y + 1))
    matrix_position = np.zeros(shape=(len_x + 1, len_y + 1))

    for i in range(1, len_x + 1):
        for j in range(1, len_y + 1):
            score_diagonal = matrix_score[i - 1, j - 1] + valor_match(secx[i-1], secy[j-1])
            score_up = matrix_score[i, j - 1] + gap_penalty
            score_left = matrix_score[i - 1, j] + gap_penalty
            matrix_score[i, j] = max(0,score_left, score_up, score_diagonal)
            if matrix_score[i, j] == 0:
                matrix_position[i, j] = 0
            if matrix_score[i, j] == score_left:
                matrix_position[i, j] = 1
            if matrix_score[i, j] == score_up:
                matrix_position[i, j] = 2
            if matrix_score[i, j] == score_diagonal:
                matrix_position[i, j] = 3
            if matrix_score[i, j] >= max_score:
                max_i = i
                max_j = j
                max_score = matrix_score[i, j];

    align_x = ''
    align_y = ''
    i = max_i
    j = max_j    # indíces

    while matrix_position[i, j] != 0:
        if matrix_position[i, j] == 3:
            align_x += secx[i-1]
            align_y += secy[j-1]
            i -= 1
            j -= 1
        elif matrix_position[i, j] == 2:
            align_x += '-'
            align_y += secy[j-1]
            j -= 1
        elif matrix_position[i, j] == 1:
            align_x += secx[i-1]
            align_y += '-'
            i -= 1

    results(align_x, align_y)

def results(align_x, align_y):

    align_x = align_x[:: -1]
    align_y = align_y[:: -1]

    score = 0
    mov = ''
    upwardsArrow = u'\u2191'
    northWestArrow = u'\u2196'
    leftWardsArrow = u'\u2190'

    for i in range(0,len(align_x)):
        if align_x[i] == align_y[i]:
            mov = mov + northWestArrow
            score += valor_match(align_x[i], align_y[i])

        elif align_x[i] != align_y[i] and align_x[i] != '-' and align_y[i] != '-':
            score += valor_match(align_x[i], align_y[i])
            mov = mov + northWestArrow


        elif align_x[i] == '-' or align_y[i] == '-':
            score += gap_penalty
            if align_x[i] == '-':
                mov = mov + upwardsArrow
            else:
                mov = mov + leftWardsArrow


    print 'Score = ' score
    print 'Alingn X =  ' align_x
    print 'Directions =' mov
    print 'Alingn X   =' align_y
