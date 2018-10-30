class StringStream:
	string = None
	offset = 0

	def __init__(self, s):
		self.string = s

	def read(self, idx=-1):
		if idx is None:
			idx = -1
		if self.offset == len(self.string):
			return None

		s = self.string[self.offset:idx]
		self.offset += idx
		return s

	def get(self):
		if self.offset == len(self.string):
			return None

		s = self.string[self.offset]
		self.offset += 1
		return s

	def seek(self, offset, whence=0):
		if whence == 0: #SEEK_SET
			if offset < 0:
				raise ValueError
			self.offset = offset
		elif whence == 1: #SEEK_CUR
			if -offset > self.offset:
				raise ValueError
			self.offset += offset
		elif whence == 2: #SEEK_END
			if offset > len(self.string):
				raise ValueError
			self.offset = len(self.string) - offset

	def unget(self):
		if self.offset != 0:
			self.offset -= 1

	def peek(self):
		return self.string[self.offset]
	def tell(self):
		return self.offset
