def integral(a_i, h, n):
	integ = 0.0
	for j in range(n):
		a_ij = a_i + (j + 0.5) * h
		integ += cos(a_ij) * h
	return integ
