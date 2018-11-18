# Mirko Mantovani

import sys

sys.setrecursionlimit(1500)


class PageRank:
    def __init__(self, alpha=0.85):
        self.alpha = alpha

    def s(self, word_graph, a, p, previous_s):

        return self.alpha * sum(previous_s[b]/word_graph.get_out_degree(b) for b in word_graph.get_pointing_to(a)) + \
               (1 - self.alpha)/word_graph.get_len()

        # return self.alpha * sum(word_graph.get_edge(j, i) / sum(word_graph.get_edge(j, k)
        #                                                         for k in word_graph.graph[j]) * previous_s[j]
        #                         for j in word_graph.graph[i]) + (1 - self.alpha) * p[i]

    def page_rank(self, word_graph, max_iterations):

        p = {}
        page_rank = {}
        last_page_rank = {}

        for node in word_graph.graph:
            p[node] = 1 / len(word_graph.graph)
            page_rank[node] = 1 / len(word_graph.graph)
            last_page_rank[node] = 1 / len(word_graph.graph)
        for iteration in range(0, max_iterations):
            for i in word_graph.graph:
                # print('page rank word '+str(i))
                page_rank[i] = self.s(word_graph, i, p, last_page_rank)
            # normalization and updating steps
            for i in page_rank:
                last_page_rank[i] = page_rank[i]
        return page_rank
