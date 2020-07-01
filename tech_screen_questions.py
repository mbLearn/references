#1
# Given a string S and a character C, return an array of integers representing the shortest distance from the character C in the string.
# Input: st = "loveleetcode", ch = 'e'
# Output: [3, 2, 1, 0, 1, 0, 0, 1, 2, 2, 1, 0]

def shortest_to_char(st, ch):
    prev = float('-inf')
    ans = []
    for i, x in enumerate(st):
        if x == ch: 
            prev = i
        ans.append(i - prev)

    prev = float('inf')
    for i in xrange(len(st) - 1, -1, -1):
        if st[i] == ch: 
            prev = i
        ans[i] = min(ans[i], prev - i)
    return ans
    
# Time Complexity - O(N)
# Space Complexity - O(N)

    
#1A Another Flavor
# Write a function get_products_of_all_ints_except_at_index() that takes a vector of integers and returns a vector of the products.
# Input:   [1, 7, 3, 4]
# Output: [84, 12, 28, 21]


#2 We are given a list cpdomains of count-paired domains. We would like a list of count-paired domains, (in the same format as the input, and in any order), that explicitly counts the number of visits to each subdomain.
# Input:  ["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
# Output:  {"mail.com" : 901, " yahoo.com" : 50 , "google.mail.com" : 900 , "wiki.org": 5, "org": 5 , "intel.mail.com": 1, "com": 951}

import collections

def subdomain_visits(cpdomains):
    ans = collections.Counter()
    for domain in cpdomains:
        count, domain = domain.split()
        count = int(count)
        frags = domain.split('.')
        for i in xrange(len(frags)):
            ans[".".join(frags[i:])] += count
    return {dom: ct for dom, ct in ans.items()}
    
# Time Complexity = O(N)
# Space Complexity = O(N)


#3 Given a list of values find the pair of values that sum a particular value K.
# Input: arr = [1, 2, 4, 6, 10, 3, 5]
# Input: expected_sum = 7
# Output: [[6, 1], [3, 4], [5, 2]]


def get_sum(lst, st):
    diff_hash = {}
    result = []
    for i in lst:
        if i in diff_hash.keys():
            result.append([i, diff_hash[i]])
        key = st - i
        diff_hash[key] = i
    return result
    
# Time Complexity = O(N)
# Space Complexity = O(N)


#4 Given two sorted lists create a combined sorted list.
# NOTE: Do Not use python "Sort" function.
# a = [3,4,5] 
# b = [2,6,7]
# Output: [2,3,4,5,6,7]

def merge_two_arrays(lst1, lst2):
    result = []

    pointer_lst1 = 0
    pointer_lst2 = 0

    while pointer_lst1 + pointer_lst2 < len(lst1) + len(lst2):
        if pointer_lst1 != len(lst1) and (pointer_lst2 == len(lst2) or lst1[pointer_lst1] < lst2[pointer_lst2]):
            result.append(lst1[pointer_lst1])
            pointer_lst1 += 1
        else:
            result.append(lst2[pointer_lst2])
            pointer_lst2 += 1
    return result
    
def merge_lists(a, b):
    size_1 = len(a) 
    size_2 = len(b)
  
    res = [] 
    i, j = 0, 0
  
    while i < size_1 and j < size_2: 
        if a[i] < b[j]: 
            res.append(a[i]) 
            i += 1
        else: 
            res.append(b[j]) 
            j += 1
  
    return res + a[i:] + b[j:] 
        
# Time Complexity = O(N)
# Space Complexity = O(N)
# Followup : Is it possible to save space?


#5 Given a list of airline tickets represented by pairs of departure and arrival airports [from, to], reconstruct the itinerary in order. All of the tickets belong to a man who departs from JFK. Thus, the itinerary must begin with JFK.
# Input: [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
# Output: ["JFK", "MUC", "LHR", "SFO", "SJC"]

def find_itinerary(tickets):
    graph = {}
    for ticket in tickets:
        from_airport, to_airport = ticket
        if from_airport not in graph:
            graph[from_airport] = []
            
        graph[from_airport].append(to_airport)
    
    for from_airport, dest in graph.items():
        graph[from_airport] = sorted(graph[from_airport], reverse=True)
    
    
    queue = ["JFK"]
    res = []
    while len(queue) > 0:
        elem = queue[-1]
        if elem in graph and len(graph[elem]) > 0:
            queue.append(graph[elem].pop())
        else:
            # I can't further explore this ele/airport
            res.append(queue.pop())
    return res[::-1]
    
# Time Complexity = O(V + E)


#6 Find All Paths in the graph.
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths
    
    
#7 Return shortest path.
# ANSWER:  BFS Algorithm
    

#8 Given a 2D board containing 'X' and 'O', capture all regions surrounded by 'X'. A region is captured by flipping all 'O's into 'X's in that surrounded region.
# Input : 
 
#  X X X X
#  X O O X
#  X X O X
#  X O X X
 
# Output:
 
#  X X X X
#  X X X X
#  X X X X
#  X O X X
# Solution: Flood Fill Algorithm

import pprint

O, X = 'O', 'X'

def save(board, i, j, safe):
    if (i, j) in safe or i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
        return

    if board[i][j] == O:
        safe[(i, j)] = True
        save(board, i - 1, j, safe)
        save(board, i + 1, j, safe)
        save(board, i, j - 1, safe)
        save(board, i, j + 1, safe)


def solve(board):
    if len(board) < 3 or len(board[0]) < 3:
        # no inner capturable cells
        return board

    safe = {}
    for col in (0, len(board[0]) - 1):
        for row in range(len(board)):
            if board[row][col] == O:
                save(board, row, col, safe)

    for row in (0, len(board) - 1):
        for col in range(1, len(board[0]) - 1):
            if board[row][col] == O:
                save(board, row, col, safe)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == O and (i, j) not in safe:
                board[i][j] = 'X'

    return board

# M is the number of pixels in the square and N is the length of the side of a square, then M = N^2 and the complexity is O(M) = O(N^2)


#9 Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
#ANSWER: Demonstrates knowledge and use of stack

#10 Given a collection of intervals, merge all overlapping intervals.
# Input: [[1,3],[2,6],[8,10],[15,18]]
# Output: [[1,6],[8,10],[15,18]]
def merge_meetings(meetings):
    # Sort by start time
    sorted_meetings = sorted(meetings)

    merged_meetings = [sorted_meetings[0]]

    for current_meeting_start, current_meeting_end in sorted_meetings[1:]:
        last_merged_meeting_start, last_merged_meeting_end = merged_meetings[-1]

        # If the current meeting overlaps with the last merged meeting, use the
        # later end time of the two
        if (current_meeting_start <= last_merged_meeting_end):
            merged_meetings[-1] = (last_merged_meeting_start,
                                   max(last_merged_meeting_end,
                                       current_meeting_end))
        else:
            # Add the current meeting since it doesn't overlap
            merged_meetings.append((current_meeting_start, current_meeting_end))

    return merged_meetings

# Time Complexoty - O(nlgn) 
# Space Complexity - O(n)

# Another Flavor
#10A Given an array of meeting time intervals consisting of start and end times [s1, e1], [s2, e2], ... , determine if a person could attend all meetings.
# Input: [ [0, 30], [5, 10], [15, 20] ],
# output:  false
