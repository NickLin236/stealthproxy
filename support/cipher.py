class Cipher:
    def __init__(self, encodePassword,decodePassword):
        self.encodePassword = encodePassword.copy()
        self.decodePassword = decodePassword.copy()
        #print(self.encodePassword)
        #print(self.decodePassword)

    def encode(self, bs):
        i=0
        while i < len(bs):
            bs[i] = self.encodePassword[bs[i]]
            i += 1

    def decode(self, bs):
        i=0
        while i < len(bs):
            bs[i] = self.decodePassword[bs[i]]
            i += 1

    @classmethod
    def NewCipher(cls, encodePassword):
        decodePassword = encodePassword.copy()
        i=0
        while i < len(encodePassword):
            v=encodePassword[i]
            decodePassword[v] = i
            i += 1
        return cls(encodePassword, decodePassword)

