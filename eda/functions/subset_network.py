import networkx as nx
def subset_network(network_df, weight_min, weight_max, num_edges = None):
    '''
    A function to subset a network using weight cutoff
    if num_edges is None, the returned subset network will have the edges outside the weight limits = 0 and all the nodes are preserved
    if num_edges is a number, the returned subset network will have the number of edges same as num_edges and nodes with degrees = 0 are removed
    '''
    subset = network_df[(network_df > weight_min) & (network_df < weight_max)]
    subset_edge = subset.stack() # convert from wide to long to determine # edges left
    # return the subnetwork with all the edges and nodes preserved
    if num_edges == None:
        print('Number of edges left:',len(subset_edge)/2)
        subset = subset.fillna(0)
        G = nx.convert_matrix.from_pandas_adjacency(subset)
        return subset, G
    # return the subnetwork with edges < cutoff and nodes with degree = 0 removed
    else:
        sorted_subset_edge = subset_edge.sort_values(0, ascending = False).reset_index()
        if num_edges > len(sorted_subset_edge)*2:
            print(f'not enough edges to filter with at the cutoff of {num_edges}')
        else:
            sorted_subset_edge_filtered = sorted_subset_edge.iloc[:num_edges*2, :]
            new_subset_adj = sorted_subset_edge_filtered.pivot(index = 'level_0', columns = 'level_1').fillna(0) # convert from edgelist back to adjacency matrix
            new_subset_adj.columns = new_subset_adj.columns.droplevel()
            G = nx.convert_matrix.from_pandas_adjacency(new_subset_adj)
        return new_subset_adj, G