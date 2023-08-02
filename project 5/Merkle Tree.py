import hashlib

#MerkleTree RFC 6962

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.levels = []

    def build_tree(self):
        #build_tree()方法根据提供的叶子构建树
        self.levels.append(self.leaves)

        level = self.leaves
        while len(level) > 1:
            level = self.build_level(level)
            self.levels.append(level)

    def build_level(self, level):
        next_level = []
        i = 0
        while i < len(level):
            if i + 1 < len(level):
                next_level.append(self.hash_children(level[i], level[i+1]))
            else:
                next_level.append(self.hash_children(level[i], level[i]))
            i += 2

        return next_level

    def hash_children(self, left_child, right_child):
        combined = left_child + right_child
        return hashlib.sha256(combined).digest()

    def get_root(self):
        #get_root()方法返回树的根散列
        if len(self.levels) == 0:
            return None
        return self.levels[-1][0]

    def get_proof(self, leaf_index):
        #get_proof()方法计算特定叶索引的证明，并沿着到根的路径提供必要的兄弟散列

        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise ValueError("Invalid leaf index")

        proof = []

        for i, level in enumerate(self.levels):
            if i == len(self.levels) - 1:
                break

            if leaf_index % 2 == 0:
                if leaf_index + 1 < len(level):
                    proof.append(level[leaf_index + 1])
                    leaf_index = leaf_index // 2
            else:
                if leaf_index - 1 >= 0:
                    proof.append(level[leaf_index - 1])
                    leaf_index = (leaf_index - 1) // 2
        
        return proof


leaves = [
    b'202100150027',
    b'MayHao',
    b'July',
    b'fifth'
]

merkle_tree = MerkleTree(leaves)
merkle_tree.build_tree()

root_hash = merkle_tree.get_root()
print("Root Hash:", root_hash.hex())

leaf_index = 2
proof = merkle_tree.get_proof(leaf_index)
print("Proof for leaf", leaf_index, ":", [hash_value.hex() for hash_value in proof])
