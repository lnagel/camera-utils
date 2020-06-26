# coding: utf-8
import logging
import re
import shutil
import sys
from pathlib import Path

logger = logging.getLogger("portrait_mover")


def check_dir(path):
    if path.is_dir():
        if re.match("^IMG_[0-9]{8}_[0-9]{6}(|_[0-9])$", path.name):
            do_move(path.parent, path)
        else:
            # scan members
            for item in path.iterdir():
                check_dir(item)


def get_next_name(name):
    seq_match = re.match("^(IMG_[0-9]{8}_[0-9]{6})_([0-9]+)$", name)
    if seq_match:
        return f"{seq_match[1]}_{int(seq_match[2])+1}"
    else:
        return f"{name}_1"


def do_move(base_dir, portrait_dir):
    # collect files to move
    candidates = []
    removables = []
    others = []
    for item in portrait_dir.iterdir():
        if re.match("^(00000|00100)(.*)(IMG|PORTRAIT)_(00000|00100)_BURST([0-9]+)(|_COVER).jpg$", item.name):
            candidates.append(item)
        elif item.name in {".deletemarkers"}:
            removables.append(item)
        else:
            others.append(item)

    base_name = portrait_dir.name
    target = base_dir / f"{base_name}.jpg"

    while target.exists():
        base_name = get_next_name(name=base_name)
        target = base_dir / f"{base_name}.jpg"

    if not target.exists():
        if len(candidates) == 1 and len(others) == 0:
            logger.info(f"MV {base_dir}/{{{candidates[0].relative_to(base_dir)} -> {target.relative_to(base_dir)}}}")
            candidates[0].rename(target)
        elif len(candidates) > 1 or len(others) > 0:
            logger.debug(f"?? {portrait_dir}")
    for removable in removables:
        logger.debug(f"RM {removable}")
        shutil.rmtree(removable)
    if len(list(portrait_dir.iterdir())) == 0:
        logger.debug(f"RM {portrait_dir}")
        portrait_dir.rmdir()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    for path_str in sys.argv[1:]:
        check_dir(Path(path_str))
