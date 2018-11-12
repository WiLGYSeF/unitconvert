class StringStream:
	string = None
	offset = 0

	def __init__(self, s):
		self.string = s

	def read(self, length=-1):
		if self.offset == len(self.string):
			return None

		if self.offset + length > len(self.string):
			length = len(self.string) - self.offset

		s = self.string[self.offset:self.offset + length]
		self.offset += length
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
				raise ValueError("stringstream seek cannot be less than zero for SEEK_SET")
			if offset > len(self.string):
				raise ValueError("stringstream seek cannot be greater than length for SEEK_SET")
			self.offset = offset
		elif whence == 1: #SEEK_CUR
			if -offset > self.offset:
				offset = -self.offset
			elif offset + self.offset > len(self.string):
				offset = len(self.string) - self.offset
			self.offset += offset
		elif whence == 2: #SEEK_END
			if offset < 0:
				raise ValueError("stringstream seek cannot be less than zero for SEEK_END")
			if offset > len(self.string):
				raise ValueError("stringstream seek cannot be greater than length for SEEK_END")
			self.offset = len(self.string) - offset

	def unget(self):
		if self.offset != 0:
			self.offset -= 1

	def peek(self):
		return self.string[self.offset]

	def tell(self):
		return self.offset
