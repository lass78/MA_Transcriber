def sec_to_hhmmss(seconds):
    h = int(seconds / 3600)
    m = int((seconds - h * 3600)/60)
    s = int(seconds - (h * 3600 + m * 60))

    return h, m, s

def hhmmss_to_sec(h,m,s):
    seconds = h*3600 + m * 60 + s
    return seconds