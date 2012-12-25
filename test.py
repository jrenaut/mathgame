

def dostuff():
	data = [('AAA', 0),('AAA', 7),('BBB', 3),('AAA', 10),('DDD', 4)]
	data.sort(key=lambda r:r[1])
	print data
	print reverse_insort(data, ('ABB', 5))
	print data
	print reverse_insort(data, ('zz', 12))
	print data
	print reverse_insort(data, ('xasf', 3.2))
	print data

def reverse_insort(a, x, lo=0, hi=None):
	if lo < 0:
		raise ValueError('lo must be non-negative')
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo+hi)//2
		if a[mid][1] < x[1]: lo = mid+1
		else: hi = mid
	a.insert(lo, x)
	return lo

if __name__ == "__main__":
	dostuff()
