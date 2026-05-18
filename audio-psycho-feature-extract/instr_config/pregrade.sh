#!/bin/bash
: <<'END'
Pregrade script for psycho-feature extraction lab.
It verifies that the learner created recovered.txt and extracted the
original hidden message from the provided cover/stego pair.
END

homedir=$1
destdir=$2
dbg=/tmp/audio-psycho-feature-extract-pregrade.log

workdir="$homedir/$destdir/stego"
resultdir="$homedir/$destdir/.local/result"
result="$resultdir/psycho_check.txt"
expected="$workdir/.expected_message.txt"
viewed="$workdir/.recovered_viewed"

mkdir -p "$resultdir"
: > "$result"
echo "pregrade for $homedir/$destdir" > "$dbg"

pass() { echo "PASS_$1" >> "$result"; }
fail() { echo "FAIL_$1: $2" >> "$result"; }

if [ -s "$workdir/cover.wav" ] && [ -s "$workdir/stego.wav" ]; then
    pass "AUDIO_RECEIVED"
else
    fail "AUDIO_RECEIVED" "cover.wav or stego.wav missing"
fi

if [ -s "$workdir/recovered.txt" ]; then
    pass "RECOVERED_CREATED"
else
    fail "RECOVERED_CREATED" "recovered.txt missing"
fi

if [ -s "$workdir/recovered.txt" ] && [ -s "$expected" ] && [ -f "$viewed" ]; then
    python3 - "$workdir/recovered.txt" "$expected" <<'PY'
from pathlib import Path
import sys
recovered = Path(sys.argv[1]).read_bytes().rstrip(b"\r\n")
expected = Path(sys.argv[2]).read_bytes().rstrip(b"\r\n")
sys.exit(0 if recovered == expected else 1)
PY
    if [ $? -eq 0 ]; then
        pass "MESSAGE_RECOVERED"
    else
        fail "MESSAGE_RECOVERED" "recovered message differs"
    fi
else
    fail "MESSAGE_RECOVERED" "recovered.txt not viewed with cat or expected message missing"
fi
