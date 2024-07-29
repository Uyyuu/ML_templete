import numpy as np
from typing import List
import math
from tqdm import tqdm
import time

class DCSBM:
    def __init__(self, graph, num_communities: int, seed: int) -> None:
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.num_communities = num_communities
        self.A = self.calculate_adjacency_matrix()
        np.random.seed(seed)
        self.communities = np.random.randint(0, num_communities, self.num_nodes)
        self.degrees = self.calculate_degrees()
        self.m = self.calculate_egdes()
        self.kappa = self.calculate_kappa()
 
        self.theta = self.calculate_theta()
        self.w = self.m

    def calculate_adjacency_matrix(self) -> np.ndarray:
        A = np.zeros((self.num_nodes, self.num_nodes))
        for node in range(self.num_nodes):
            for key, value in self.graph[node].items():
                if node == key:
                    # 自己エッジは二倍とする
                    A[node, key] = 2*value['weight']
                else:
                    A[node, key] = value['weight']
        
        return A
    
    def calculate_degrees(self) -> np.ndarray:
        degrees = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            for d in self.A[i]:
                degrees[i] += d
        
        return degrees
    
    def calculate_kappa(self) -> np.ndarray:
        kappa = np.zeros(self.num_communities)
        for i in range(self.num_nodes):
            kappa[self.communities[i]] += self.degrees[i]

        return kappa
    
    def calculate_egdes(self) -> np.ndarray:
        m = np.zeros((self.num_communities, self.num_communities))
        for i in range(self.num_nodes):
            # Aが非ゼロのところだけを探索
            for j in np.nonzero(self.A[i])[0]:
                m[self.communities[i], self.communities[j]] += self.A[i][j]

        return m
    
    def calculate_theta(self) -> np.ndarray:
        theta = np.zeros(self.num_nodes)
        for i in range(self.num_nodes):
            theta[i] = self.degrees[i]/self.kappa[self.communities[i]]

        return theta
    
    def log_likelihood(self) -> float:
        ll = 0
        for r in range(self.num_communities):
            for s in range(self.num_communities):
                try:
                    ll += self.m[r][s]*math.log(self.m[r][s]/(self.kappa[r]*self.kappa[s]))
                except ValueError:
                    ll += 0

        return ll
    
    def delta(self, new_x, old_x) -> float:
        try:
            x = new_x*math.log(new_x)
        except ValueError:
            x = 0
        
        try:
            y = old_x*math.log(old_x)
        except ValueError:
            y = 0
        
        return x - y
       
    def count_edges_to_group(self, node: int, group: int) -> int:
        edges_to_group = 0
        # Aが非ゼロのところだけを探索
        for neighbor in np.nonzero(self.A[node])[0]:
            if self.communities[neighbor] == group and neighbor != node:
                edges_to_group += self.A[node][neighbor]

        return edges_to_group
    
    def delta_log_likelihood(self, node: int, old_community: int, new_community: int) -> float:
        delta_ll = 0

        # kappa_r → kappa_r - k_i
        delta_ll -= 2*self.delta(self.kappa[old_community] - self.degrees[node], self.kappa[old_community])

        # kappa_s → kappa_s - k_i
        delta_ll -= 2*self.delta(self.kappa[new_community] + self.degrees[node], self.kappa[new_community])

        # m_rs → m_rs + k_ir - k_is
        k_ir = self.count_edges_to_group(node, old_community)
        k_is = self.count_edges_to_group(node, new_community)
        delta_ll += 2*self.delta(self.m[old_community][new_community] + k_ir - k_is, self.m[old_community][new_community])

        # m_rr → m_rr - 2(k_ir + u_i)
        delta_ll += self.delta(self.m[old_community][old_community] - 2*(k_ir + self.A[node][node]//2), self.m[old_community][old_community])

        # m_ss → m_ss - 2(k_is + u_i)
        delta_ll += self.delta(self.m[new_community][new_community] + 2*(k_is + self.A[node][node]//2), self.m[new_community][new_community])

        for t in range(self.num_communities):
            if t == old_community or t == new_community:
                continue

            # m_rt, m_st
            k_it = self.count_edges_to_group(node, t)
            delta_ll += 2*self.delta(self.m[old_community][t] - k_it, self.m[old_community][t])
            delta_ll += 2*self.delta(self.m[new_community][t] + k_it, self.m[new_community][t])

        return delta_ll
    
    def update_parameter(self) ->  None:
        self.kappa = self.calculate_kappa()
        self.m = self.calculate_egdes()
        self.theta = self.calculate_theta()
        self.w = self.m

    def fit(self, max_iter: int = 100) -> None:
        for _ in tqdm(range(max_iter)):
            prev_ll = self.log_likelihood()
            # Nステップの操作中の最大対数尤度とそのコミュニティの構成
            best_community = self.communities.copy()
            best_ll = prev_ll

            moved_nodes = set()
            # 各ノードを一回移動させる
            while len(moved_nodes) < self.num_nodes:
                for node in range(self.num_nodes):
                    if node not in moved_nodes:
                        old_comunity = self.communities[node]
                        # あるノードの最適な移動先を探す
                        max_ll = prev_ll
                        max_community = old_comunity

                        for new_community in range(self.num_communities):
                            if new_community != old_comunity:
                                ll = prev_ll + self.delta_log_likelihood(node, old_comunity, new_community)
                                if max_ll < ll:
                                    max_ll = ll
                                    max_community = new_community
                        
                        # print(f"{node}の探索終了")
                        self.move_node(node, max_community)
                        # パラメータの更新
                        # print("パラメータの更新開始")
                        moved_nodes.add(node)
                        # print("パラメータの更新終了")

                    # Nステップのうち最大対数尤度となるコミュニティ分配を保存
                    if best_ll < max_ll:
                        best_ll = max_ll
                        best_community = self.communities.copy()
            
            self.communities = best_community.copy()
            self.update_parameter()
            if best_ll - prev_ll < 1e-5:
                break
                                
    
    def move_node(self, node: int, new_community: int) -> None:
        # ノードを新しいコミュニティに配置
        self.communities[node] = new_community
        self.update_parameter()

    def get_communities(self) -> np.ndarray[int]:
        return self.communities

    def get_theta(self) -> np.ndarray[float]:
        return self.theta

    def get_w(self) -> np.ndarray[float]:
        return self.w  