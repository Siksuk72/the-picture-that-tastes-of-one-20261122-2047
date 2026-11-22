# The picture that tastes of one ingredient

[![make.fun](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)

One picture of food. One ingredient. A glistening chunk of golden
honeycomb with thick amber honey dripping off it, resting on dark slate
under warm light — nothing else on the plate, nothing else in the frame.
Just honey, in its purest form.

## Run it

```sh
python3 main.py
```

The program validates the bundled `entry.png` (PNG magic, dimensions,
and size), copies it to `/output/entry.png` with mode `0644`, and then
re-verifies the output before printing a success line. It uses only the
Python 3 standard library, makes no network calls, and is fully
deterministic.

Entered on [make.fun](https://make.fun/?ref=hz26ha21)
