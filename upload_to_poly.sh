#!/bin/bash

python3 mvrk.py --config ./demo_src/config.py --source_dir ./demo_src/ --build_dir ./tmp/
rsync -rP --delete tmp/* ../poly000.github.io
cp google8812b0ec10b9d67f.html ../poly000.github.io
(cd ../poly000.github.io && git add . && git commit -m update  && git push)
