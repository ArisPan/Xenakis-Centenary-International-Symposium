/* We use two Synths as sources, one creating pulses of PinkNoise (a kind of Noise which has less energy at high frequencies than at low), and another creating pulses of sine waves. The pulses are created using the UGens Impulse and Decay2. These are then reverberated using a chain of AllpassC, which is a kind of delay. */

(
SynthDef("DecayPink",
	{
		// direct will control the proportion of direct to processed signal
		arg outBus = 0, effectBus, direct = 0.5, decayTime = 0.2;
		var source;

		source = Decay2.ar(
			Impulse.ar(1, 0.25), /* in */
			0.01,    /* attackTime */
			decayTime,    /* decayTime */
			PinkNoise.ar);    /* mul */

		// This is our main output.
		Out.ar(outBus, source * direct);
		// This is our effects output.
		Out.ar(effectBus, source * (1 - direct));
	}
).add;

SynthDef("DecaySin",
	{
		arg outBus = 0, effectBus, direct = 0.5, freq = 440;
		var source;

		source = Decay2.ar(
			Impulse.ar(0.3, 0.25),
			0.3,
			1,
			SinOsc.ar(SinOsc.kr(0.2, 0, 110, freq))
		);

		// This is our main output.
		Out.ar(outBus, source * direct);
		// This is our effects output.
		Out.ar(effectBus, source * (1 - direct));
	}
).add;

SynthDef("Reverb",
	{
		arg outBus = 0, inBus;
		var input;

		input = In.ar(inBus, 1);

		// This is our make-do reverb.
		// 16.do takes a function as an argument. It will evaluate it 16 times.
		16.do(
			{
				input = AllpassC.ar(
					input,
					0.04,
					// {}.dup(n) evaluates the function n times.
					// The default n is 2, making a stereo reverb.
					// Returns an Array.
					{Rand(0.001, 0.04)}.dup,
					3
				)
			}
		);

		Out.ar(outBus, input);
	}
).add;

b = Bus.audio(s, 1);
)

(
x = Synth.new("Reverb", [\inBus, b]);
y = Synth.before(x, "DecayPink", [\effectBus, b]);
z = Synth.before(x, "DecaySin", [\effectBus, b, \outBus, 1]);
)

(
h = OSCFunc( { | msg, time, addr, port |
    var pyFreq, pyDecTime;

    pyFreq = msg[1].asFloat;
	pyDecTime = msg[2].asFloat;
	( "DecaySin's new frequency:" + pyFreq ).postln;
	( "Delay time:" + pyDecTime ).postln;
	y.set( \decayTime, pyDecTime );    /* Redefine DecayPink's DecayTime */
	z.set( \freq, pyFreq );    /* Redefine DecaySin's frequency */
}, "/sonify" );
)