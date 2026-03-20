#!/usr/bin/python3


from collections import defaultdict as dd
import random
import numpy as np  
import sys,os 

# np
HERE = os.path.dirname(os.path.abspath(__file__))                                                                                                                                                        
if HERE not in sys.path: sys.path.insert(0, HERE)
import qcProgress as QP
import qcIO as IO 


#############################################################################################
##################################     TRAIT CLASS      ####################################
#############################################################################################




class DeDupe:
    def __init__(self, traits, rule='sampleSize.target'):
        self.traits, self.rule, self.rank = traits, rule, dd(float) 
        

        for ti,T in self.traits.items(): 
            if rule in ['sampleSize.target','sampleSize','n','N']:         self.rank[ti] = T.sampleSize.target 
            elif rule.upper() in ['H2']:                                   self.rank[ti] = T.misc.h2 
            else:                                                          self.rank[ti] = random.random() 



    def separate_pairs_and_groups(self): 
        self.pairs, mults, obs = [], [], [] 
        


        for ti,T in self.traits.items():
            if ti in obs: continue 
            elif len(T.dupes) > 1 or len(self.traits[T.dupes[0]].dupes) > 1: mults.append(ti) 
            else:
                
                obs.append(T.dupes[0]) 
                self.pairs.append([ti, T.dupes[0]]) 
        


        self.groups = sorted(self.split_mults(mults)) 
        

    def maximize_group_winners(self):  
        winners, losers = [], [] 
        for group in self.groups: 
            
            cands = self.choose_max_independent_sets(group) 
            #good = [x for x in group if x in IWANT] 
            #print() 
            #print(self.traits[group[0]].name) 
            #print(len(group), group)  
            #print(len(cands))
            #print('yo', good) 

            ranked_cands  = sorted([[sum([self.rank[ti] for ti in cand_group]), cand_group] for cand_group in cands] , reverse=True)             
            
            #for j,(rv,rc) in enumerate(ranked_cands): 
            #    if j > 3: break 
            #    print(rc) 

            winners.append(ranked_cands[0][1]) 
            losers.append([g for g in group if g not in ranked_cands[0][1]]) 

            #winners.extend(ranked_cands[0][1]) 
            #losers.extend([g for g in group if g not in ranked_cands[0][1]]) 
        return winners, losers  

    #def select_top_pairs(self): 
    def order_pairs(self): 
        winners, losers = [], [] 
        ordered_pairs = [] 
        

        for t1,t2 in self.pairs:
            if t1 in [23110,23109]: 
                print('yes') 
            if self.rank[t1] > self.rank[t2]: ordered_pairs.append([t1,t2])  
            else:                             ordered_pairs.append([t2,t1])           
        return ordered_pairs 



    def split_mults(self, mults):
        mults = set(str(x) for x in mults)
        # build adjacency restricted to mults
        adj = {tid: set() for tid in mults}
        for tid in mults:
            T = self.traits[tid]
            for d in (T.dupes or []):
                d = str(d)
                if d in mults:
                    adj[tid].add(d)
                    adj[d].add(tid)   # ensure symmetry
        # find connected components
        seen = set()
        groups = []
        for start in mults:
            if start in seen:
                continue
            stack = [start]
            seen.add(start)
            comp = []
            while stack:
                u = stack.pop()
                comp.append(u)
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            groups.append(comp)
        return groups

    def choose_max_independent_sets(self, group, max_solutions=None):
        """
        Input: group (list[str] or list[int]) of trait IDs

        Output: list_of_lists
            A list of independent sets (each is a list of IDs),
            where EVERY set has the SAME length and that length is maximum
            among all independent sets in this group.

        max_solutions:
            None => return all maximum solutions found (can be huge)
            int  => cap number of returned maximum solutions
        """
        group = set(str(x) for x in group)

        # adjacency restricted to this group (symmetrized)
        adj = {u: set() for u in group}
        for u in group:
            for v in (self.traits[u].dupes or []):
                v = str(v)
                if v in group and v != u:
                    adj[u].add(v)
                    adj[v].add(u)

        nodes = set(adj.keys())
        best_size = -1
        sols = set()  # store as sorted tuples to dedupe

        def record(chosen):
            nonlocal best_size, sols
            k = len(chosen)
            if k > best_size:
                best_size = k
                sols = {tuple(sorted(chosen))}
            elif k == best_size:
                sols.add(tuple(sorted(chosen)))

        def rec(chosen, rem):
            nonlocal best_size, sols

            # prune: can't beat current best
            if len(chosen) + len(rem) < best_size:
                return

            # optional cap (only after we have max-size solutions)
            if max_solutions is not None and best_size >= 0 and len(sols) >= max_solutions:
                return

            if not rem:
                record(chosen)
                return

            # branch on a high-degree node for speed
            u = max(rem, key=lambda x: len(adj[x] & rem))

            # include u
            rec(chosen + [u], rem - {u} - (adj[u] & rem))
            # exclude u
            rec(chosen, rem - {u})

        rec([], nodes)

        out = [list(t) for t in sols]
        out.sort()
        return out




















