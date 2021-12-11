import hashlib, json, datetime


class Block:
    """ブロックチェーンのブロックを表す

    ハッシュ部分以外は比較的何でも良い
    重要なのはハッシュの部分で、ハッシュに入っている値を後から書き換えようとすると、ハッシュの値が変わってしまうので、書き換えることはできない
    今回ハッシュに含まれているもので言うと
    - index
    - timestamp（取引時間）
    - transaction（取引内容）
    - previous_hash（前の取引のハッシュ = 前の取引の index, timestamp, transaction, previous_hash
       - previous_hash がハッシュに入っていることで、ここまでのすべての取引を改変できなくなる
    """
    def __init__(
        self,
        index: int,
        previous_hash: str,
        transaction: str,  # 取引データの中身
    ):
        self.__index = index
        self.__timestamp = str(datetime.datetime.now().timestamp())
        self.__previous_hash = previous_hash
        self.__transaction = transaction
        self.__current_hash = self.calculate_hash()

    def get_index(self) -> int:
        return self.__index

    def get_hash(self) -> str:
        return self.__current_hash

    def get_transaction(self) -> str:
        return self.__transaction

    def calculate_hash(self) -> str:
        data_hash = {
            "index": self.__index,
            "timestamp": self.__timestamp,
            "previous_hash": self.__previous_hash,
            "transaction": self.__transaction,
        }
        json_text = json.dumps(data_hash, sort_keys=True)
        return hashlib.sha256(json_text.encode("ascii")).hexdigest()

# とりあえず配列で
block_chain = []

# 一番最初のブロック
genesis = Block(0, "", "取引内容")
block_chain.append(genesis)

for i in range(5):
    new_block = Block(i + 1, block_chain[i].get_hash(), "取引内容" + str(i+1))
    block_chain.append(new_block)

# ブロックチェーンの内容を出力
for block in block_chain:
    print(block.get_index(), block.get_hash(), block.get_transaction())

