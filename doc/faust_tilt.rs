spectral_tilt(N,f0,bw,alpha) = seq(i,N,sec(i)) with {
  sec(i) = g * tf1s(b1,b0,a0,1) with {
    g = a0/b0; // unity dc-gain scaling
    b1 = 1.0;
    b0 = mzh(i);
    a0 = mph(i);
    mzh(i) = prewarp(mz(i),ma.SR,w0); // prewarping for bilinear transform
    mph(i) = prewarp(mp(i),ma.SR,w0);
    prewarp(w,SR,wp) = wp * tan(w*T/2) / tan(wp*T/2) with { T = 1/ma.SR; };
    mz(i) = w0 * r ^ (-alpha+i); // minus zero i in s plane
    mp(i) = w0 * r ^ i; // minus pole i in s plane
    f0p = max(f0,ma.EPSILON); // cannot go to zero
    w0 = 2 * ma.PI * f0p; // radian frequency of first pole
    f1 = f0p + bw; // upper band limit
    r = (f1/f0p)^(1.0/float(N-1)); // pole ratio (2 => octave spacing)
  };
};