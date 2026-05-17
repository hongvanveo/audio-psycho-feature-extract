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

if [ -s "$workdir/recovered.txt" ]; then
    pass "RECOVERED_CREATED"
else
    fail "RECOVERED_CREATED" "recovered.txt missing"
fi

if [ -s "$workdir/recovered.txt" ] && [ -s "$expected" ] && [ -f "$viewed" ] && [ "$viewed" -nt "$workdir/recovered.txt" -o "$viewed" -ef "$workdir/recovered.txt" ]; then
    cmp -s "$workdir/recovered.txt" "$expected"
    if [ $? -eq 0 ]; then
        pass "MESSAGE_RECOVERED"
    else
        fail "MESSAGE_RECOVERED" "recovered message differs"
    fi
else
    fail "MESSAGE_RECOVERED" "recovered.txt not viewed with cat or expected message missing"
fi
