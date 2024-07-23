import tempfile

import pandas as pd
from gensim.models import Word2Vec
from pecanpy import node2vec


class SNAP:
    def fit(self, X: pd.DataFrame) -> None:
        """引数は scikit-learn の style に準拠 (pipeline で利用可)
        参考：
        https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline.fit
        """
        with tempfile.NamedTemporaryFile("w+t") as temp_file:
            X[["source_id", "target_id"]].to_csv(temp_file, sep="\t", index=False, header=False)

            g = node2vec.SparseOTF(p=1, q=1, workers=1, verbose=False)
            g.read_edg(temp_file.name, weighted=False, directed=False)
            # generate random walks
            walks = g.simulate_walks(num_walks=10, walk_length=80, n_ckpts=10, pb_len=10)
            # use random walks to train embeddings
            self.w2v_model = Word2Vec(walks, vector_size=8, window=3, min_count=0, sg=1, workers=1, epochs=1)
