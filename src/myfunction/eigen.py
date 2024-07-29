import numpy as np

def SpectralClusteringPlot(A: np.ndarray):
    degree_matrix = np.diag(np.sum(A, axis=1))
    laplacian_matrix = degree_matrix - A
    eigenvalues, eigenvectors = np.linalg.eig(laplacian_matrix)

    # 固有値と固有ベクトルのペアを固有値の昇順でソート
    eigen_pairs = [(eigenvalues[i], eigenvectors[:, i]) for i in range(len(eigenvalues))]
    eigen_pairs.sort(key=lambda x: x[0])

    print(eigen_pairs[0][0],eigen_pairs[0][1])
    print(eigen_pairs[1][0],eigen_pairs[1][1])
    print(eigen_pairs[2][0], eigen_pairs[2][1])

    return eigen_pairs[1][1], eigen_pairs[2][1]
