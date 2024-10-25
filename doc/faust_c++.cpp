#pragma once
#include "JuceHeader.h"

class SpectralTiltFilter_TF1S {

public:
    void setSampleRate(double sampleRateIn) {
        SR = sampleRateIn;
    }
    void set_tf1s(double b1, double b0, double a0, double w1) {
        double c = 1 / tan(w1*0.5 / SR);
        double d = a0 + c;
        b1d = (b0 - b1 * c) / d;
        b0d = (b0 + b1 * c) / d;
        a1d = (a0 - c) / d;
        g = a0 / b0;
    }
    double process_tf1(double sampleIn) {
        input_1 = input;
        input = sampleIn;
        output_1 = output;
        output = ((input * b0d) + (input_1 * b1d)) + (output_1 * -a1d);
        double output_gained = g * output;
        return output_gained;
    }

private:
    double SR = 44100.0;
    double b1d = 0.0;
    double b0d = 0.0;
    double a1d = 0.0;
    double g = 1.0;
    double input = 0.0;
    double output = 0.0;
    double input_1 = 0.0;
    double output_1 = 0.0;

};

class SpectralTiltFilter {

public:
    void setSampleRate(double sampleRateIn) {
        SR = sampleRateIn;
        T = 1 / SR;
        for (int i = 0; i < filterArray.size(); i++) {
            SpectralTiltFilter_TF1S* unit = filterArray.getUnchecked(i);
            unit->setSampleRate(sampleRateIn);
        }
    }
    void setFilterN(int N) {
        filterN = N;    //N must be 2 or more
        filterArray.clear();
        for (int i = 0; i < N; i++) {
            SpectralTiltFilter_TF1S* unit = new SpectralTiltFilter_TF1S();
            unit->setSampleRate(SR);
            filterArray.add(unit);
        }
    }
    void setFilter(double f0, double bw, double alphaIn) {
        alpha = alphaIn;
        w0 = 2 * MathConstants<float>::pi * f0;
        f1 = f0 + bw;
        r = pow((f1 / f0), (1.0 / static_cast<double>(filterN - 1))); //N must be at least 2
        for (int i = 0; i < filterN; i++) {
            SpectralTiltFilter_TF1S* unit = filterArray.getUnchecked(i);
            unit->set_tf1s(1.0, mzh(i), mph(i), 1);
        }
    }
    double processSample(double sampleIn) {
        double input_filtered = sampleIn;
        for (int i = 0; i < filterN; i++) {
            SpectralTiltFilter_TF1S* unit = filterArray.getUnchecked(i);
            input_filtered = unit->process_tf1(input_filtered);
        }
        return input_filtered;
    }
    double prewarp(double w, double T, double wp) {
        return wp * tan(w*T / 2) / tan(wp*T / 2);
    }
    double mz(int i) {
        return w0 * pow(r, (-alpha + i));
    }
    double mp(int i) {
        return w0 * pow(r, i);
    }
    double mzh(int i) {
        return prewarp(mz(i), T, w0);
    }
    double mph(int i) {
        return prewarp(mp(i), T, w0);
    }

private:
    OwnedArray<SpectralTiltFilter_TF1S> filterArray;
    int filterN = 2;
    double SR = 44100.0;
    double T = 1 / 44100.0;
    double w0 = 10.0;
    double f1 = 220.0;
    double r = 40.0;
    double alpha = 0.5;

};

//Initialization:
SpectralTiltFilter spectralTilt;
spectralTilt.setSampleRate(sampleRate);
spectralTilt.setFilterN(12); // N must be 2 or more
spectralTilt.setFilter(cornerFreqHz, widthOfRollOffBand, slope); //slope is set as 0 = flat, -0.5 = 3dB/oct LPF, -1 = 6 db/oct LPF

//Sample processing:
filteredNoise = spectralTilt.processSample(whiteNoise);