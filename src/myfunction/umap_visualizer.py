import umap.umap_ as umap
import matplotlib.pyplot as plt

def umap_visualizer(A, A_expected, A_expected_zero, n_neighbors, random_state, n_components=2, metric="euclidean") -> None:
    # UMAPを適用し、2次元に埋め込む
    embedding_orig = umap.UMAP(n_components=n_components, n_neighbors=avdg, random_state=22, metric="euclidean").fit_transform(A)
    embedding_expected = umap.UMAP(n_components=n_components, n_neighbors=avdg, random_state=22, metric="euclidean").fit_transform(A_expected)
    embedding_expected_zero = umap.UMAP(n_components=n_components, n_neighbors=avdg, random_state=22, metric="euclidean").fit_transform(A_expected_zero)

    # 結果をプロット
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    ax1.scatter(embedding_orig[:, 0], embedding_orig[:, 1], c=communities, cmap='coolwarm', s=50)
    ax1.set_title('UMAP on Original Non Weight Adjacency Matrix')
    ax1.set_xlabel('UMAP Dimension 1')
    ax1.set_ylabel('UMAP Dimension 2')

    ax2.scatter(embedding_expected[:, 0], embedding_expected[:, 1], c=communities, cmap='coolwarm', s=50)
    ax2.set_title('UMAP on Expected Adjacency Matrix')
    ax2.set_xlabel('UMAP Dimension 1')
    ax2.set_ylabel('UMAP Dimension 2')

    ax3.scatter(embedding_expected_zero[:, 0], embedding_expected_zero[:, 1], c=communities, cmap='coolwarm', s=50)
    ax3.set_title('UMAP on Expected Adjacency Matrix Zero')
    ax3.set_xlabel('UMAP Dimension 1')
    ax3.set_ylabel('UMAP Dimension 2')

    plt.tight_layout()
    plt.show()