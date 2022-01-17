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
        # self.__timestamp = str(datetime.datetime.now().timestamp())
        self.__timestamp = "1"
        self.__previous_hash = previous_hash
        self.__transaction = transaction
        self.__current_hash = self.calculate_hash()
        # nonce を追加
        self.__nonce = None

    def set_nonce(self, nonce: int):
        self.__nonce = nonce

    def get_index(self) -> int:
        return self.__index

    def get_hash(self) -> str:
        return self.__current_hash

    def get_transaction(self) -> str:
        return self.__transaction

    def get_hash_with_nonce(self) -> str:
        joined = self.__current_hash + str(self.__nonce)
        return hashlib.sha256(joined.encode('ascii')).hexdigest()

    def get_nonce(self) -> int:
        return self.__nonce

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

for i in range(5):
    if i == 0:
        new_block = Block(i, "", "取引内容")
    else:
        new_block = Block(i, block_chain[i - 1].get_hash(), "取引内容" + str(i))

    # マイニング処理
    difficulty = 6  # マイニングの難易度
    nonce = 0
    while True:
        # none を結合したハッシュを計算
        joined = new_block.get_hash() + str(nonce)
        nonce_joined_hash = hashlib.sha256(joined.encode("ascii")).hexdigest()

        # 先頭から difficulty 桁が 0 で埋まっているか確認
        if nonce_joined_hash[:difficulty:] == "000000":
            # マイニング終了
            new_block.set_nonce(nonce)
            break
        nonce += 1

    # マイニングに成功したら保存できる
    block_chain.append(new_block)

# ブロックチェーンの内容を出力
for block in block_chain:
    print(
        block.get_index(), 
        block.get_transaction(), 
        block.get_hash(), 
        block.get_hash_with_nonce(), 
        block.get_nonce(),
    )

