import numpy as np

def chessboard_symmetries(n):
  def flip_along_diag(a):
    for i in range(0, a.shape[0]):
      for j in range(i+1, a.shape[0]):
        a[i][j],a[j][i] = a[j][i],a[i][j]
    return a

  idt = np.arange(n*n).reshape(n,n)
  r_y = idt.copy()[::-1]
  r_x = np.flip(idt.copy(), 1)
  r_270 = np.rot90(idt.copy())
  r_180 = np.rot90(r_270.copy())
  r_90 = np.rot90(r_180.copy())
  r_d1 = flip_along_diag(idt.copy())
  r_d2 = flip_along_diag(np.flip(idt.copy()))

  return {
        'r90': r_90.flatten(),
        'r180': r_180.flatten(),
        'r_270': r_270.flatten(),
        'r_x': r_x.flatten(),
        'r_y': r_y.flatten(),
        'r_d1': r_d1.flatten(),
        'r_d2': r_d2.flatten()
    }


if __name__ == '__main__':
  n = 4
  symmetries = chessboard_symmetries(n)
  for symm in symmetries:
    print(symmetries[symm])