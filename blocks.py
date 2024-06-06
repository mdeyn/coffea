from pybitcointools import *
import rlp
import re
from transactions import Transaction

class Block():
  def __init__(self,data=None):
    if not data:
      return
    if re.match('^[0-9a-fA-F]*$',data):
      data = data.decode('hex')
    header, tree_node_list, transaction_list, sibling_list = rlp.decode(data)
    h = rlp.decode(header)
    self.prevhash = encode(h[0],16,64)
    self.coinbase = encode(h[1],16,40)
    self.balance_root = encode(h[2],256,32)
    self.contract_root = encode(h[3],256,32)
    self.difficulty = h[4]
    self.timestamp = h[5]
    transactions_root = encode(h[6],256,32)
    siblings_root = encode(h[7],256,32)
    self.nonce = h[8]
    self.datastore = {}
    for nd in rlp.decode(tree_node_list):
      ndk = bin_sha256(nd)
      self.datastore[ndk] = rlp.decode(nd)
    self.transactions = [Transaction(x) for x in rlp.decode(transaction_list)]
    self.siblings = [rlp.decode(x) for x in rlp.decode(sibling_list)]

    if self.balance_root != '' and self.balance_root not in self.datastore:
      raise Exception("Balance Merkle root not found!")
    if self.contract_root != '' and self.contract_root not in self.datastore:
      raise Exception("Contract Merkle root not found!")
    if bin_sha256(transaction_list) != transactions_root:
      raise Exception("Transaction list root hash does not match!")
    if bin_sha256(sibling_list) != sibling_root:
      raise Exception("Transaction list root hash does not match!")
    for siblng in self.self.siblings:
      if sibling[0] != self.prevhash:
        raise Exception("Sibling's parent is not my parent!")


..
