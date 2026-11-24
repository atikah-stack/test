import cv2, numpy as np, sys
a, b = cv2.VideoCapture(sys.argv[1]), cv2.VideoCapture(sys.argv[2])
i = 0; hook = []; free = []; worst_mean_shift = 0
while True:
    oa, fa = a.read(); ob, fb = b.read()
    if not oa or not ob:
        print("source ended" if not oa else "", "output ended" if not ob else "", "at frame", i); break
    if i % 3 == 0:
        p = cv2.PSNR(fa, fb)
        if i < 313: hook.append(p)
        elif 8.6 * 60 < i < 15.9 * 60: free.append(p)   # stretch with no graphics
        if i < 313 or 8.6 * 60 < i < 15.9 * 60:
            worst_mean_shift = max(worst_mean_shift, np.abs(fa.reshape(-1, 3).mean(0) - fb.reshape(-1, 3).mean(0)).max())
    i += 1
rest_a = sum(1 for _ in iter(lambda: a.read()[0], False)); rest_b = sum(1 for _ in iter(lambda: b.read()[0], False))
print("frames compared", i, "| leftover src", rest_a, "out", rest_b)
print("hook section PSNR min %.1f dB mean %.1f dB" % (min(hook), np.mean(hook)))
print("graphics-free section PSNR min %.1f dB mean %.1f dB" % (min(free), np.mean(free)))
print("max mean colour shift (0-255 scale): %.2f" % worst_mean_shift)
